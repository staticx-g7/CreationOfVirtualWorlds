---
tags: [pcg, unreal, tutorial]
---
# Step 4 — Grass Layer

**Strip: +90 m.** Switch from skinned trees to **static-mesh foliage**: the
whole point is that grass needs *no mesh tag* — the mesh list lives inside
the spawner node.

```
S6_Ground ──Surface──► S4_Sample ──► S4_Move ──► S4_Tumble ──► S4_Proj ──► S4_Spawn
```

| Node | Type | Configured with |
|---|---|---|
| `S4_Sample` | [[nodes/Surface Sampler]] | `pointsPerSquaredMeter=1` (real grass ≈ 1/m²) |
| `S4_Move` | [[nodes/Transform Points]] | absolute +90 m; also `scaleMax=(10,10,10)` |
| `S4_Tumble` | [[nodes/Transform Points]] | pitch/roll ±15°, full yaw, scale 0.4–1.3, reseed |
| `S4_Proj` | [[nodes/Projection]] | snap onto `S6_Ground` |
| `S4_Spawn` | [[nodes/Spawners (Static and Instanced Skinned)|Static Mesh Spawner]] | **weighted selector, 4 grass variants, equal weight** |

## Lessons

1. **Two spawner families.** Trees used
   [[nodes/Spawners (Static and Instanced Skinned)|Instanced Skinned Mesh Spawner]]
   + `SkinnedMeshPath` tag. Grass uses
   [[nodes/Spawners (Static and Instanced Skinned)|Static Mesh Spawner]] with
   a `PCGMeshSelectorWeighted` **inside** the node — points carry no mesh
   info here. (This is exactly why [[17 Modular PCG via MCP#3. Rules that make PCG subgraphs modular|rule 1]]
   keeps spawners in the main graph: those inner selector objects **cannot
   cross asset boundaries**.)
2. **Variants need no graph nodes.** Random pick-per-point is the weighted
   selector's job — compare with [[05 Step 5 - Clumps Near Trees]] reusing
   the *same* mesh list on different points.
3. **Tumble is what makes billboards work** — grass tufts are flat-ish; a
   random pitch/roll kills the "all blades same angle" tell.

> [!warning] 1/m² is already a lot
> The volume at scale 40 = 200×200 m = **40 000 points** on this strip alone.
> Surface Sampler counts scale with area — see
> [[nodes/Surface Sampler#Density is in REAL-WORLD units]].

Next: [[05 Step 5 - Clumps Near Trees]]
