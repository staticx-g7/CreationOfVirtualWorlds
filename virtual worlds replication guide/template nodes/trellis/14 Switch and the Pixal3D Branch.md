---
tags: [node, template, branch]
---
# The Switch and the Pixal3D Branch (skim)

**What it is:** the official template is actually **two generation pipelines**
in one file; a boolean switch picks which one runs. This vault's API JSONs
already contain the pruned TRELLIS.2-only graph, so this file is a tour of the
half you *don't* run — enough to recognize it, not to operate it.

**`Switch to Trellis2` (the boolean node)**
- **true** (course setting): the Pixal3D branch nodes never execute — lazy
  evaluation prunes them. Your graph = the 28 nodes of this tour
- **false**: Pixal3D path runs instead: needs
  `diffusion_models/pixal3d_int8_convrot.safetensors` + a **MoGe geometry model**
  (`geometry_estimation/moge_2_vitl_normal_fp16.safetensors`, `LoadMoGeModel`
  node) + camera-conditioning nodes that estimate a virtual camera from the
  single photo before generating

**Why it matters even if you never flip it:**
1. **The “2 models missing” badge** on a fully-TRELLIS.2 setup = these two
   branch files (documented + curl block in
   [[05 TRELLIS.2 Model Weights#The files (reference — sizes match the block above)]])
2. **It's the fallback ladder**: when TRELLIS.2's bake is impossible,
   Pixal3D (and below it Hunyuan) are the documented degradation path —
   [[08 VRAM Playbook (12 GB and under)]] — which is why the course machine
   carries all three model sets

**Dials inside the branch:** MoGe loader (`model_name`, one file, nothing to
tune) and camera nodes (focal/angle estimation, all auto). No widget in the
Pixal3D half is worth turning from a TRELLIS.2 workflow — you switch *branches*,
you don't mix them.

Prev: [[13 Export MeshToFile3D and SaveGLB]] · Upstream half: [[00 Text2Image Node Map]] · Back: [[00 Node Map]]
