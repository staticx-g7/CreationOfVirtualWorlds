---
tags: [node, text2img]
---
# 01 CheckpointLoaderSimple

**What it is:** the SDXL equivalent of TRELLIS's loader trio combined —
**one checkpoint file = image model + both text encoders + the VAE**, exposed
as three outputs. That's the big conceptual difference from the 3D half, which
loads UNet / VAEs / CLIP-vision separately ([[05 UNETLoader]]).

**Widgets**

| Widget | Shipped default | Turning it does |
|---|---|---|
| `ckpt_name` | `sd_xl_base_1.0.safetensors` (6.94 GB, `stabilityai` repo — link in [[05 TRELLIS.2 Model Weights#The files (reference — sizes match the block above)]]) | any SDXL-family checkpoint (refiner, fine-tunes like Juggernaut…) — file goes to `models/checkpoints/`, GUI picks it up on refresh |

**Output sockets — memorize the order, it's the wiring:**
- `0 MODEL` → KSampler's `model`
- `1 CLIP` → **both** CLIPTextEncodes ([[02 CLIPTextEncode x2]])
- `2 VAE` → VAEDecode ([[05 VAEDecode and SaveImage]])

**VRAM/time:** load once per session (fast when the file is page-cached —
our first-ever run measured 10 s *including* the load on this machine).
Residency is streamed from RAM under the course launch flags, same as the 3D
half ([[16 Text to Image to 3D#The single chained graph (one Queue, text → GLB) — measured truth]]).

Prev: [[00 Text2Image Node Map]] · Next: [[02 CLIPTextEncode x2]]
