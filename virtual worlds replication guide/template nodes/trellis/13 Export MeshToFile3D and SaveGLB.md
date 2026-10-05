---
tags: [node, template, export]
---
# Export: ApplyTextureToMesh, MeshToFile3D, SaveGLB

**What they are:** the exit doors. Three nodes, two of them are alternatives —
know which one wrote your file.

| Node · Widget | Default | What it does / turning it |
|---|---|---|
| `ApplyTextureToMesh` | *no widgets* | fuses baked texture ([[09 BakeTextureFromVoxel]]) onto the UV-mapped mesh. Full pipeline only |
| `MeshToFile3D · filename_prefix` | `3d/VWML_trellis2_smoke` | writes the **pre-decimate dense master** — this is why the shape-only JSON sets `3d/VWML_trellis2_shape_only`: your GLB name = this string. Prefix doubles as folder: writes under `output/<prefix>*.glb` |
| `SaveGLB · filename_prefix` | `3d/VWML_trellis2_smoke` | writes the **final (decimated/unwrapped/smoothed)** mesh — usually the one you import to UE |

**Practical consequences worth internalizing:**
- Two files per full run: `..._00001_.glb` twice (master + final) with the same
  prefix, in `~/comfyui/ComfyUI/output/3d/` — check mtime/size to tell them apart
- `filename_prefix` is how runs stay organized (`3d/day1_batch/`) and how our
  [[07 Headless Generation and the API]] batch pattern finds “the new file”
- GLB is the interchange format everything downstream (UE import,
  gltf-viewer, Blender) eats — no conversion step exists, and none is needed

Prev: [[12 MeshSmoothNormals]] · Next: [[14 Switch and the Pixal3D Branch]]
