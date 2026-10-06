---
tags: [pcg, unreal, pcg-node]
---
# World Ray Hit Query

**What it is:** shoots world rays down through the volume's bounds and
returns every hit as a **Surface** data set — the graph's *model of the
ground*. One node, read once, reused everywhere.

**In the learn graph:** `S6_Ground` — the root source of all ten steps.
Every [[nodes/Surface Sampler]]'s `Surface` pin and every
[[nodes/Projection]]'s `Projection Target` hangs off its `Out`.

## Live configuration (from the graph)

| Param | Value | Why |
|---|---|---|
| `rayOrigin` | `(0,0,6000)` | start 60 m above |
| `rayDirection` / `rayLength` | `(0,0,−1)` / `15000` | 150 m downward reach |
| `bGetImpactNormal` | **true** | drives `ImpactNormal` — used for tilt-to-ground everywhere |
| `bIgnorePCGHits` | **true** | PCG-spawned stuff can never block the ground read |
| `bIgnoreSelfHits` | true | |
| `collisionChannel` | `ECC_WorldStatic` | terrain/landscape/static meshes |
| `selectLandscapeHits` | Include | |

## Why one node feeds the whole graph

- Collision is the expensive part — read it **once**, pass the Surface
  around. In [[PCG_ScatterMesh - Module Map]] this is `SG_GroundSurface`, a
  one-node module whose only job is being everyone's `Surface` input.
- `bIgnorePCGHits=true` is the answer to
  [[17 Modular PCG via MCP#5. Height-placement rules (the expensive lessons)|rule 4]]:
  points spawned this run have no cooked collision yet, so a ground query
  that *didn't* ignore PCG hits would start sampling the previous run's
  grass as terrain.

> [!warning] Rays only reach under the volume footprint
> Strips parked far from the volume ([[07 Step 7 - Road Cut|step 7 at −60 m]])
> project correctly only because they sit near the sampled area — far-away
> projections latch onto the nearest edge rays. The [[nodes/Projection]]
> nearest-neighbour caveat is the same root cause.

Used in: [[06 Step 6 - Float and Snap]] (the visible demo) · every other
step's sampler.
