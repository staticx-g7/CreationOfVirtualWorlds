---
tags: [node, template, post]
---
# UnwrapMesh

**What it is:** creates UV coordinates — the “flattening pattern” that lets a
2D texture image paint a 3D mesh. A GLB without UVs is untexturable in any
engine, which is why even the geometry-only workflow keeps this node.

**Widgets**

| Widget | Template default (full / shape-only) | Turning it does |
|---|---|---|
| `segmenter` | `pec` | UV-segmenting model (learned). Alternative `convex_hull` is dumber/faster with worse seams — no reason here |
| `resolution` | 4096 / 1024 | resolution of the internal UV-atlas raster: higher = better seam placement + larger placeholder texture. 4096 fine post-generation; **shape-only on 12 GB uses 1024** — cheap and enough when nothing samples it |
| `padding` | 1 | texel gap between UV islands; 1–2 prevents texture bleeding at seams. 0 = visible seam lines on baked textures |
| `weld_distance` | 0.0002 | pre-welds coincident verts (smaller mesh, fewer UV cracks). Lower = risk of split seams; raise only if you see micro-gaps |

**Cost profile:** CPU-heavy, seconds-to-a-minute; VRAM ∝ `resolution²`. It's
*after* the diffusion so it can't kill your run — the classic “it froze” moment
here is just patience ([[14 Troubleshooting Field Guide]]).

Prev: [[10 DecimateMesh]] · Next: [[12 MeshSmoothNormals]]
