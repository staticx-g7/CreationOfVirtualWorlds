---
tags: [node, template, input]
---
# RemoveBackground (+ LoadBackgroundRemovalModel)

**What it is:** two nodes doing one job — cut the object out with an AI matting
model (BiRefNet) so the 3D generator only ever sees the silhouette. The loader
picks *which* matting model; the removal node applies it.

**Widgets**

| Node · Widget | Template default | Turning it does |
|---|---|---|
| `LoadBackgroundRemovalModel · bg_removal_name` | `birefnet.safetensors` | only interesting option = swap matting model (BiRefNet is the strong one; you need the file in `models/background_removal/` — [[05 TRELLIS.2 Model Weights]]) |
| `RemoveBackground` | *no widgets* | runs matting → outputs image + alpha mask |

**Failure modes you'll actually see**
- **Eats part of the object** (dark object on dark bg, fur, transparent glass)
  → fix the photo, or raise `grow_mask` one step in [[03 ImageCropToMask]]
- **Leaves background chunks** → they get reconstructed as floating geometry —
  annoying in UE, trivially fixed by re-shooting
- Matting runs **once per prompt, ~2 s, negligible VRAM** — never a bottleneck

The mask it produces is what the cropping node and the conditioning both use,
so quality here propagates everywhere.

Prev: [[01 LoadImage]] · Next: [[03 ImageCropToMask]]
