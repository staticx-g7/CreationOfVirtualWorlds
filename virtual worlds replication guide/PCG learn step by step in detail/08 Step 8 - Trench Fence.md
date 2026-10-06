---
tags: [pcg, unreal, tutorial]
---
# Step 8 — Trench Fence

**On the same drawn road spline.** One spline now drives *two* features: the
step-7 road cut and a corrugated trench wall on **both shoulders**. The new
trick: pushing points sideways **along their own curve-following rotation**
using transform *attributes* instead of Transform Points.

```
S7_Spline ──► S8_SampC (every 8 m, bFitToCurve — rotation follows road)
                ├─► S8_OffL (Add Attribute: LocalOff = (0,−600,0)) ─► S8_CmpL ─┐
                └─► S8_OffR (Add Attribute: LocalOff = (0, 600,0)) ─► S8_CmpR ─┤
                                                          S8_CmpL ┐            │
                                                          S8_CmpR ┴► S8_Scale ─► S8_Spawn
```

| Node | Type | Configured with |
|---|---|---|
| `S8_SampC` | [[nodes/Spline Sampler]] | `distanceIncrement=800`, **`bFitToCurve=true`** — each point's rotation follows the curve |
| `S8_OffL` / `S8_OffR` | [[nodes/Add Attribute]] | constant **Transform** attribute `LocalOff`, local Y ∓6 m |
| `S8_CmpL` / `S8_CmpR` | [[nodes/Attribute Transform Op]] | Compose: `$Transform = $Transform × LocalOff` |
| `S8_Scale` | [[nodes/Transform Points]] | `scale=(3,1,1)` — the FENCE SIZE KNOB (stretches along the road) |
| `S8_Spawn` | [[nodes/Spawners (Static and Instanced Skinned)|Static Mesh Spawner]] | corrugated trench wall mesh |

## Lessons

1. **Why not just Transform Points with a Y offset?** It would work — but
   composing a **Transform attribute** onto `$Transform` via
   [[nodes/Attribute Transform Op]] is the *general* trick: you can store,
   copy, and compose arbitrary transforms per point, and it composes
   *under* the point's existing curve rotation instead of fighting it.
2. **`bFitToCurve` is the load-bearing flag** on `S8_SampC` — without the
   curve-following rotation, "local Y" wouldn't mean "sideways off the
   road". Same reason the water ribbon in
   [[PCG_ScatterMesh - Module Map|SG_WaterRibbon]] offsets sideways cleanly.
3. **One branch, two fences, one spawner.** Left/right chains re-merge at
   `S8_Scale` — both sides share the scale knob and one
   [[nodes/Spawners (Static and Instanced Skinned)|spawner]].

> [!tip] Scaling a wall segment
> `scale=(3,1,1)` stretches each mesh **along local X = the road tangent** —
> segment length knob without touching height. Crank min/max apart for
> weathered, uneven walls.

Next: [[09 Step 9 - The Grove]]
