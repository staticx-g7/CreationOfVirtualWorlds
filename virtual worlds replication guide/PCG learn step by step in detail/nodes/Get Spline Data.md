---
tags: [pcg, unreal, pcg-node]
---
# Get Spline Data

**What it is:** finds spline actors in the level and outputs their splines as
PCG **Spline** data — the bridge between *drawn authoring* and generation.

**In the learn graph:** `S7_Spline` (tag `PCGLearn_RoadSpline` → road + fence
for steps 7–8) and `S9_Spline` (tag `PCGLearn_GroveSpline` → grove region for
step 9).

## Configuration that matters

| Param | Value | Meaning |
|---|---|---|
| `actorSelection` | **ByTag** | the tag *is* the API — draw an actor with the tag, done |
| `bSelectMultiple` | true | several drawn actors feed one graph |
| `bIgnoreSelfAndChildren` | true | never read the volume running the graph |
| `alwaysRequery` (re-query) | **true** | redraw or move the spline actor → regenerate picks it up, zero graph edits |

## The authoring loop it enables

```
draw spline (PCG spline tool, actor tagged)  →  Generate  →  walk over  →  redraw  →  Generate
```

- [[07 Step 7 - Road Cut]]: the drawn road *is* the corridor mask.
- [[08 Step 8 - Trench Fence]]: same spline, second consumer.
- `SG_RoadCorridor` in [[PCG_ScatterMesh - Module Map]] reads tag
  `RoadSpline` and fans it out to `Spline` / `Cutter` / `TileStrip`.

> [!warning] Empty tag match = silently empty branch
> Nothing tagged → node emits nothing → downstream spawner logs nothing.
> Not an error. Check actor tags first when a spline-driven feature "isn't
> generating".
