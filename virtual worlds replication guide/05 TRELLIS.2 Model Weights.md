---
tags: [replication, comfyui, models]
---
# TRELLIS.2 Model Weights

The exact set that drives the official *Pixal3D & TRELLIS.2: Image to Model*
template (min ComfyUI **0.34.0**). File list + links verified live against
HuggingFace on 2026-10-04. The HF repos mirror the `models/` folder layout,
so every file downloads straight into place.

> [!tip] The GUI can fetch these too
> Opening the template ([[06 Your First 3D Model (GUI)]]) shows a **Download**
> button per missing model. The block below is the headless/scriptable
> equivalent (and fetches everything, including what the template doesn't list).

## Download — everything in one block
Runs in bash, zsh, **fish** (no shell variables); `-C -` resumes interrupted
downloads. **Skip lines by tier** — the comments mark what you need:
required = every machine · optional = OOM fallbacks (+12 GB) · big-VRAM = ≥24 GB cards.

```bash
cd ~/comfyui/ComfyUI/models

# ── REQUIRED (TRELLIS.2 path, 8.9 GB) ──────────────────────────────
curl -L -C - -o diffusion_models/trellis_2_int8_convrot.safetensors \
  "https://huggingface.co/Comfy-Org/TRELLIS.2/resolve/main/diffusion_models/trellis_2_int8_convrot.safetensors"
curl -L -C - -o vae/trellis_2_shape_vae_bf16.safetensors \
  "https://huggingface.co/Comfy-Org/TRELLIS.2/resolve/main/vae/trellis_2_shape_vae_bf16.safetensors"
curl -L -C - -o vae/trellis_2_texture_vae_bf16.safetensors \
  "https://huggingface.co/Comfy-Org/TRELLIS.2/resolve/main/vae/trellis_2_texture_vae_bf16.safetensors"
curl -L -C - -o clip_vision/dino_v3_L_naf_fp32.safetensors \
  "https://huggingface.co/Comfy-Org/Pixal3D/resolve/main/clip_vision/dino_v3_L_naf_fp32.safetensors"
curl -L -C - -o background_removal/birefnet.safetensors \
  "https://huggingface.co/Comfy-Org/BiRefNet/resolve/main/background_removal/birefnet.safetensors"

# ── OPTIONAL (fallback ladder, +13.6 GB — see note 08) ─────────────
curl -L -C - -o diffusion_models/pixal3d_int8_convrot.safetensors \
  "https://huggingface.co/Comfy-Org/Pixal3D/resolve/main/diffusion_models/pixal3d_int8_convrot.safetensors"
curl -L -C - -o geometry_estimation/moge_2_vitl_normal_fp16.safetensors \
  "https://huggingface.co/Comfy-Org/MoGe/resolve/main/geometry_estimation/moge_2_vitl_normal_fp16.safetensors"
curl -L -C - -o checkpoints/hunyuan_3d_v2.1.safetensors \
  "https://huggingface.co/Comfy-Org/hunyuan3D_2.1_repackaged/resolve/main/hunyuan_3d_v2.1.safetensors"

# ── BIG VRAM ≥24 GB (full-precision, +10.3 GB) ─────────────────────
curl -L -C - -o diffusion_models/trellis_2_bf16.safetensors \
  "https://huggingface.co/Comfy-Org/TRELLIS.2/resolve/main/diffusion_models/trellis_2_bf16.safetensors"

# ── TEXT→IMAGE FRONTEND (optional, +6.9 GB — note 16) ──────────────
curl -L -C - -o checkpoints/sd_xl_base_1.0.safetensors \
  "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"
```

⚠ Repos to copy exactly: `TRELLIS.2` is **with a dot** (`TRELLIS_2` 404s — bit
us) and `hunyuan3D_2.1_repackaged` keeps its lowercase h + underscore + dot.

## The files (reference — sizes match the block above)

| Tier | File → `models/<this path>` | Size | Role |
|---|---|---|---|
| required | `diffusion_models/trellis_2_int8_convrot.safetensors` | 5.25 GB | TRELLIS.2 main model (low-VRAM quant — what the course ships) |
| required | `vae/trellis_2_shape_vae_bf16.safetensors` | 1.10 GB | shape latent codec |
| required | `vae/trellis_2_texture_vae_bf16.safetensors` | 0.95 GB | texture latent codec |
| required | `clip_vision/dino_v3_L_naf_fp32.safetensors` | 1.22 GB | image encoder (shared by both template branches) |
| required | `background_removal/birefnet.safetensors` | 0.44 GB | background removal |
| optional | `diffusion_models/pixal3d_int8_convrot.safetensors` | 5.58 GB | same-template alternative model (`Switch to Trellis2 = false`) |
| optional | `geometry_estimation/moge_2_vitl_normal_fp16.safetensors` | 0.66 GB | Pixal3D camera branch |
| optional | `checkpoints/hunyuan_3d_v2.1.safetensors` | 7.37 GB | last-resort 3D model (native nodes) |
| big-VRAM | `diffusion_models/trellis_2_bf16.safetensors` | 10.34 GB | full-precision UNet (Ampere+; fp16-family) |
| text2img | `checkpoints/sd_xl_base_1.0.safetensors` | 6.94 GB | generates the *input image* from text — [[16 Text to Image to 3D]] (note: official `stabilityai` repo, not Comfy-Org) |

> [!info] Template “missing models” badge
> The official template bundles **both** model paths, so its checker also wants
> `pixal3d_int8_convrot` + `moge_2_vitl_normal_fp16` even for pure-TRELLIS.2
> use. With `Switch to Trellis2 = true` the Pixal3D branch never executes —
> downloading the two optional files is recommended (fallbacks), not required.

## Switching to bf16 (≥ 24 GB cards)
In the GUI template (or any API JSON, e.g.
[[attachments/trellis2_api_workflow_1024_full.json]]) set the `UNETLoader`
node's `unet_name` to `trellis_2_bf16.safetensors`, leave `weight_dtype` on
`default` (keeps native bf16). Keep int8 too — swap back for bake-heavy
sessions if you feel tight. Then raise quality via
[[08 VRAM Playbook (12 GB and under)#≥ 24 GB: the quality ladder (estimates)]].
**Course policy:** the image ships int8 (fits every student laptop, one asset
pack for all); bf16 is opt-in — same workflows, one dropdown change.

## Verify (sizes must match the table)
```bash
du -sh ~/comfyui/ComfyUI/models/* | sort -rh
ls -la ~/comfyui/ComfyUI/models/diffusion_models/   # expect the 5.25 GB file
```

Next: [[06 Your First 3D Model (GUI)]]
