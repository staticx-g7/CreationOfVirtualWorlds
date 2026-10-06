---
tags: [pcg, unreal, pcg-node]
---
# Duplicate Point

**What it is:** copies each input point N times (`iterations`), all copies
**at the same position** (and same scale/rotation, metadata shared). Boring
alone; paired with a [[nodes/Transform Points]] local offset it becomes the
**clump generator**.

## In the graphs

| Instance | iterations | Feeds |
|---|---|---|
| `S5_Dup` (learn) | **25** | ±3 m scatter → clumps per tree ([[05 Step 5 - Clumps Near Trees]]) |
| `SG_TallGrassClumps` | **120** | ±4.5 m scatter, +2 m up, around every tree |
| `SG_GrassTufts` DupRock | 1 | one tuft per boulder |
| `SG_GrassTufts` DupFloor | 2 | two tufts per floor rock |

## Why this beats a second sampler

A second [[nodes/Surface Sampler]] would scatter *uniformly by area*. A
duplicate+local-offset clumps **relative to each anchor** — grass around
trunks, tufts on rocks — while *inheriting* the anchor's scale (scales
multiply, [[nodes/Transform Points]]), so grass on a big rock is bigger for
free ([[17 Modular PCG via MCP#7. Grass-on-rocks recipe]]).

> [!warning] It multiplies your point count
> `iterations=120` on 4 000 tree anchors = 480 000 points. In the real graph
> this runs *before* road [[nodes/Filter Attribute Elements by Range|cutting]] and
> snapping — keep the duplicate **after** the anchor density node and the
> anchors themselves sparse. And beware `GetNodeDataView` timeouts on these
> monster nodes ([[17 Modular PCG via MCP#8. Verify like we did (no eyeballing first)|verify step 5]]).

> [!note] `bOutputSourcePoint=false`
> Keep the original out of the output stream when the copies replace it
> (tufts don't need the bare rock point in the grass data).
