---
tags: [node, template, texture]
---
# BakeTextureFromVoxel — the node that ate 12 GB

**What it is:** converts the *voxel texture* the diffusion produced into a
classic UV-mapped texture image for the mesh. Conceptually a “render to UV”.
In practice: **the single most VRAM-hungry node in the template, and the reason
the course ships geometry-only on laptops.**

**Widgets**

| Widget | Template default | Turning it does |
|---|---|---|
| `texture_size` | 1024 | nominal output texture resolution (512/1024/2048/4096). **On small cards this dial is a liar:** measured, the bake cost ≈ **4–10 GiB regardless of the value** — we ran `texture_size: 512` and it asked for *more* (~7–10 GiB) than the 1024 run. Whatever it does internally (dense voxel sampling, UV raster buffers), it doesn't scale with the number you set |

**Measured record (our 7 runs, 12 GB card, server flags as in note 03):**
- bake @1024 → `torch.OutOfMemoryError`, wanted 4.3 GiB with the rest loaded
- bake @512 (control experiment!) → OOM at the same node, different amount
- same graphs **without** this node (geometry-only) → ✅ complete, 164 MB GLB
→ conclusion: bake needs roughly ≥16 GB with everything else resident; there
is **no setting of this node that saves a 12 GB card**. But "textured" has more
than one definition — see the vertex-color route below before reaching for
Blender ([[10 Create the Demo Project]] track).

## The 12 GB workaround: skip bake, paint vertices (`PaintMesh`)

> [!success] Measured 2026-10-04 (run 9, [[08 VRAM Playbook (12 GB and under)]])
> A **textured** GLB *does* fit on 12 GB — if you skip UV space entirely.
> The texture stage and its decode pass fine on 12 GB (that was always the case);
> only the UV *bake* dies. So export the colors where they already are: on the
> voxels → on the **vertices**.
>
> Chain: `Trellis2TextureStage` → `KSampler` (12 steps, **cfg 1.0**, euler/normal
> — template default) → `VaeDecodeTextureTrellis` (needs `trellis_2_texture_vae_bf16`
> + the `SHAPE_SUBDIVIDES` wire from `VaeDecodeShapeTrellis`) → `PaintMesh`
> (`mesh` + `voxel_colors`) → `MeshToFile3D` → `SaveGLB`. No `UnwrapMesh`,
> no bake, no image textures.
>
> Result: 19 MB GLB, **394k vertex colors** (`COLOR_0`), luminance 0.01–0.96,
> no OOM. Ready-made graphs: note 06's File → Open list.
>
> Honest limits: vertex colors only — no PBR maps, detail is capped by vertex
> density (fine at 1024), and UE shows them via the imported vertex-color
> material, not authored textures. For course purposes (recognizable props in
> the city) this is the 12 GB texture answer.

> [!tip] Reading the OOM honestly
> “Tried to allocate X GiB” at this node ≠ your `texture_size` is too big.
> `nvidia-smi` first ([[14 Troubleshooting Field Guide]] — the UE editor
> holding 1.7 GiB looks *exactly* like this failure).

**On ≥24 GB:** this is where the quality ladder's bake column lives — 1024–2048
fine, 4096 on 48 GB ([[08 VRAM Playbook (12 GB and under)#≥ 24 GB: the quality ladder (estimates)]]).

Prev: [[08 Trellis2 Stages and VaeDecodes]] · Next: [[10 DecimateMesh]]
