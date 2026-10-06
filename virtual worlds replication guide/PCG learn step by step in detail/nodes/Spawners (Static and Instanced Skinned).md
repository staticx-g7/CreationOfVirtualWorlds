---
tags: [pcg, unreal, pcg-node]
---
# Spawners (Static and Instanced Skinned)

**What they are:** the only nodes that turn points into rendered objects.
Learn graph uses both families; the real
[[PCG_ScatterMesh - Module Map|PCG_ScatterMesh]] keeps exactly **10** of them
in the main graph — and that placement is a *rule*, not a style choice.

## Static Mesh Spawner (learn: `S4_Spawn`, `S5_Spawn`, `S6_SpawnG`, `S8_Spawn`, `S10_Moss`)

- Mesh list lives **inside the node** as an inner selector object:
  `PCGStaticMeshSpawnerSettings_N.PCGMeshSelectorWeighted_0`
  (e.g. step 4 = 4 grass variants, equal weight; rocks = 17 variants).
- Points carry **no** mesh info — `In` + points is enough
  ([[04 Step 4 - Grass Layer]]).
- Random pick per point is the weighted selector's job; multiple `In`
  connections are allowed (the grass spawner takes ground grass **and**
  rock tufts, [[05 Step 5 - Clumps Near Trees]]).

## Instanced Skinned Mesh Spawner (learn: trees/shrubs)

- For **skinned** vegetation (PVE trees with wind).
- Mesh comes from the point's `SkinnedMeshPath` tag
  ([[nodes/Add Attribute]]) — one spawner, any species mix
  ([[01 Step 1 - Density and Tag]]).
- `bApplyMeshBoundsToPoints=false` in the real graphs — don't let bounds
  override authored point scales.

## Why spawners stay in the MAIN graph

The mesh/material settings live in **inner sub-objects** of the node
(`…SpawnRocks.PCGStaticMeshSpawnerSettings_1.PCGMeshSelectorWeighted_0`)
that **cannot be carried across asset boundaries**. A subgraph that spawned
would ship its points but lose its meshes — so modules emit points, the
orchestrator spawns
([[17 Modular PCG via MCP#3. Rules that make PCG subgraphs modular|rule 1]]).

## Verify hook

Each spawner logs per generation:
`Added N instances of '<mesh>'` in `LogPCG` — the ground-truth count for a
regenerate, read via `LogsToolset.GetLogEntries`
([[17 Modular PCG via MCP#8. Verify like we did (no eyeballing first)]]).
If points exist but no line appears, the spawner's selector is empty — not
the upstream graph's fault.
