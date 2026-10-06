---
tags: [pcg, unreal, pcg-node]
---
# Filter Attribute Elements by Range

**What it is:** keeps points whose numeric attribute falls inside
`[minThreshold, maxThreshold]`. The act-after-measure half of the distance
cutter, and generally *the* way to thin by any computed value.

**In the learn graph:** `S7_Keep` — `targetAttribute="DistToRoad"`,
`minThreshold=400 cm`, max = ∞ → nothing spawns within 4 m of the road
([[07 Step 7 - Road Cut]]).

## Pins & params

- `In` → `InsideFilter` (kept) and usually an `OutsideFilter` pin — the
  rejected half. Unwire it to delete; wire it to *use* the rejects.
- `minThreshold` / `maxThreshold` — type-sensitive (here Double 400 = 4 m).
  Works on any float/int attribute, not just distances: slope, density,
  custom scores.

## Patterns

- **Road/mask clearance:** `Distance` → keep > width/2
  ([[nodes/Distance]] covers the pairing).
- **Slope-selective vegetation:** sample normal Z, keep flat-ish points —
  same two nodes, different attribute.
- **Density falloff:** store distance-to-edge, keep < r.

> [!warning] It deletes silently
> A typo'd attribute name or a type mismatch (float vs Double) filters
> *everything* or *nothing* with no warning. Verify with
> `GetNodeDataView` one node upstream — check the attribute exists and its
> unit (cm, not m!)
> ([[17 Modular PCG via MCP#8. Verify like we did (no eyeballing first)]]).
