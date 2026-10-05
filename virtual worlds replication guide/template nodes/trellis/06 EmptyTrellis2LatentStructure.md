---
tags: [node, template, model]
---
# EmptyTrellis2LatentStructure

**What it is:** seeds the generation — creates the empty *latent structure* the
first sampler will fill. Think “blank canvas”, except the canvas itself is a
learned 3D-ish representation, and its shape/size constrains everything.

**Widgets**

| Widget | Template default | Turning it does |
|---|---|---|
| `batch_size` | 1 | **N models per prompt.** Every stage downstream runs ×N and VRAM is ×N (not “+a bit”). 2 on a 12 GB card = dead. 4 is a 48 GB+ party trick — but at scale it's the *efficient* way to get variety from one photo (one model load, N results) |

**Why anyone touches it:** A/B testing seeds without re-queueing — batch 4 with
seeds fixed gives four candidate shapes in one run. On big GPUs this is how you
build the course's “20 assets” sets fast. On 12 GB: keep **1**, always.

**VRAM/time:** linear multiplier on the entire pipeline.

Prev: [[05 UNETLoader]] · Next: [[07 KSampler x4]]
