---
tags: [pcg, unreal, tutorial]
---
# Step 9 — The Grove

**Region demo, not a strip.** A **closed** drawn spline defines a circular
plot; conifers fill **only the interior**. This is the "paint a region, let
PCG fill it" authoring pattern.

```
DRAW IT: closed spline, actor tagged "PCGLearn_GroveSpline"
S9_Spline ──► S9_Samp (OnInterior, Fill, ~4 m) ──► S9_Tag ──► S9_Var ──► S9_Proj ──► S9_Spawn
S6_Ground ───────────────────────────────────────► (Projection Target)
```

| Node | Type | Configured with |
|---|---|---|
| `S9_Spline` | [[nodes/Get Spline Data]] | by tag `PCGLearn_GroveSpline`, `alwaysRequery` — empty until you draw |
| `S9_Samp` | [[nodes/Spline Sampler]] | **`dimension=OnInterior`, `fill=Fill`**, `interiorSampleSpacing=400` |
| `S9_Tag` | [[nodes/Add Attribute]] | conifer `SkinnedMeshPath` |
| `S9_Var` | [[nodes/Transform Points]] | yaw ±180°, uniform scale 0.8–1.4 |
| `S9_Proj` | [[nodes/Projection]] | snap to `S6_Ground` (coarser far from the volume — known limit) |
| `S9_Spawn` | [[nodes/Spawners (Static and Instanced Skinned)|Instanced Skinned Mesh Spawner]] | |

## Lessons

1. **`OnInterior` turns a spline into a mask.** Same
   [[nodes/Spline Sampler]] node as the road (which used `OnSpline`) — the
   `dimension` flag flips it from "walk the curve" to "flood the polygon".
   One node class, two authoring modes.
2. **Closed spline = region, open spline = path.** Draw with the PCG spline
   tool closed (loop) and the sampler's `Fill` mode covers it like a cookie.
3. Everything downstream is boring on purpose — tag → vary → snap → spawn
   is [[01 Step 1 - Density and Tag|step 1]] + [[02 Step 2 - Randomise|step 2]];
   only the *source* changed. That's the modular mindset of
   [[17 Modular PCG via MCP]] in one node swap.

> [!tip] Try
> Redraw the loop smaller and regenerate — the grove re-counts itself
> automatically (interior area × spacing), no node edited.

Next: [[10 Step 10 - Scatter on a Mesh]]
