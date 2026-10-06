---
tags: [pcg, unreal, pcg-node]
---
# Merge Points

**What it is:** concatenates several point sets into **one stream** — no
deduplication, no spatial logic, just "all of them".

**In the learn graph:** `S5_Merge` joins the lawn layer with the per-tree
clumps so [[05 Step 5 - Clumps Near Trees|step 5]] spawns both with a single
[[nodes/Spawners (Static and Instanced Skinned)|spawner]]. `SG_GrassTufts`'s
`JoinTufts` (a **Gather** node — same idea, general data) merges the boulder
and floor-rock tuft branches.

## Why merge before the spawner

- One spawner node = one log line (`Added N instances`) and one batch of
  instances — easier verify pass
  ([[17 Modular PCG via MCP#8. Verify like we did (no eyeballing first)]]).
- The two layers already differ *in their points* (scale/rotation set by
  their own [[nodes/Transform Points]]) — the spawner doesn't need to know
  there were two sources.
- Multi-mesh sharing: `SG_GrassTufts` deliberately does **not** merge but
  adds a *second input connection* to the existing grass spawner — pins
  accept multiple data inputs, so merging vs multi-wiring are both fine;
  merge when sources share everything, multi-wire when they don't.

> [!warning] Merge ≠ Difference ≠ Gather
> Merge = union of points. **Difference** = subtraction (the road cutters in
> [[PCG_ScatterMesh - Module Map]]). **Gather** = concat of arbitrary data
> types. They look similar in the palette; picking wrong = silently empty or
> tripled output.
