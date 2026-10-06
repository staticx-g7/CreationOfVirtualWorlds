---
tags: [pcg, unreal, pcg-node]
---
# Projection

**What it is:** the **snap**. Copies the nearest point of a *target* surface
onto each input point's position, so everything that moved sideways (or was
launched 150 m up) lands back on the ground.

**In the learn graph:** 8 instances (`S2_Proj … S9_Proj`), always with
`bProjectPositions=true` and `S6_Ground`'s Surface as
`Projection Target`.

## Pins

- `In` — the data to snap.
- `Projection Target` — a **concrete** surface; that's why every real module
  shows a [[nodes/Boundary Helpers (Filter Data, To Point, Make Concrete)|Make Concrete]]
  feeding this pin (boundary data arrives abstract).
- `Out` — snapped points; **spawners attach here**, never upstream
  ([[06 Step 6 - Float and Snap]]).

## Ordering laws (both are graph comments in the real project)

1. Snap **after** every sideways move
   ([[17 Modular PCG via MCP#5. Height-placement rules (the expensive lessons)|rule 3]]).
2. **Lift after** the snap — a downstream Projection silently erases a Z
   offset applied before it (rule 2). The real graphs' `LiftGrass`/
   `LiftWater` sit *after* `Proj…` for exactly this reason.

## Honest limitation (from `S2_Proj` comment)

Projection is **nearest-neighbour** against the ground-ray grid:
- volume scale ≤ ~5: heights are accurate;
- extreme scales: the ray grid is coarse relative to terrain and heights
  drift. Known, accepted, documented in-graph.

> [!tip] Debug toggle
> Select any Projection in the learn graph and press **D** → regenerate →
> the strip floats. Fastest way to *feel* what the node does.

> [!note] Rotations
> `bProjectRotations` can also tilt points to the target normals; the
> learn graph keeps it false and does rotation explicitly with
> [[nodes/Add Attribute|Add Attribute]] + `Make Rotator Attribute`
> ([[PCG_ScatterMesh - Module Map|SG_WaterRibbon]]).
