---
tags: [node, text2img]
---
# 03 EmptyLatentImage — the canvas

**What it is:** sizes the blank latent canvas. Unlike the 3D half's
[[06 EmptyTrellis2LatentStructure]] (where only batch matters — the *shape* is
the model's business), here width×height **is** a quality dial: SDXL was
trained on a handful of native resolutions and degenerates off them.

**Widgets**

| Widget | Shipped default | Turning it does |
|---|---|---|
| `width` / `height` | 1024 / 1024 | stick to SDXL's trained aspect ladder: `1024²`, `832×1216` (portrait), `1216×832` (landscape), `1344×768`, `1536×640`. 512² = mushy incoherence; off-ladder ARs = doubled/cropped subjects. VRAM & time ≈ ∝ pixels |
| `batch_size` | 1 | N images per queue, VRAM ×N — same rule as the 3D half: 2+ is a big-GPU luxury; on 12 GB re-roll the seed instead |

**For 3D inputs specifically:** 1024² or the portrait rung (buildings!) —
the TRELLIS half crops to 1024² anyway ([[03 ImageCropToMask]]), so extra
pixels beyond that are only for your own cropping freedom.

Prev: [[02 CLIPTextEncode x2]] · Next: [[04 KSampler]]
