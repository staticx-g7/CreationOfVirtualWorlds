---
tags: [pcg, unreal, tutorial]
---
# Step 5 — Clumps Near Trees

**Strip: +120 m.** The first *two-layer* step: sparse tree anchors spawn
trees **and** sprout grass clumps around each trunk, merged with a plain
lawn — all into one grass spawner call.

```
S6_Ground ──Surface──► S5_Sample ──► S5_Move ──┬─► S5_Dup ──► S5_Scatter ──┐
                                    (anchors)  │                            ├─► S5_Merge ──► S5_Proj ──► S5_Spawn
S6_Ground ──Surface──► S5_Sample2 ─► S5_Move2 ─► S5_LawnT ──────────────────┘
S5_Move ───────────────► S5_Tag ──► S5_SpawnTrees          (the trees themselves)
```

| Node | Type | Configured with |
|---|---|---|
| `S5_Sample` | [[nodes/Surface Sampler]] | `0.02`/m² — the tree anchors |
| `S5_Dup` | [[nodes/Duplicate Point]] | `iterations=25` per anchor, same spot |
| `S5_Scatter` | [[nodes/Transform Points]] | ±3 m **point-local** offset → one clump *per tree* |
| `S5_Sample2` / `S5_Move2` / `S5_LawnT` | [[nodes/Surface Sampler]] (0.444/m²) + [[nodes/Transform Points]] | the plain lawn layer |
| `S5_Merge` | [[nodes/Merge Points]] | lawn + clumps → ONE stream |
| `S5_Spawn` | [[nodes/Spawners (Static and Instanced Skinned)|Static Mesh Spawner]] | same mesh list as step 4, bigger scales |
| `S5_Tag` / `S5_SpawnTrees` | [[nodes/Add Attribute]] + [[nodes/Spawners (Static and Instanced Skinned)|Instanced Skinned Mesh Spawner]] | the anchor points become the trees |

## Lessons

1. **Duplicate → local-offset = clumping.**
   [[nodes/Duplicate Point]] copies a point 25× *at the same position*;
   because [[nodes/Transform Points]] offsets are **point-local**, each copy
   moves sideways from **its own anchor** — instant per-tree clumps with no
   distance maths.
2. **One stream, one spawner.** [[nodes/Merge Points]] concatenates lawn +
   clumps so the spawner runs once (cheaper, one log line). The size
   difference is already baked into the point scales by `S5_Scatter`.
3. **Anchors double as trees and as clump seeds** — the same `S5_Move`
   output feeds the tree branch *and* the duplicate branch. Point data is
   cheap to fork; this is the PCG version of DRY.

> [!note] This is the real graph's pattern
> `SG_TallGrassClumps` in [[PCG_ScatterMesh - Module Map]] is exactly this
> idea with `×120` per tree and ±4.5 m scatter.

Next: [[06 Step 6 - Float and Snap]]
