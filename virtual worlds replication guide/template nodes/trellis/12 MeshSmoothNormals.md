---
tags: [node, template, post]
---
# MeshSmoothNormals ×2

**What it is:** recomputes vertex normals so the low-poly result *shades*
smoothly instead of showing every triangle facet. It appears **twice** in the
graph — after decimate and after unwrap — because each of those steps mangles
normals again, and this node is too cheap to skip in between.

**Widgets**

| Widget | Template default | Turning it does |
|---|---|---|
| `crease_angle` | 180.0 | angle threshold for “keep this edge sharp”. **180 = smooth everything** (default, good for organic). Lower (30–60) preserves hard edges on man-made objects — a crate wants ~45 or it looks wax-dipped; a rock wants 180 |

**The one visible symptom of this being wrong:** your box looks like a melted
box (over-smoothed corners) or your boulder looks faceted (over-sharpened).
Fix = this dial, nothing else.

**VRAM/time:** trivial. Safe everywhere.

Prev: [[11 UnwrapMesh]] · Next: [[13 Export MeshToFile3D and SaveGLB]]
