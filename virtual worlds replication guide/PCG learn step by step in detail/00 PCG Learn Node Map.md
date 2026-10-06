---
tags: [pcg, unreal, tutorial, moc]
---
# PCG Learn — Node Map

The asset **`/Game/PCG/PCG_Learn_StepByStep`** (74 nodes, 81 edges) is a
tutorial copy of [[PCG_ScatterMesh - Module Map|PCG_ScatterMesh]] — ten steps
laid out as parallel **strips** in one graph, so you can compare techniques
side by side in the same generated world. It is *not* used by the level;
`ScatterVolume` runs the real scatter graph.

> [!important] The volume transform is the master switch
> One **PCG volume** runs the graph. Move it → the whole layout follows.
> Rotate → layout rotates. **Scale → the sampled footprint grows and the
> POINT COUNT grows with it** at constant real-world spacing
> ([[nodes/Surface Sampler|Surface Sampler]] works in pts/m²). At scale 1 the
> brush is 5×5 m — scale the volume up (e.g. 40) to see a real forest strip.
> Requires **terrain under the volume** (everything samples its surface).

## Architecture (one ground read, ten strips)

```mermaid
flowchart LR
  G[nodes/World Ray Hit Query|S6_Ground] --> S1[Step 1 strip @ 0 m]
  G --> S2[Step 2 strip @ +30 m]
  G --> S3[Step 3 strip @ +60 m]
  G --> S4[Step 4 strip @ +90 m]
  G --> S5[Step 5 strip @ +120 m]
  G --> S6[Step 6 strip @ +150 m]
  G --> S7[Step 7 strip @ −60 m road demo]
  SP[drawn road spline] --> S7
  SP --> S8[Step 8 trench fence]
  GL[drawn grove loop] --> S9[Step 9 grove]
  R[SM_Rock_03 actor] --> S10[Step 10 moss on mesh]
```

Each step parks itself with an **absolute-offset**
[[nodes/Transform Points|Transform Points]] (`bAbsoluteOffset=true`, +30 m
steps) — scale the volume and the layout never explodes; strip spacing stays
fixed in world units.

## The ten steps

| Step | Strip | Teaches | Node chain |
|---|---|---|---|
| 1 | 0 m | density sample + mesh tag + spawn | [[01 Step 1 - Density and Tag]] |
| 2 | +30 m | randomise (spin/scale) | [[02 Step 2 - Randomise]] |
| 3 | +60 m | break the grid (jitter + thin) | [[03 Step 3 - Break the Grid]] |
| 4 | +90 m | grass layer (static meshes) | [[04 Step 4 - Grass Layer]] |
| 5 | +120 m | clumps around trees (duplicate) | [[05 Step 5 - Clumps Near Trees]] |
| 6 | +150 m | the float + snap demo | [[06 Step 6 - Float and Snap]] |
| 7 | −60 m | road cut from a drawn spline | [[07 Step 7 - Road Cut]] |
| 8 | on road | trench fence along the curve | [[08 Step 8 - Trench Fence]] |
| 9 | drawn loop | trees inside a closed region | [[09 Step 9 - The Grove]] |
| 10 | rock actor | scatter on a mesh surface | [[10 Step 10 - Scatter on a Mesh]] |

## Node reference (every node type used)

- Sources: [[nodes/World Ray Hit Query]] · [[nodes/Get Spline Data]] ·
  [[nodes/Get Actor Data]]
- Generators: [[nodes/Surface Sampler]] · [[nodes/Spline Sampler]] ·
  [[nodes/Duplicate Point]]
- Modifiers: [[nodes/Transform Points]] · [[nodes/Add Attribute]] ·
  [[nodes/Attribute Transform Op]] · [[nodes/Random Choice]]
- Filters: [[nodes/Distance]] · [[nodes/Filter Attribute Elements by Range]]
- Snapping: [[nodes/Projection]]
- Merging: [[nodes/Merge Points]]
- Output: [[nodes/Spawners (Static and Instanced Skinned)]]
- Boundary plumbing: [[nodes/Boundary Helpers (Filter Data, To Point, Make Concrete)]]

## How to walk it in the editor

1. Open the level, select **`PCG_Learn_Tutorial`** (the volume; scale it up
   to ~40 on X/Y).
2. Open the graph, press **Generate** — strips appear 30 m apart.
3. Toggle nodes with **D** and regenerate — the comments tell you what
   disappears (e.g. disable a [[nodes/Projection|Projection]] and the strip
   floats in the air).
4. Steps 7–9 need drawing: they read splines live
   ([[nodes/Get Spline Data|Get Spline Data]] with `alwaysRequery`), so
   redraw the road/loop and re-generate.

Related: [[17 Modular PCG via MCP]] (how the real graphs were built) ·
[[10 Create the Demo Project]]
