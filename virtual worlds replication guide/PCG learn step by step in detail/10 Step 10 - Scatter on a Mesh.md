---
tags: [pcg, unreal, tutorial]
---
# Step 10 — Scatter on a Mesh

**The rock demo.** Ground is not the only surface: grab a **normal,
editable level actor's mesh**, sample its surface, and grow moss on it. Move
the rock actor → moss follows on regenerate.

```
LEVEL ACTOR: "SM_Rock_03" tagged "PCG_Learn_Rock" (a plain StaticMesh actor)
S10_Get ──► FilterDataByType_1 ──InsideFilter──Surface──► S10_Surf ──► S10_Var ──► S10_Moss
```

| Node | Type | Configured with |
|---|---|---|
| `S10_Get` | [[nodes/Get Actor Data]] | by tag `PCG_Learn_Rock`, components **ByClass** `StaticMeshComponent`, `alsoOutputSinglePoint` |
| `FilterDataByType_1` | [[nodes/Boundary Helpers (Filter Data, To Point, Make Concrete)|Filter Data – Surface]] | only Surface-typed data may enter the sampler |
| `S10_Surf` | [[nodes/Surface Sampler]] | `1.5` pts/m², **`bUnbounded=true`** — sample the mesh, not the volume |
| `S10_Var` | [[nodes/Transform Points]] | full yaw, scale 0.5–0.75 (pre-divided for the rock's 2× scale) |
| `S10_Moss` | [[nodes/Spawners (Static and Instanced Skinned)|Static Mesh Spawner]] | Wild_Grass VarB/D/F |

## Lessons

1. **Any mesh is terrain to PCG.** [[nodes/Get Actor Data]] reconstructs the
   actor's mesh as PCG **Surface** data — the same data type
   [[nodes/World Ray Hit Query]] produces — so the *same*
   [[nodes/Surface Sampler]] node runs on it.
2. **`bUnbounded=true`** tells the Surface Sampler: don't clip to the volume,
   cover the input surface. Without it the rock's points get trimmed to the
   volume footprint.
3. **Scale pre-division gotcha** (node comment): the rock actor is scaled
   2×, and tuft scales are pre-divided to compensate. Mesh scale flows into
   sampled-point scale — check it before wondering why moss is giant.
4. The actor stays **fully editable and outside PCG ownership** — it isn't
   spawned by the graph, so artists keep moving/rotating it; generation just
   reacts. (Contrast: [[09 Step 9 - The Grove]] where the spline is
   authoring-only too.)

> [!warning] Data-type walls
> The Filter-Data node between `S10_Get` and the sampler isn't decoration —
> the sampler's `Surface` pin refuses data that isn't Surface-typed.
> Boundary conversions are normal; see
> [[nodes/Boundary Helpers (Filter Data, To Point, Make Concrete)]].

Back to [[00 PCG Learn Node Map]] · real-world use: [[PCG_ScatterMesh - Module Map]]
