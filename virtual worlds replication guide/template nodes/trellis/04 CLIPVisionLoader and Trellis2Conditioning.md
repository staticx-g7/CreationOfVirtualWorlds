---
tags: [node, template, conditioning]
---
# CLIPVisionLoader + Trellis2Conditioning

**What they are:** the vision encoder (DINOv3 ViT-L) that *looks* at your
cropped image, and the node that packages what it saw as **conditioning** — the
guidance signal every sampler downstream will follow.

**Widgets**

| Node · Widget | Template default | Turning it does |
|---|---|---|
| `CLIPVisionLoader · clip_name` | `dino_v3_L_naf_fp32.safetensors` | swap vision encoder. This is **DINOv3, not CLIP** despite the node name (name is legacy). No reason to change — every TRELLIS.2/Pixal3D file expects it |
| `Trellis2Conditioning` | *no widgets* | encodes image+mask → positive/negative conditioning pair |

> [!info] This node is the “missing model” badge
> When the GUI says a model is missing *before you queue anything*, it's a
> loader complaining (this one, `UNETLoader`, `VAELoader`, the removal loader).
> Fix = drop the file in `models/…` per [[05 TRELLIS.2 Model Weights]] — the
> server finds new files on refresh, no restart needed.

**VRAM/time:** encoder runs once per prompt (~1 s, ~1 GiB transient). Never the
bottleneck, never a dial worth touching.

Prev: [[03 ImageCropToMask]] · Next: [[05 UNETLoader]]
