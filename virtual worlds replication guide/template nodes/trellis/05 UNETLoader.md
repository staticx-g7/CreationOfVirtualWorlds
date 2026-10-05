---
tags: [node, template, model]
---
# UNETLoader

**What it is:** loads the **main generative model** (the diffusion UNet — here a
flow-matching DiT, node name is legacy) that all four samplers share. One file,
one dropdown — and that dropdown is *the* VRAM quality switch of the template.

**Widgets**

| Widget | Template default | Turning it does |
|---|---|---|
| `unet_name` | `trellis_2_int8_convrot.safetensors` (5.25 GB) | **the big dial:** `trellis_2_bf16.safetensors` (10.34 GB) = full precision, finer gradients/thin geometry, needs ≥24 GB comfortable. `pixal3d_int8_convrot` = the other template branch |
| `weight_dtype` | `default` | `default` = keep the file's native precision (int8 stays int8, bf16 stays bf16). `force fp32` = 2× VRAM for zero visible gain on these files — never |

**The trade in one line (measured on 12 GB):** int8 = the *only* variant that
fits a 12 GB laptop doing geometry; bf16 is a ≥24 GB conversation — see
[[05 TRELLIS.2 Model Weights#Switching to bf16 (≥ 24 GB cards)]] and the ladder
in [[08 VRAM Playbook (12 GB and under)#≥ 24 GB: the quality ladder (estimates)]].

Quality difference int8→bf16: subtle. VRAM difference: double. Course ships int8.

**VRAM:** resident while the session runs (`--disable-smart-memory` keeps it
loaded — that's our 12 GB flag combo trading RAM round-trips for predictability).

Prev: [[04 CLIPVisionLoader and Trellis2Conditioning]] · Next: [[06 EmptyTrellis2LatentStructure]]
