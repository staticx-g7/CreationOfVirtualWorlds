---
tags: [replication, comfyui, trellis]
---

The course-defining moment: **one image → textured, game-ready GLB**. On the
12 GB course machine a full 1024³ run takes **6–12 minutes**.

## Basics first: ComfyUI in 10 minutes
*New to ComfyUI? Read this before clicking anything — it's the whole mental
model plus where everything lives.*

**The one idea:** a workflow is a **visible Python script**. Each node = one
function, wires = arguments, **Queue = Run**. Nothing hits the GPU until you
queue. Wire/socket colors are Python types (`IMAGE`, `MODEL`, `LATENT`,
`CONDITIONING`, `VAE`, `MESH`…) — sockets refuse to connect on type mismatch,
and that's your best debugging clue.

**Interface map (frontend 1.5x):**

| Where | What |
|---|---|
| Top bar **`+`** | new tab + **“Browse all workflows” → Templates tab** = official model zoo (TRELLIS.2 lives here; that's step 2.2 below) |
| Top bar **Workflow menu** | Save / Open / Export (API format); saved graphs land in `ComfyUI/user/default/workflows/` |
| Top bar **▶ Queue Prompt** | runs the graph (number = jobs queued); **Interrupt** stops |
| Left icon dock | 📁 workflows · 📦 **model library** (lists detected model files, offers downloads) · 🧩 node palette · ⚙ settings |
| Bottom-right queue panel | progress + the running node highlights on canvas — tells you *which stage* you're in |

**Canvas gestures** (10-min muscle memory): middle-drag pan · scroll zoom ·
double-click empty = **node search** · drag socket-to-socket to wire ·
`Ctrl+Z` undo · `Ctrl+M` mute / `Ctrl+B` bypass · `F` fit view · right-click = menu.

**Where models live** — all models are *files* under `~/comfyui/ComfyUI/models/`
and node dropdowns list those files **after a refresh** (browser reload / `R`):

| Folder | Holds | Course file |
|---|---|---|
| `diffusion_models/` | the big learned model (“checkpoint”/UNet) | `trellis_2_int8_convrot.safetensors` |
| `vae/` | latent ↔ data codecs | `trellis_2_shape_vae_bf16`, `…_texture_vae_bf16` |
| `clip_vision/` | the model's *eyes* (image encoder) | `dino_v3_L_naf_fp32.safetensors` |
| `background_removal/` | rembg nets | `birefnet.safetensors` |
| `geometry_estimation/` | camera/geometry nets (Pixal3D only) | `moge_2_vitl_normal_fp16` |
| `input/` · `output/` | your uploads · results (`output/3d/*.glb` here) | — |

Two rules that prevent 80 % of beginner errors:
**① wrong folder = invisible file** (HF repos in [[05 TRELLIS.2 Model Weights]]
mirror this layout — download straight in). **② a loader shows a *filename*,
not an “installed” flag** — when in doubt `ls` the folder, never trust the
dropdown alone.

**Words you'll hear:** *template* = built-in example workflow · *latent* =
compressed working space VAEs encode into/out of · *KSampler* = the actual
generation loop (*steps* = quality↔time, *CFG* = how strongly it obeys
conditioning, *seed* = randomness; same seed + same graph = same model) ·
*core vs custom node* = shipped vs community (this course: **100 % core**).

## 0. Pre-flight VRAM ritual (12 GB cards — non-negotiable)
- [ ] **Close the Unreal Editor** (it silently holds ~1.7 GB — this cost us
      three failed runs before we found it: [[14 Troubleshooting Field Guide#3. The invisible 1.7 GB thief]])
- [ ] Close browser tabs / Chrome GPU apps / games
- [ ] `nvidia-smi` → near-zero usage before starting ComfyUI
- [ ] Server started with the flags from [[03 Install ComfyUI (Linux)#3. Launch — with the 12 GB flags from day one]]

## 1. Input image rules (make or break)
- **ONE object** filling ~70 % of frame, plain background, soft light
- Real photos OK; clean renders even better (we used a rendered stylized house)
- Multi-object scenes / text / busy backgrounds → blobby garbage mesh.
  **Demo this failure on purpose in class** — it teaches the model's contract.

Put your image anywhere; you'll upload it in the UI (it lands in `ComfyUI/input/`).

## 2. Load the official template
1. Server running (or double-click the Desktop launcher) → http://127.0.0.1:8188
2. **Workflow → Browse templates → category “3D”** (or press `+` → templates)
3. Open **“Pixal3D & TRELLIS.2: Image to Model”** (~66 nodes — first time
   loading takes a few seconds; the template pack ships with ComfyUI 0.34+)
4. If it offers to download models you skipped in [[05 TRELLIS.2 Model Weights]] — let it.
   > [!info] “2 models missing” after you downloaded the required five? NORMAL.
   > This template contains **both** model paths, so its checker also wants the
   > Pixal3D branch's `pixal3d_int8_convrot` + `moge_2_vitl_normal_fp16`
   > (note 05's optional table). With `Switch to Trellis2 = true` the Pixal3D
   > branch never executes — downloading them is optional (but recommended:
   > they're the course's OOM-fallback ladder, and the GUI button is one click).
5. Set the **`Switch to Trellis2`** boolean to **true** (false = Pixal3D path)
6. **≤12 GB machines — three checks before you ever press Queue** (all measured,
   run 8 in [[08 VRAM Playbook (12 GB and under)]]):
   - `Switch to Trellis2` = **true** — the template **ships `false`** (Pixal3D), which is heavier and hits the same walls
   - `Trellis2UpsampleStage` node → `target_resolution` = **1024** — the template **ships 1536**, which OOMs in `VaeDecodeShapeTrellis` after you've already burned minutes of sampling
   - **close the UE Editor** — our passing 1024 runs peak at ~11.1 of 11.7 GiB; any neighbor eating VRAM turns success into OOM
   And accept the physics: even with all three, this *full* template still dies at
   the texture bake on 12 GB. For a GLB from this machine skip the template entirely —
   **File → Open** one of two pre-fixed, GUI-ready graphs (all traps removed:
   Trellis2 branch hard-wired, no upsample stage = 1024 decode, no UV bake):
   - `[[attachments/trellis2_gui_vertexcolor_12gb.json]]` — **textured**: it samples a
     texture stage and paints the colors onto vertices (`PaintMesh` → `COLOR_0`)
     instead of UV-baking — that's the 12 GB trick that dodges the bake wall
     (run 9 in [[08 VRAM Playbook (12 GB and under)]]). Verified 2026-10-04: 19 MB
     GLB, 394k vertex colors, luminance 0.01–0.96.
   - `[[attachments/trellis2_gui_shape_only_12gb.json]]` — geometry only: half the
     runtime and file size.
   Either way: pick your image on its `Load Image` node, press Queue, done.
   **Single objects with clean silhouettes** are the sweet spot — TRELLIS.2 is an
   object model, busy scenes come out sludgy regardless of settings.
   (API-format twins for note 07: `[[attachments/trellis2_api_workflow_shape_only.json]]`
   and `[[attachments/trellis2_api_workflow_vertexcolor_12gb.json]]`.)

## 3. Swap in your image and queue
1. On the `Load Image` node → *upload* your object photo
   (no photo handy? Generate one with SDXL — extension track: [[16 Text to Image to 3D]])
2. Leave the defaults for a first run **except the three 12 GB checks from
   step 6 above** (switch · upsample 1024 · UE closed). Model-file defaults are fine.
   > [!tip] What does every dial on this graph do?
   > The template's nodes are explained one by one — every widget, its shipped
   > default, and what turning it gets you — in
   > [[template nodes/00 Node Map|the Node Map]] (start there; one note per node).
3. **Queue** (the ▶ button). Watch progress per-stage in the queue panel.
4. Done = the `Preview3D` node shows your model spinning; `Save3DAdvanced`
   writes `ComfyUI/output/3d/*.glb`

## 4. Sanity-check the result
```bash
ls -la ~/comfyui/ComfyUI/output/3d/       # expect a .glb of a few MB
```
Open it in Blender / https://gltf-viewer.donmccurdy.com / Windows 3D Viewer.

> [!failure] If it OOMs (red toast, `torch.OutOfMemoryError` in the log)
> Go to [[08 VRAM Playbook (12 GB and under)]] — it is a decision tree, in
> order, with the exact flag to add at each step. Do not randomly lower
> settings; the upsample stage has a hard floor and won't cooperate.
> **Heads-up for 12 GB cards:** the *textured* template path (UV bake stage)
> needs ≳ 16 GB no matter the flags — on 12 GB generate **geometry-only** with
> the shape-only graph and texture afterwards (Blender), or use the fallback
> models. We measured all seven variants so you don't have to.

Next (or skip): [[10 Create the Demo Project]] — get the GLB into Unreal.
Advanced/automation track: [[07 Headless Generation and the API]]
