---
tags: [pcg, unreal, tutorial]
---
# Step 7 — Road Cut

**Strip: −60 m (front strip).** First contact with **drawn authoring**: you
draw a spline in the viewport, and vegetation keeps out of its corridor. The
real graphs do this with cookie-cutters (Difference); the learn graph shows
the *distance* way — which is what you reach for when you need road **width
as a knob**.

```
DRAW IT: actor "PCG_Learn_Road", tag "PCGLearn_RoadSpline"
S7_Spline ──Out──► S7_Road (Spline Sampler, 2 m chain)
S6_Ground ──Surface──► S7_Sample ──► S7_Move(−60 m) ──► S7_Proj ──► S7_Tag
                                                             │ Source
S7_Road ──────────────────────────────────────────── Target ─► S7_Cut (Distance)
S7_Cut ──► S7_Keep (> 4 m) ──InsideFilter──► S7_Spawn
```

| Node | Type | Configured with |
|---|---|---|
| `S7_Spline` | [[nodes/Get Spline Data]] | by tag `PCGLearn_RoadSpline`, `alwaysRequery` — live |
| `S7_Road` | [[nodes/Spline Sampler]] | every 2 m along the spline, `bUnbounded` |
| `S7_Sample` | [[nodes/Surface Sampler]] | copy of step 1 (0.03/m²) |
| `S7_Move` | [[nodes/Transform Points]] | absolute **−60 m** — parked low so the ground rays still reach it |
| `S7_Cut` | [[nodes/Distance]] | writes `DistToRoad` = distance to nearest road point |
| `S7_Keep` | [[nodes/Filter Attribute Elements by Range]] | keep `DistToRoad > 400 cm` — **minThreshold = road width** |
| `S7_Spawn` | [[nodes/Spawners (Static and Instanced Skinned)|Instanced Skinned Mesh Spawner]] | survivors |

## Lessons

1. **Measure, then filter.** [[nodes/Distance]] stores a number per point;
   [[nodes/Filter Attribute Elements by Range]] acts on it. Two dumb nodes
   beat one clever one — and the *road is now a slider* (widen: raise
   `minThreshold`).
2. **Live re-query = redraw and regenerate.** No graph edit to move the
   road; the spline actor is the UI.
3. **The cut is scoped**: `S7_Cut` only sees this strip's points — steps 1–6
   ignore the road entirely (they'd still need cookie-cutters if they
   wanted it: see `SG_RoadCorridor` + `Difference` in
   [[PCG_ScatterMesh - Module Map]]).
4. Disable `S7_Spline` or `S7_Road` → nothing is near a "road" → strip grows
   back full. That's the built-in A/B toggle.

> [!warning] Why −60 m and not far up the hill?
> Node comment: terrain rays only reach the volume footprint area — strips
> parked far from the volume would project underground.

Next: [[08 Step 8 - Trench Fence]]
