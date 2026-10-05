---
tags: [node, text2img]
---
# 04 KSampler (text2img preset)

**What it is:** *the same node class* the 3D half runs four times
([[07 KSampler x4]]) — same widgets, different sweet spots, because SDXL is a
2D image model. All widget semantics carry over; only the shipped values differ:

| Widget | Text→Image default | (3D half uses) | Notes |
|---|---|---|---|
| `seed` | fixed (e.g. 20261004) | 42×3 + 43 | identical meaning — same seed + same prompt ⇒ same image (determinism is real; the vault's two lamp PNGs were pixel-identical renders, differing only in embedded workflow metadata — see [[05 VAEDecode and SaveImage]]) |
| `steps` | **28** | 12/20/12 | 20 = fine drafts, 28 = sweet spot, 40+ = wasted minutes on SDXL |
| `cfg` | **6.5** | 7.5 (1.0 texture) | prompt adherence; 7 typical; ≥8 burns in oversaturation/plastic look |
| `sampler_name` | **`dpmpp_2m`** | `euler` | dpmpp_2m is the SDXL community standard |
| `scheduler` | **`karras`** | `normal` | karras noise schedule pairs with dpmpp_2m; the 3D model wants its trained `normal` |
| `denoise` | 1.0 | 1.0 | <1.0 here = img2img — pair with a loaded image, the classic photo-restyle trick |

**Symptom → dial:** washed-out, ignores prompt → cfg ↑ (to 7.5) · plastic/oversaturated → cfg ↓ · muddy at 28 steps → wrong resolution ([[03 EmptyLatentImage]]) · wants variation, same subject → keep prompt, randomize `seed`.

**VRAM/time:** the ~6 GB peak / ~10 s measured on the course laptop lives
right here; steps scale linearly, pixels (note 03) scale ~quadratically.

Prev: [[03 EmptyLatentImage]] · Next: [[05 VAEDecode and SaveImage]]
