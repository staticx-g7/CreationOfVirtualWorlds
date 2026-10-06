---
tags: [pcg, unreal, pcg-node]
---
# Boundary Helpers (Filter Data, To Point, Make Concrete)

**What they are:** the plumbing trio that appears wherever data crosses a
type boundary (subgraph pins) or a node's typed input. Newbies delete them
and "break" the graph — they're **required conversions**, not clutter
([[17 Modular PCG via MCP#3. Rules that make PCG subgraphs modular|rule 3]]).

## The trio

| Node | Job | Where you see it |
|---|---|---|
| **Filter Data – X** (Surface/Spline/Point…) | passes only data of type X | every subgraph `Surface`/`Spline` input; `FilterDataByType_1` before [[10 Step 10 - Scatter on a Mesh|step 10]]'s sampler |
| **To Point** | tagged/generic data → **concrete points** a spawner can eat | all 11 `ToPoint_N` in [[PCG_ScatterMesh - Module Map]] between subgraph outputs and spawners |
| **Make Concrete** | materializes abstract data (spawner/projection target needs concrete) | feeding `Projection Target` pins everywhere; `SG_Trees` etc. |

## Why data goes "abstract"

Data crossing a subgraph boundary loses its concrete/points flags (the
boundary type is the generic `Spatial`). `ConnectNodePins` over MCP
**auto-inserts** these helpers — leave them in. The learn graph (no
subgraphs) still needs one Filter-Data for the Get-Actor surface, so you
meet them early
([[nodes/Get Actor Data]]).

## Failure modes

- Deleted helper → pin goes grey/red, node executes on nothing, **no error
  line** — "my trees vanished after cleanup" is usually this.
- `Filter Data – Spline` has `InsideFilter` / `OutsideFilter` pins — the
  road's `Spline` output in `SG_RoadCorridor` comes from the *inside* pin.
- Attribute tags (`SkinnedMeshPath`, `WaterDir`) **do** survive these
  conversions — if species/mesh info dies, look elsewhere (spawner
  selector, [[nodes/Add Attribute]]).

Related: [[00 PCG Learn Node Map]] · [[PCG_ScatterMesh - Module Map]]
