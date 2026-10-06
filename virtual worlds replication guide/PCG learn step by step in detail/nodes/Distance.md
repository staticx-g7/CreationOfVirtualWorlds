---
tags: [pcg, unreal, pcg-node]
---
# Distance

**What it is:** for every point in `Source`, finds the nearest point in
`Target` and **stores the number** as a float attribute. It doesn't
remove anything — pairing with a range filter is what makes it a cutter.

**In the learn graph:** `S7_Cut` in [[07 Step 7 - Road Cut]] —
`outputAttribute = "DistToRoad"`, target = the 2 m road point chain from
[[nodes/Spline Sampler|S7_Road]], `maximumDistance` effectively unlimited.

## The distance-cut pair

```
S7_Tag ──Source──► [Distance → DistToRoad] ──► [Filter by Range: keep > 4 m] ──► spawn
S7_Road ─ Target ─┘
```

- The attribute is just data: you could log it, colour by it, drive scale
  by it — the [[nodes/Filter Attribute Elements by Range]] is one opinion
  about it.
- **Road width = the filter's `minThreshold`** — one number, live on regen.

## Distance vs Difference (the two cutter philosophies)

| | This pair | `Difference` (real graphs) |
|---|---|---|
| Mechanism | measure + range-test | spatial boolean with fat "cookie" points |
| Width control | filter threshold | `RoadCut` [[nodes/Surface Sampler|sampler]] extents (650 cm) |
| Costs | extra attribute + filter node | one node, needs fat points |
| Learn-graph role | step 7 | steps 1–6 ignore roads entirely |

`SG_Trees` etc. use `Difference` (`densityFunction=Binary, mode=Discrete`)
against `SG_RoadCorridor`'s `Cutter` — same result, fewer nodes, less
tunability ([[PCG_ScatterMesh - Module Map]]).

> [!warning] Target must cover the area
> The measure is "nearest target point" — where the road chain is sparse or
> missing, distances explode and every point "passes" the filter. An empty
> [[nodes/Get Spline Data]] silently un-cuts the whole strip (that's the
> built-in toggle in step 7).
