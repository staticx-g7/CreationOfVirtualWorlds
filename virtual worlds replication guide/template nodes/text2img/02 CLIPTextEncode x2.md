---
tags: [node, text2img]
---
# 02 CLIPTextEncode ×2 — the prompt

**What they are:** the two text encoders **inside the SDXL checkpoint**
(OpenCLIP-bigG writes the main semantics, CLIP-ViT-L provides a short
“pooled summary” the model's style path consumes). The node encodes text
through both at once — which is why one node type appears twice:
**positive** (what you want) and **negative** (what you forbid).
This is the *only* creative control in this half — the prompt kit for
3D-friendly images lives in [[16 Text to Image to 3D#The 3D-friendly prompt kit (what makes TRELLIS.2 happy)]].

**Widgets**

| Widget | Shipped default | Turning it does |
|---|---|---|
| `text` (positive) | the verified lamp prompt | everything: subject, framing, background, lighting — phrase the *image the 3D half needs*, not the mood poster |
| `text` (negative) | “multiple objects, text, watermark, shadow on background, …” | suppression list; for 3D inputs its whole job is protecting BiRefNet's cutout and TRELLIS's inference |

**Gotchas & facts**
- Name collision alert: this CLIP is the **text** encoder baked into the
  checkpoint — unrelated to `CLIPVisionLoader`'s DINOv3 **image** encoder
  ([[04 CLIPVisionLoader and Trellis2Conditioning]]). Same letters, different models.
- The official “SDXL prompt and style” template adds a *third* encode —
  a short style prompt feeding the negative node's optional `conditioning`
  input. Optional garnish: our verified minimal graph omits it and produced
  the example lamp fine.
- Negatives are weak guidance: “no building” often *adds* a building
  (SDXL is bad at negation semantics — describe the desired absence instead,
  e.g. negative `people, cars` works, positive `empty street` works better).

**VRAM/time:** ~2 s, transient. Never the problem.

Prev: [[01 CheckpointLoaderSimple]] · Next: [[03 EmptyLatentImage]]
