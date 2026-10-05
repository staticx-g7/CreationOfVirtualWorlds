---
tags: [node, template, diffusion]
---
# KSampler ×4 — the heart of the template

**What they are:** the template runs the **same loaded UNet through four
sampler passes**, each refining a different representation. Understanding this
chain is 80 % of understanding the template:

```
⑥ structure  →  ⑦ shape  →  [upsample ⑦]  →  [texture ⑦]
  12 steps       20 steps      12 steps         12 steps
  cfg 7.5        cfg 7.5       cfg 7.5          cfg 1.0   ← different on purpose
  seed 42        seed 42       seed 42          seed 43
  euler/normal   euler/normal  euler/simple     euler/normal
```

(⑥/⑦ = node ids in the API JSONs of this vault,
[[attachments/trellis2_api_workflow_1024_full.json]])

**Widgets, and what moving them does**

| Widget | Template default | Turning it does |
|---|---|---|
| `seed` | 42, 42, 42, **43** | the shape roulette. Structure+shape+upsample **share 42** = the passes stay coherent; texture uses **43** = texture variety independent of shape. *Fixed* = reproducible (needed for teaching/checklist); *randomize* = new design. Change one seed → related stage changes |
| `steps` | 12 / 20 / 12 / 12 | quality↔time, **linear**. Shape sampler (20) has the biggest payoff — it defines the geometry. Structure at 12 is already decisive; texture at 12 is plenty. 30+ = diminishing, on laptops painful |
| `cfg` | 7.5×3, **1.0 texture** | guidance strength: how hard the sampler obeys the image conditioning. Shape passes: 5 = dreamy/reinterprets, 7.5 = sweet spot, 10+ = overcooked contrast. **Texture is 1.0 on purpose** — texture diffusion is guidance-free; raising it bakes in blotchy over-saturation |
| `sampler_name` | `euler` (all) | integrator. Euler is what the model was validated with; `dpmpp_2m`+`karras` *can* work with fewer steps but changes the look — experiment only on ≥24 GB rigs |
| `scheduler` | `normal`, upsample pass = **`simple`** | noise-schedule shape. The upsample pass uses `simple` because it continues an existing latent, not noise-from-scratch. Leave all four as shipped |
| `denoise` | 1.0 (all) | <1.0 = “start from existing latent, change only this much”. All 1.0 = full generation. `denoise ~0.4` on the *shape* sampler against a saved latent = img2img-style refine — advanced, needs the API graph ([[07 Headless Generation and the API]]) |

**The practical dial set:** seed (free) → shape-pass `steps` (linear time) →
`cfg` if the result ignores your photo. That's the whole tuning loop.

**VRAM:** sampler VRAM scales with the *representation* being sampled (set by
[[08 Trellis2 Stages and VaeDecodes]]), not with steps. More steps = longer,
never heavier.

Prev: [[06 EmptyTrellis2LatentStructure]] · Next: [[08 Trellis2 Stages and VaeDecodes]]
