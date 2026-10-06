---
tags: [pcg, unreal, pcg-node]
---
# Get Actor Data

**What it is:** pulls a live level actor's components into PCG as **mesh /
surface data**. The inverse of a spawner: instead of PCG owning the actor,
the graph *reads* an actor the artist placed and edits normally.

**In the learn graph:** `S10_Get` in [[10 Step 10 - Scatter on a Mesh]] —
grabs the `SM_Rock_03` actor (selected **by tag** `PCG_Learn_Rock`), its
`StaticMeshComponent` (component filter **ByClass**), and
`alsoOutputSinglePoint=true` (a point at the actor's position, in addition
to the mesh).

## What the output enables

The reconstructed mesh is **Surface** data — identical type to
[[nodes/World Ray Hit Query]] output — so the *same*
[[nodes/Surface Sampler]] runs on it:

```
S10_Get → Filter Data–Surface → Surface Sampler (bUnbounded) → moss tufts
```

Move/rotate/rescale the rock actor → regenerate → moss follows. The actor
stays outside PCG ownership (never spawned/destroyed by the graph).

## Caveats

- **Actor scale leaks into sampled point scale** — step 10 pre-divides tuft
  scale for the rock's 2×. Check `GetNodeDataView` `$Scale` if scatter is
  oddly big/small on the mesh.
- Filter-Data node after it isn't optional ceremony — the sampler's
  `Surface` pin wants Surface-typed data
  ([[nodes/Boundary Helpers (Filter Data, To Point, Make Concrete)]]).
- By-tag selection, like [[nodes/Get Spline Data]]: no hard actor refs to
  break when someone renames things.
