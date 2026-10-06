---
tags: [pcg, unreal, tutorial]
---
# Step 2 — Randomise

**Strip: +30 m.** Same trees, now alive: random spin, tilt and size. Compare
directly against strip 1 — identical points, identical mesh, only a
[[nodes/Transform Points]] inserted.

```
S6_Ground ──Surface──► S2_Sample ──► S2_Move ──► S2_Rand ──► S2_Tag ──► S2_Proj ──► S2_Spawn
```

| Node | Type | Configured with |
|---|---|---|
| `S2_Sample` | [[nodes/Surface Sampler]] | `pointsPerSquaredMeter=0.111` (denser than step 1) |
| `S2_Move` | [[nodes/Transform Points]] | `offset=(3000,0,0)` **absolute** — parks the strip 30 m down +X |
| `S2_Rand` | [[nodes/Transform Points]] | yaw 0–360°, pitch/roll ±6°, scale 0.6–1.6×, `bRecomputeSeed=true` |
| `S2_Tag` | [[nodes/Add Attribute]] | same `SkinnedMeshPath=PVE_Conifer_01` as step 1 |
| `S2_Proj` | [[nodes/Projection]] | `bProjectPositions` — re-snaps onto `S6_Ground` |
| `S2_Spawn` | [[nodes/Spawners (Static and Instanced Skinned)|Instanced Skinned Mesh Spawner]] | same selector as step 1 |

## The three rules this strip teaches

1. **Rotations ADD, scales MULTIPLY, offsets are point-local** —
   [[nodes/Transform Points]]' semantics (from
   [[17 Modular PCG via MCP#5. Height-placement rules (the expensive lessons)]]).
2. **Move = own node, absolutely-offset.** `S2_Move` uses
   `bAbsoluteOffset=true` so strip spacing is fixed in world units — scale
   the volume and the layout never explodes.
3. **Order matters: randomise → tag → snap → spawn.** The
   [[nodes/Projection]] comes *after* the transform (nothing sideways here,
   but this is the position the lift-after-projection rule will punish you
   for getting wrong in [[06 Step 6 - Float and Snap]]).

> [!tip] `bRecomputeSeed`
> Without it, every copy from a [[nodes/Duplicate Point]] upstream would
> reuse its parent's random value (identical spin). Recompute = per-point
> reseed.

Next: [[03 Step 3 - Break the Grid]]
