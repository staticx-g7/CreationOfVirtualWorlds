---
tags: [pcg, unreal, pcg-node]
---
# Transform Points

**What it is:** moves / rotates / scales points by random ranges. The
workhorse — **18 instances** in the learn graph (strip parking, jitter,
tumble, size variance, the float).

## The three rules (from the graph comments, the hard way)

1. **Offsets rotate with the point** — they are *point-local* unless
   `bAbsoluteOffset=true`. X = along the point's facing, Y = sideways,
   Z = up. That's how sideways-from-curve tricks work
   ([[08 Step 8 - Trench Fence|step 8]] does the attribute version).
2. **Rotations ADD** to the point's existing rotation (relative) — yaw
   `0→360` + reseed = random spin; `−12→12` = slight wiggle around the
   current facing ([[PCG_ScatterMesh - Module Map|SG_RoadFlagstones]]).
3. **Scales MULTIPLY** the point's scale — duplicated points inherit and
   grow with their parent ([[05 Step 5 - Clumps Near Trees|step 5]],
   `SG_GrassTufts`).

## Jobs it performs here

| Job | Where | Settings |
|---|---|---|
| strip parking | `S2…S6_Move` | absolute `(30/60/90/120/150 m,0,0)` |
| jitter | `S3_Jitter` | local XY ±140 cm, reseed |
| tumble | `S4_Tumble`, `S5_LawnT` | pitch/roll ±12–15°, yaw full, reseed |
| size variance | `S2_Rand`, `S3_Vary`, `S9_Var` | scale min/max ranges |
| embed rocks | `SG_Rocks` | z offset −25…+10 cm — sinks some |
| the FLOAT | `S6_Vary`, `S6_Lawn` | absolute +150 m Z ([[06 Step 6 - Float and Snap]]) |
| fence scale knob | `S8_Scale` | `(3,1,1)` multiplies along tangent |

> [!warning] Two placement traps
> - **A later [[nodes/Projection]] overwrites your Z.** Lift AFTER
>   projection ([[17 Modular PCG via MCP#5. Height-placement rules (the expensive lessons)|rule 2]]).
> - **Sideways move → new ground underneath.** Re-snap after it (rule 3) —
>   see the water ribbon's snap→offset→**re-snap** chain.

> [!tip] `bRecomputeSeed=true`
> Present on nearly every instance. Without it, points duplicated from one
> anchor all draw the *same* "random" offset — identical clumps.
