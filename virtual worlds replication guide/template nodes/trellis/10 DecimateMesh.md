---
tags: [node, template, post]
---
# DecimateMesh

**What it is:** reduces the raw generated mesh (TRELLIS.2 emits *dense*
geometry — millions of tiny triangles from the voxel grid) down to a usable
triangle budget. Purely post-processing: **cannot OOM your generation**, worst
case it's slow.

**Widgets**

| Widget | Template default | Turning it does |
|---|---|---|
| `target_face_count` | 700 000 | the triangle budget. 700k = “keep everything, mostly”. For game engines this is *huge* — a hero prop wants 30–100k, clutter/background 5–20k. Lower = smaller GLB, faster UE import/lighter scene, slight loss of silhouettes on organic shapes |
| `placement_mode` | `midpoint` | decimation strategy; midpoint is the sane default. Don't tune unless you see artifacts on a specific model |

**Course-relevant dial:** this is your **UE budget lever after the fact** — drop
a 700k GLB into the demo level once, watch the stat counters, then re-run with
`target_face_count: 50000` and compare. Zero re-generation time if you save the
pre-decimate GLB ([[13 Export MeshToFile3D and SaveGLB]] runs *before* decimate
in the graph — that's on purpose: dense master + decimated game mesh).

**VRAM/time:** mesh-space CPU work; light VRAM. Safe on everything.

Prev: [[09 BakeTextureFromVoxel]] · Next: [[11 UnwrapMesh]]
