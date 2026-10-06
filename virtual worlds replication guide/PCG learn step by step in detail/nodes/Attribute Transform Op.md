---
tags: [pcg, unreal, pcg-node]
---
# Attribute Transform Op

**What it is:** per-point transform **math on attributes** — combine two
transform attributes (`InA × InB` in Compose mode) and write the result. The
learn graph uses it twice, in one pattern worth memorising.

## The step-8 fence pattern

```
S8_SampC point ($Transform already follows the road curve)
   +  S8_OffL constant (LocalOff = Translate(0,−600,0))
   =  S8_CmpL:  $Transform = $Transform × LocalOff
```

Result: each fence point slides 6 m **to its own side of the road** —
because composing *under* the existing transform means "local Y" is
"perpendicular to wherever this point's curve tangent points". A flat
[[nodes/Transform Points]] offset could only do world-space or a single
fixed local axis; composition handles per-point orientation.

| Pins | Use |
|---|---|
| `InA` | base transform (`$Transform`) |
| `InB` | offset transform (`LocalOff` from [[nodes/Add Attribute]]) |
| mode | **Compose** (matrix multiply) |
| `Out` / output tag | overwritten `$Transform` |

## When to reach for it

- Offsets that must follow **per-point rotation you didn't set** (splines
  with `bFitToCurve`, copied scans, …) — [[08 Step 8 - Trench Fence]].
- Stacking *reusable* offset attributes (store once, compose many places).
- Anything you'd otherwise do with two chained Transform Points that fight
  each other's rotations.

> [!warning] $Transform vs transform components
> Writing `$Transform` overwrites position+rotation+scale in one go — any
> later [[nodes/Transform Points]] still layers on top (add/multiply rules),
> but a later explicit `$Position` write will not know about yours. Keep one
> transform authority per branch.
