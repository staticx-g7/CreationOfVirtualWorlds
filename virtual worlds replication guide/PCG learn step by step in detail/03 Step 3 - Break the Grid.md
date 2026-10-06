---
tags: [pcg, unreal, tutorial]
---
# Step 3 — Break the Grid

**Strip: +60 m.** Steps 1–2 prove the grid is perfect; step 3 destroys it —
the two cheapest tools against "too procedural": **jitter** and **thinning**.

```
S6_Ground ──Surface──► S3_Sample ──► S3_Jitter ──► S3_Half ──Chosen──► S3_Move ──► S3_Vary ──► S3_Tag ──► S3_Proj ──► S3_Spawn
                                                          Discarded ──► (dies here)
```

| Node | Type | Configured with |
|---|---|---|
| `S3_Sample` | [[nodes/Surface Sampler]] | `pointsPerSquaredMeter=0.111` |
| `S3_Jitter` | [[nodes/Transform Points]] | XY offset ±140 cm — breaks rows/columns |
| `S3_Half` | [[nodes/Random Choice]] | default 50 %: `Chosen` survives, `Discarded` stops |
| `S3_Move` | [[nodes/Transform Points]] | absolute +60 m X — strip parking |
| `S3_Vary` | [[nodes/Transform Points]] | spin/tilt/scale like [[02 Step 2 - Randomise|step 2]] |
| `S3_Tag` | [[nodes/Add Attribute]] | **different species**: `Tree_Black_Alder_01_B` (Megaplant) |
| `S3_Proj` | [[nodes/Projection]] | re-snap after the ±1.4 m sideways move |
| `S3_Spawn` | [[nodes/Spawners (Static and Instanced Skinned)|Instanced Skinned Mesh Spawner]] | |

## Lessons

1. **Jitter first, thin second, snap last.** The
   [[nodes/Random Choice]] drop makes density *uneven* (patches), which reads
   natural; the later [[nodes/Projection]] exists only because jitter moved
   points sideways — the ground under a point changed
   ([[17 Modular PCG via MCP#5. Height-placement rules (the expensive lessons)|rule 3]]).
2. **Discarded data just stops.** No error, no empty instances — a
   [[nodes/Random Choice]] pin with nothing wired is a point-deletion tool.
3. The strip swaps to a **different tree species** via one
   [[nodes/Add Attribute]] change — species is data on the points, not a
   spawner setting.

> [!tip] Read the strips left-to-right physically
> Walk the volume +X in the viewport: grid → alive → scattered. The graph is
> literally a "before/after/after" lineup you can screenshot for a lecture.

Next: [[04 Step 4 - Grass Layer]]
