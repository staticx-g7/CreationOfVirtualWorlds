---
tags: [pcg, unreal, pcg-node]
---
# Random Choice

**What it is:** a per-point coin flip with two outputs. `Chosen` continues,
`Discarded` — if unwired — simply **stops**: that point is deleted.

**In the learn graph:** `S3_Half` in [[03 Step 3 - Break the Grid]] —
default 50 %, thins the jittered grid to uneven density.

## The two uses

1. **Thinning** — drop half your points; leftover patches read natural
   where the grid didn't. (Wire only `Chosen`.)
2. **Splitting one stream into two variants** — the real pattern:
   `SG_Trees`'s `SpeciesSplit` sends `Chosen` → conifer tag, `Discarded` →
   deciduous tag. Two species, one sampler, one [[nodes/Add Attribute]] per
   branch ([[PCG_ScatterMesh - Module Map]]).

## Params

- `bFixedMode=false` → **probability** mode: `probability` = % going to
  `Chosen` (50 default).
- Fixed mode → exact count instead of probability.

> [!tip] Density vs counts
> Want "30 % more shrubs"? Raise the sampler's density (spacing stays
> constant — [[nodes/Surface Sampler]]). Want "every other point"? Random
> Choice. The first is art-directed by area, the second by ratio; mixing
> them up is how "density feels wrong everywhere" bugs start.
