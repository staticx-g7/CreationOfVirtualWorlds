---
tags: [pcg, unreal, tutorial]
---
# Step 1 — Density and Tag

**Strip: 0 m (at the volume).** The smallest meaningful PCG loop: *sample →
tag → spawn*. Everything else in the graph is decoration on top of this.

```
S6_Ground ──Surface──► S1_Sample ──Out──► S1_Tag ──Out──► S1_Spawn
```

| Node | Type | Configured with |
|---|---|---|
| `S1_Sample` | [[nodes/Surface Sampler]] | `pointsPerSquaredMeter=0.03` (~5.8 m spacing), `pointExtents=(300,100,3)` |
| `S1_Tag` | [[nodes/Add Attribute]] | writes `SkinnedMeshPath = PVE_Conifer_01` (SoftObjectPath) |
| `S1_Spawn` | [[nodes/Spawners (Static and Instanced Skinned)|Instanced Skinned Mesh Spawner]] | reads the `SkinnedMeshPath` tag to pick the mesh |

## What each node is for here

1. [[nodes/Surface Sampler]] **is the density engine**: it covers the
   volume's footprint with ~0.03 points per **real-world m²** — looseness 0
   makes a perfect square grid (on purpose: you should SEE the grid in this
   step).
2. [[nodes/Add Attribute]] writes which mesh each point should become. The
   spawner doesn't know any meshes yet — the *point carries its own mesh
   path* (this is the tag pattern from [[17 Modular PCG via MCP#3. Rules that make PCG subgraphs modular|rule 1]]).
3. The [[nodes/Spawners (Static and Instanced Skinned)|spawner]] consumes the
   tag and instances `PVE_Conifer_01` on every point.

> [!warning] No Projection yet — by design
> Step 1 has **no [[nodes/Projection]]**. Points only sit on the surface
> because the Surface Sampler itself drops them on the ground rays. Once a
> later step moves points sideways (jitter, offset), that's when you must
> re-snap — see [[06 Step 6 - Float and Snap]].

## Try it

- Regenerate → a perfect grid of identical conifers at the volume.
- Scale the volume up → same spacing, **more trees** (count grows with area).
- Change `S1_Tag`'s mesh path to the deciduous tree → the whole strip swaps
  species: one node = whole forest identity.

Next: [[02 Step 2 - Randomise]]
