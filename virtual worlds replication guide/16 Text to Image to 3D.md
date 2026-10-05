---
tags: [replication, comfyui, text2img, extension]
---
# Text to Image to 3D (Extension Track)

The core path is *photo → GLB* ([[06 Your First 3D Model (GUI)]]). This
extension replaces the camera: **SDXL generates the input image from text**,
and the generated picture goes into the exact same TRELLIS.2 pipeline.

Why this is better than it sounds: TRELLIS.2 wants single objects on plain
backgrounds with even light — which is *literally promptable*. No camera, no
desk, no occlusions; the AI photographer never shoots a crooked frame.

> [!note] Prerequisite
> `sd_xl_base_1.0.safetensors` (6.94 GB) from the master download block:
> [[05 TRELLIS.2 Model Weights#The files (reference — sizes match the block above)]],
> tier *TEXT→IMAGE*. Node explanations:
> [[00 Text2Image Node Map|the Text2Image node map]].

## The pattern: two queues (12 GB-safe, the course default)

SDXL (~6 GB) and TRELLIS (5.25 GB UNet + decodes) can technically share a run
even here — see the chained experiment below, it *passes* — but as a learning
pipeline **two queue jobs** beat one graph: each half can be inspected,
re-rolled (new seed = new photo), and retried independently, and the file
system is the wire. That's the course default; the one-Queue version is a
convenience layer on top.

### Queue 1 — text → image
[[attachments/text2img_sdxl_api.json]] (GUI equivalent below):

```bash
# submit (fish: type bash first, or translate the curl — it's shell-agnostic)
curl -s -X POST http://127.0.0.1:8188/prompt \
  -H 'Content-Type: application/json' -d @text2img_sdxl.json
# result lands here:
ls ~/comfyui/ComfyUI/output/VWML_text2img_*.png
```

### The wire — one copy (LoadImage only browses `input/`)
```bash
cp ~/comfyui/ComfyUI/output/VWML_text2img_00001_.png ~/comfyui/ComfyUI/input/
```

### Queue 2 — image → GLB (unchanged core pipeline)
Take `attachments/trellis2_api_workflow_shape_only.json`, set node 1's `image`
to `VWML_text2img_00001_.png`, submit — or in the GUI: open the TRELLIS.2
template, pick the png from LoadImage's dropdown, `Switch to Trellis2 = true`,
Queue. On 12 GB the geometry-only rule applies ([[08 VRAM Playbook (12 GB and under)]]).

### GUI-only version
No JSONs needed: **Browse → “SDXL Text to Image” template** (ships in the
template pack) → write prompt → Queue → right-click the result → *Save*; drop
it into `input/` (or drag onto the LoadImage node, which auto-copies) → the
TRELLIS.2 template as always. Two templates, one object, zero terminal.

## The 3D-friendly prompt kit (what makes TRELLIS.2 happy)

The image prompt IS the 3D brief. Recipe that verified on the course laptop:

```
POSITIVE  a vintage brass desk lamp, studio product shot, centered
          composition, plain pure white background, even soft lighting,
          single object, no shadows, photorealistic, sharp focus
NEGATIVE  multiple objects, text, watermark, logo, shadow on background,
          scenery, room, hands, cropped, out of frame, blurry, low quality
```

Template = `<object>, studio product shot, plain white background, single
object, no shadows, photorealistic`. Swap only the object.

**Verified object roster (2026-10-04 batch, seeds 111/222/333, full
text→image→textured-vertexcolor GLB pass):** `a classic green glass banker's
desk lamp with brass base` (1.0M tris, 818k colors), `a rustic wooden chair`
(877k tris, 626k colors), `a red ceramic teapot with black handle` (2.2M tris,
1.8M colors — SDXL drew two tiny black artifact spikes near the lid which the
3D dutifully reproduced: *look at the PNG before converting it*).

The verified output of the exact prompt above (SDXL base, seed 20261004, 28
steps — became `VWML_lamp_from_text_00001_.glb` 20 s later):

![Text→image→3D example: SDXL-generated brass lamp, TRELLIS.2 shape-only GLB](attachments/text2img_lamp_example.png)

**Known traps — prevent them in the prompt, not in the 3D settings**
(our verified lamp shot avoided all four; each fix is one negative-prompt term):

| What SDXL did | What TRELLIS.2 made of it |
|---|---|
| painted a contact shadow under the object | a fused pedestal/disc under the mesh |
| two mugs when prompted “coffee mug set” | one welded blob-mug |
| object cropped by frame edge | extrapolated half-object |
| busy room background | BiRefNet cutout errors → floating geometry shards |

Settings worth knowing (all in
[[00 Text2Image Node Map]] and its node notes): fixed
`seed` for reproducible teaching runs, 1024² is SDXL's native canvas, cfg 6.5.

## The single chained graph (one Queue, text → GLB) — measured truth

`attachments/text2img_to_trellis_chained.json` wires SDXL's `VAEDecode`
straight into BiRefNet → the full TRELLIS shape chain (no LoadImage at all).

**On the 12 GB course laptop with baseline flags:** **it passes** — measured
2026-10-04: one Queue, ~30 s, PNG *and* GLB produced (same seed → the same lamp reappears). The predicted “both UNets resident → OOM” wall never
materialized, and the reason is the launch flags themselves: `--lowvram` keeps
weights in system RAM (this machine has 32 GB) and streams them per-layer, so
two models coexist happily — the extra cost is RAM footprint and streaming
time, not VRAM. What breaks the chained graph is NOT small VRAM; it would be
the *textured* bake stage (same wall as always, note 08).
**On ≥24 GB cards:** one queue end-to-end, no flags needed — the wire is a
tensor instead of a file.

## Big-GPU upgrades (opt-in, like the 3D side)

| Model | Size | VRAM peak | Notes |
|---|---|---|---|
| SDXL base *(verified here)* | 6.94 GB | ~6 GB @1024² | course default |
| SD3.5 Medium | ~5 GB + 5 GB T5 | ~10 GB | better prompt-following; `Comfy-Org/stable-diffusion-3.5-fp8` |
| FLUX.1-schnell fp8 | ~12 GB | ~11 GB+ | best structure fidelity; document-only on the course machine |

## Verify
```bash
ls -la ~/comfyui/ComfyUI/output/3d/        # the GLB from Queue 2
```
Verified end-to-end on the course laptop (2026-10-04, all baseline flags,
prompt = brass desk lamp from the kit above):
- `output/VWML_text2img_00001_.png` — 10 s
- `output/3d/VWML_lamp_from_text_00001_.glb` — 16.0 MB, valid glTF v2, 20 s (two-queue)
- `output/3d/VWML_chained_test_00001_.glb` — 15.0 MB, valid glTF v2, ~30 s (chained, one queue)

Text → lamp → GLB in under a minute of GPU time. The camera is officially optional.

Prev track: [[15 Verification Checklist]] completed · Back: [[00 Start Here]]
