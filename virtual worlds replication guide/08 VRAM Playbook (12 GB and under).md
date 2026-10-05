---
tags: [replication, comfyui, vram, troubleshooting]
---
# VRAM Playbook (12 GB and under)

Everything on this page was **measured, not theorised**, on a 12 GB RTX 4080.
Nine instrumented runs (September research + the 2026-10-04 clean-room
replication) produced this decision tree.

## The problem structure
TRELLIS.2 generation memory has three stacked costs:
1. **UNet resident** — int8 weight alone wants ~5 GB (fp16: 10.3 GB, dead on arrival)
2. **1024³ shape decode** — the shape VAE decode at the upsample stage's floor
   resolution needs **+2.5 GB on top**, and `Trellis2UpsampleStage`
   `target_resolution` has **min = 1024** — you cannot dial it down
3. **Dense mesh post-processing** — a 1024³ marching-cubes mesh is *millions of
   triangles*; decimate/unwrap/bake need multi-GB of their own, **even with all
   models offloaded** (the mesh itself lives on the GPU)

## Decision tree (in order — each step is verified)
- [ ] **1. Free the card.** `nvidia-smi` before every session. The Unreal
      Editor holds ~1.7 GB silently; browsers/games do too. This alone
      moved a failure → pass one stage.
- [ ] **2. Server flags (baseline):**
      `--lowvram --disable-smart-memory --reserve-vram 2`
      (offloads models + keeps headroom for the decode)
- [ ] **3. Still OOM in `VaeDecodeShapeTrellis` or `DecimateMesh`:**
      `--novram` + allocator anti-fragmentation:
      ```bash
      PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
        ../.venv/bin/python main.py --listen 127.0.0.1 --port 8188 \
        --novram --reserve-vram 2
      ```
      (fish: `env PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True ../.venv/bin/python main.py …`
      or run the bash line inside `bash`)
- [ ] **4. Still dying in mesh ops (`DecimateMesh`): go LOW-RES route** — drop the
      upsample stage entirely and decode the low-res shape latent directly; the
      mesh lands at ~128-level detail (blocky but real, UV-unwraps fine).
      **Verified pass on this 12 GB card:**
      [[attachments/trellis2_api_workflow_shape_only.json]] →
      image → structure → shape → decode → unwrap → **GLB ✓** (~7 min).
- [ ] **5. Textured assets on 12 GB: the honest wall.** `BakeTextureFromVoxel`
      (UV bake from voxel colors) requested **4.3 GiB at texture_size 1024 and
      ~10 GiB at 512** — the color voxel field is denser than the shape grid,
      so the request does *not* scale with your texture setting, and it OOMs
      with everything else offloaded. On 12 GB: ship geometry-only GLBs
      (step 4 — UVs ready, texture later in Blender or on a bigger card) or
      switch model (step 6). Textured TRELLIS.2 realistically wants **≥ 16 GB**.
- [ ] **6. Model fallbacks (both native, same template):** set
      `Switch to Trellis2 = false` (Pixal3D) or use Hunyuan3D-2.1 native nodes.
- [ ] **7. Nuclear option:** pre-generated asset pack (course share).

## Measured outcomes (our seven runs, 12 GB card)
| # | Config | Outcome | Memory at failure | Lesson |
|---|---|---|---|---|
| 1 | defaults, full graph | ✗ `VaeDecodeShapeTrellis` | 7.17 + 2.5 GiB | UNet parks in VRAM |
| 2 | `--lowvram --disable-smart-memory` | ✗ same node | 7.16 + 2.5 GiB | flags insufficient **while UE Editor holds 1.7 GB** |
| 3 | + UE closed, `--reserve-vram 2` | ✗ `DecimateMesh` (decode ✓) | 8.74 + 0.5 GiB | decode fixed; dense-mesh ops are next wall |
| 4 | + `--novram`, expandable_segments | ✗ `DecimateMesh` | 10.84 + 0.5 GiB | offload can't help — the 1024³ **mesh data itself** is the hog |
| 5 | low-res graph, bake 1024 | ✗ `BakeTextureFromVoxel` (decode ✓ unwrap ✓) | 9.22 + 4.3 GiB | low-res fixes every earlier stage; bake is its own wall |
| 6 | low-res graph, bake 512 | ✗ same node | 10.58 + 10.0 GiB | bake memory ≠ texture_size — change routes, not settings |
| 7 | low-res, **no bake** (shape-only) | ✅ **GLB written** | — | the 12 GB course route |
| 8 | GUI full template, **switch=false + upsample at shipped 1536**, UE open | ✗ `VaeDecodeShapeTrellis` | 8.41 + 2.5 GiB | the three GUI traps in one run (→ note 06's 12 GB checklist); also proves the **Pixal3D branch shares the same decode wall** |
| 9 | 1024 + texture stage + **PaintMesh (vertex colors)**, no bake | ✅ **textured GLB** (394k `COLOR_0` verts, 19 MB) | — | **textured output IS possible on 12 GB — if you skip the UV bake** and paint vertices instead |

> [!summary] The one-line version for students
> On 12 GB: **close everything, run the flags, and take your TRELLIS.2 GLBs at
> ≤ 1024** — geometry-only, or **textured via vertex colors (`PaintMesh`)**, which
> sidesteps the bake wall entirely (run 9). UV-textured GLBs: texture in Blender
> after, or ≥ 16 GB. ≥ 24 GB: defaults fine.

## ≥ 24 GB: the quality ladder (estimates)
Big cards don't need the survival flags — they spend VRAM on **detail**. Ballpark
budgets (measured anchor: 1024³ decode ≈ +2.5 GiB, texture bake ≈ +4–10 GiB
independent of `texture_size`; N³ scaling for the rest — trust your first
`nvidia-smi` over these tables):

| Your VRAM | Weights | `target_resolution` | bake `texture_size` | server flags | notes |
|---|---|---|---|---|---|
| 16 GB | int8 | 1024 | 1024 | baseline flags | geometry ✅; bake still borderline (see run #5) |
| 24 GB | int8 (bf16 w/ offload) | 1024 → **1536** | 1024–2048 | none needed | full template comfortably at 1024; 1536 ≈ template default |
| 32 GB | **bf16** | **1536** | 2048 | none | batch 1–2 |
| 48 GB+ | bf16 | **2048** (node max) | 4096 | none (optional `--highvram`) | batch 4 via `EmptyTrellis2LatentStructure.batch_size`; multi-object sessions |

bf16 weights + how to swap the `UNETLoader`: [[05 TRELLIS.2 Model Weights#Switching to bf16 (≥ 24 GB cards)]].
Quality-vs-time is roughly linear in steps, ~cubic in `target_resolution` —
a 1024 draft pass + 1536 hero pass is the efficient studio pattern.

Related: [[14 Troubleshooting Field Guide]]
