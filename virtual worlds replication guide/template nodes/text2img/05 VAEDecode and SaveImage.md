---
tags: [node, text2img]
---
# 05 VAEDecode and SaveImage — pixels out

**What they are:** the exit doors of the first half. `VAEDecode` converts the
finished latent into actual pixels using the checkpoint's VAE (output `2`,
see [[01 CheckpointLoaderSimple]]); `SaveImage` writes the PNG — with two
course-critical behaviors hiding in plain sight.

**Widgets**

| Node · Widget | Shipped default | Turning it does |
|---|---|---|
| `VAEDecode` | *no widgets* | latent → image; ~1 s. (Swapping in other VAE files is an SD1.5-era habit — the stock SDXL VAE is right.) |
| `SaveImage · filename_prefix` | `VWML_text2img` | → `output/VWML_text2img_00001_.png` (auto-incremented; prefix doubles as subfolder, same convention as the 3D export [[13 Export MeshToFile3D and SaveGLB]]) |

> [!warning] The `input/` gotcha (bites every first run)
> TRELLIS's `LoadImage` node browses **only `models/../input/`** — output
> PNGs are *invisible* to it until copied:
> `cp ~/comfyui/ComfyUI/output/VWML_text2img_*.png ~/comfyui/ComfyUI/input/`
> (GUI shortcut: dragging a PNG onto the canvas auto-copies it into `input/`.)

> [!tip] The PNG *is* the workflow
> ComfyUI embeds the full graph + prompts into every saved PNG — drag
> `VWML_text2img_00001_.png` onto the canvas and the whole text→image graph
> reloads, prompt included. This is also why “identical” renders can hash
> differently: the pixels match, the embedded JSON doesn't. Course habit:
> good prefixes name the *run*, since the PNG is self-documenting.

Prev: [[04 KSampler]] · Downstream: [[00 Node Map]] (TRELLIS half) · Back: [[00 Text2Image Node Map]]
