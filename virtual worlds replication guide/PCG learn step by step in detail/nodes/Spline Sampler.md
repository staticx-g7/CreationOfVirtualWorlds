---
tags: [pcg, unreal, pcg-node]
---
# Spline Sampler

**What it is:** walks a **Spline** input and emits points along/in it. One
node class, *three distinct authoring modes* — all three are used in the
learn graph.

## The modes, as configured here

| Instance | mode | What it makes |
|---|---|---|
| `S7_Road` (step 7) | `dimension=OnSpline`, `mode=Distance`, `distanceIncrement=200`, `bUnbounded` | a 2 m point chain = the road corridor to measure against |
| `S8_SampC` (step 8) | `OnSpline`, `distanceIncrement=800`, **`bFitToCurve=true`** | fence posts every 8 m, rotation following the curve |
| `S9_Samp` (step 9) | **`dimension=OnInterior`**, `fill=Fill`, spacing 4 m | trees flooding the closed loop only |
| `SG_WaterRibbon` | `OnSpline`, 120 cm, `bComputeTangents`→`WaterDir` | dense overlapping tile ribbon |
| `SG_RoadFlagstones` | 520 cm, tangent→`RoadDir` | slabs along the path |

## Params worth knowing

- `distanceIncrement` — the spacing knob, real-world cm. 520 (flagstones) vs
  120 (water) is the difference between *beaded* and *continuous*.
- `bFitToCurve` — point rotation follows the tangent. Load-bearing for
  [[08 Step 8 - Trench Fence|sideways offsets]]
  ([[nodes/Attribute Transform Op]]).
- `bComputeTangents` + `leaveTangentAttribute` — stores the tangent as a
  named vector attribute (`WaterDir`, `RoadDir`) that
  [[nodes/Add Attribute]] later feeds into `MakeRotFromXZ`.
- `bUnbounded` — don't clip output to the volume bounds (splines usually
  leave it).

> [!tip] Tangent → rotation, the two-step dance
> Sampler stores tangent attribute → `Make Rotator Attribute`
> (`MakeRotFromXZ`, tangent + `ImpactNormal`) writes `$Rotation`. Yaw from
> the path, tilt from the ground — the water ribbon and flagstones both do
> exactly this ([[PCG_ScatterMesh - Module Map]]).
