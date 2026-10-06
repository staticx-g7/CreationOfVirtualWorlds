---
tags: [pcg, unreal, tutorial]
---
# Step 6 — Float and Snap

**Strip: +150 m.** The snap demonstration: the whole strip is deliberately
launched **150 m into the air**, and one [[nodes/Projection]] per branch is
the only thing keeping it on the ground. Disable it (**D**) and regenerate —
the forest hangs in the sky. That single toggle *is* the lesson.

```
S6_Sample ──► S6_Move ──► S6_Vary (FLOAT +150 m) ──► S6_Tag ──► S6_ProjT ──► S6_Spawn
S6_Sample2 ─► S6_Lawn  (FLOAT +150 m too)        ──────────► S6_ProjG ──► S6_SpawnG
                    ▲ every Projection pulls from S6_Ground (World Ray Hit Query)
```

| Node | Type | Configured with |
|---|---|---|
| `S6_Sample` | [[nodes/Surface Sampler]] | `0.01`/m² |
| `S6_Vary` | [[nodes/Transform Points]] | offset `(0,0,15000)` **absolute** — the float |
| `S6_Lawn` | [[nodes/Transform Points]] | offset `(15000,0,15000)` absolute — parks + floats |
| `S6_ProjT` / `S6_ProjG` | [[nodes/Projection]] | `bProjectPositions`, target = `S6_Ground` surface |
| `S6_Spawn` / `S6_SpawnG` | [[nodes/Spawners (Static and Instanced Skinned)|skinned / static spawner]] | spawned **after** projection, so they land |

## Lessons

1. **Spawn AFTER the snap.** The spawners hang off the Projection outputs —
   mesh instances copy the *point's* final transform. Spawn before snapping
   and you've built furniture in mid-air.
2. **The ground is read once, snapped many times.** All six strips'
   samplers **and** all their Projections consume the single
   [[nodes/World Ray Hit Query]] (`S6_Ground`). One collision read for the
   whole graph — every real module in [[PCG_ScatterMesh - Module Map]] takes
   this as its `Surface` input for the same reason.
3. **Honest limitation (from the node comment):** Projection is
   **nearest-neighbour** against the ray grid. Fine while the volume is a
   sane size (scale ≤ ~5); at extreme scales the ground ray grid is coarse
   relative to terrain and heights drift.

> [!warning] The rule this step encodes
> *A downstream Projection overwrites the Z you just lifted* — and the
> inverse: **lift AFTER projection**. In the real graphs the grass
> `LiftGrass` (+18–35 cm) sits **after** `ProjGrass` for exactly this reason
> ([[17 Modular PCG via MCP#5. Height-placement rules (the expensive lessons)|rule 2]]).

Next: [[07 Step 7 - Road Cut]]
