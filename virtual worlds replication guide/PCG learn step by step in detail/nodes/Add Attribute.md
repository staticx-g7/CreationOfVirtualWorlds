---
tags: [pcg, unreal, pcg-node]
---
# Add Attribute

**What it is:** writes one named attribute onto every point. In this project
it has two jobs: **mesh tags** and **constant transforms/vectors for other
nodes to consume**. 9 instances in the learn graph, 3+ in real modules.

## Job 1 — the mesh-path tag pattern

```
outputTarget = "SkinnedMeshPath"
attributeTypes.type = SoftObjectPath
softObjectPathValue = /ProceduralVegetationEditor/.../PVE_Conifer_01
```

The point now *carries its own mesh*. An
[[nodes/Spawners (Static and Instanced Skinned)|Instanced Skinned Mesh Spawner]]
with `useMeshPathTag` reads it — so species variation is **data**, one node
([[01 Step 1 - Density and Tag|step 1]]). `SG_Trees` splits two species off
one stream via [[nodes/Random Choice]] and tags each branch differently.

> [!note] Attribute tags survive subgraph boundaries
> `SkinnedMeshPath`, `WaterDir`, `ImpactNormal` all cross subgraph pins —
> that's why spawners can live in the main graph while tagging happens in a
> module ([[17 Modular PCG via MCP#3. Rules that make PCG subgraphs modular|rule 1]],
> [[17 Modular PCG via MCP#8. Verify like we did (no eyeballing first)|verify step 2]]).

## Job 2 — constant values as attributes

`S8_OffL/S8_OffR`: `outputTarget="LocalOff"`, type **Transform**,
location `(0,∓600,0)` — a constant side-offset that
[[nodes/Attribute Transform Op]] composes onto `$Transform`. Storing a value
as an attribute (instead of hard-coding it in a transform) means it can be
computed, overridden per-point, or reused by several nodes.

## Job 3 — rotators from vectors

Real modules (`SG_RoadFlagstones`, `SG_WaterRibbon`) pair it with the
*Make Rotator Attribute* mode: `inputSource1=RoadDir/WaterDir`,
`inputSource2=ImpactNormal`, `operation=MakeRotFromXZ`,
`outputTarget=$Rotation` — yaw to the path tangent, tilt to the ground
normal, in one write.

> [!tip] inputSource vs outputTarget
> Leave `inputSource=None` and set `attributeTypes` → constant write.
> Set `inputSource` → copy/convert an existing attribute.
