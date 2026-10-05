---
tags: [node, template, input]
---
# ImageCropToMask

**What it is:** crops/pads the matted image to a fixed square canvas around the
object and composites it onto a flat background color. This framing is literally
what the model thinks the object's world is.

**Widgets**

| Widget | Template default | Turning it does |
|---|---|---|
| `width` / `height` | 1024 / 1024 | canvas size; matches the model's native conditioning resolution — leave it |
| `pad_factor` | 1.0 | 1.0 = tight box around mask. **Raise (1.1–1.3)** for objects shot edge-on/cropped in the photo; lower clips |
| `grow_mask` | 0 | dilates the mask N px before cropping — **raise 5–15 if bg removal shaved fur/thin parts** |
| `background` | `#000000` | fill color behind the object; black is neutral for DINOv3 — don't play with this |

**The dial worth knowing:** `grow_mask` + `pad_factor` together are your answer
to “the model generated a stubbier/boxier thing than my photo” — 90 % of the
time the input silhouette was clipped. Check by looking at the preview of this
node: if the object touches a canvas edge, pad more.

**VRAM/time:** free. Turn freely.

Prev: [[02 RemoveBackground]] · Next: [[04 CLIPVisionLoader and Trellis2Conditioning]]
