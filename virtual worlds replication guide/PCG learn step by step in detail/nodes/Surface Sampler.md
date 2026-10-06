---
tags: [pcg, unreal, pcg-node]
---
# Surface Sampler

**What it is:** the **density engine**. Covers a given **Surface** input with
points at a density specified in *real-world units* — `pointsPerSquaredMeter`
— and drops the points onto that surface.

**In the learn graph:** 10 instances (`S1_Sample … S10_Surf`), one per
layer/step. It's the node that decides *how much stuff exists*.

## Density is in REAL-WORLD units

- `0.03/m²` ≈ 5.8 m grid (trees) · `0.035` shrubs · `0.025` rocks · `0.12`
  floor rocks · `1.0/m²` grass · `1.5/m²` moss.
- Scale the volume up → footprint grows → **point count grows to match,
  spacing stays identical**. This is the master-switch behaviour from
  [[00 PCG Learn Node Map]].

## Pins

- `Surface` (in) — usually [[nodes/World Ray Hit Query]] output; in
  [[10 Step 10 - Scatter on a Mesh|step 10]] it's a mesh's reconstructed
  surface via [[nodes/Get Actor Data]].
- `Out` — points carrying position + surface metadata (`ImpactNormal` etc.).

## Key params seen in the graphs

| Param | Values used | Note |
|---|---|---|
| `pointsPerSquaredMeter` | 0.01 – 10 | the whole knob |
| `pointExtents` | `(300,100,3)` … `(80,80,80)` | makes fat "cookie" points for [[nodes/Distance]]/Difference work |
| looseness | 0 = square grid | step 1 shows the grid on purpose; `S6_Sample2` uses 0.75 |
| `bUnbounded` | true in `S10_Surf` | sample the input surface, don't clip to the volume |

> [!warning] The volume still sets the stage
> Points appear where **volume ∩ surface** is. A sampler with no surface
> under the volume emits nothing — "empty graph" is usually "no terrain
> under the box", not a broken node.

> [!tip] Point count discipline
> 200×200 m at 1/m² = 40 000 points. Grass at 10/m² (real `SG_GroundCover`)
> only survives because the course volume is small — check `Added N
> instances` in the log ([[17 Modular PCG via MCP#8. Verify like we did (no eyeballing first)]]).

Used in: [[01 Step 1 - Density and Tag|1]]–[[06 Step 6 - Float and Snap|6]],
[[07 Step 7 - Road Cut|7]], [[10 Step 10 - Scatter on a Mesh|10]] · all
vegetation modules in [[PCG_ScatterMesh - Module Map]].
