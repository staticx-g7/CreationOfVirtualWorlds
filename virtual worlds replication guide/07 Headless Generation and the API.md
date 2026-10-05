---
tags: [replication, comfyui, api]
---
# Headless Generation and the API

ComfyUI's HTTP API is how you batch-generate dataset assets (and how this
guide's authors smoke-tested the stack). Server must be running: [[03 Install ComfyUI (Linux)]].

## The five endpoints you need

| What | Command |
|---|---|
| Health | `curl -s localhost:8188/system_stats` |
| Node spec (inputs/types/defaults) | `curl -s localhost:8188/object_info/Trellis2ShapeStage` |
| Submit workflow | `curl -s -X POST localhost:8188/api/prompt -H 'Content-Type: application/json' -d @workflow.json` |
| Poll result | `curl -s localhost:8188/history/<prompt_id>` |
| List errors without running | same POST — validation errors come back as `node_errors` |

> [!tip] The golden debugging loop
> `POST /api/prompt` **validates before running**: wrong/missing inputs come
> back instantly as `node_errors` with `details` (e.g. `received_type(MASK)
> mismatch input_type(IMAGE)`). Edit → POST → read error → repeat. We built a
> 23-node Trellis graph from scratch this way in ~15 minutes, without ever
> opening the UI. Node specs from `/object_info/<Class>` tell you every input
> name, type and default.

## Prompt-graph format (the gotchas that cost us an hour)
A prompt file is `{"prompt": {"<node_id>": {"class_type": ..., "inputs": {...}}}}`:
- Connected inputs are `["<src_node_id>", <output_slot_index>]`
- **Output index 0 = the node's PRIMARY output**, named outputs follow — and
  they don't always match intuition: `RemoveBackground` index 0 is its MASK,
  `BakeTextureFromVoxel` index 0 is an IMAGE, not a mesh. When in doubt:
  `/object_info` → `input`/`output` names.
- Every required widget must be present (missing → `required_input_missing`),
  even if the UI shows a default
- `Trellis2UpsampleStage.target_resolution`: INT, **min 1024**, max 2048

## Shipped workflows (this vault, `attachments/`)
Every node and widget in these JSONs, with defaults and tuning effects:
[[template nodes/00 Node Map]].
| File | What it does | Status on 12 GB |
|---|---|---|
| [[attachments/trellis2_api_workflow_shape_only.json]] | low-res, **no texture bake** — geometry + UVs to GLB | ✅ **passes end-to-end** (the 12 GB route) |
| [[attachments/trellis2_api_workflow_vertexcolor_12gb.json]] | low-res + texture stage, **vertex colors instead of bake** | ✅ **passes end-to-end** (textured 12 GB route, note 08 run 9) |

GUI users: both graphs also ship pre-laid-out for the browser as
[[attachments/trellis2_gui_shape_only_12gb.json]] and
[[attachments/trellis2_gui_vertexcolor_12gb.json]] (File → Open, see note 06).
| [[attachments/trellis2_api_workflow_lowres.json]] | as above + texture bake @1024 | ✗ OOM at `BakeTextureFromVoxel` |
| [[attachments/trellis2_api_workflow_lowres_bake512.json]] | texture bake @512 (control experiment) | ✗ OOM at same node — memory ≠ texture_size |
| [[attachments/trellis2_api_workflow_1024_full.json]] | full quality: upsample + decimate + bake | needs ≳16–24 GB |

All share the same input handling: drop your object photo in `ComfyUI/input/`
and set the `LoadImage` node's `image` value. Full ladder context:
[[08 VRAM Playbook (12 GB and under)]].

## Run one
> [!note] bash syntax below (`$(…)` subshells). In fish: `set PID (curl … | python3 -c …)`
> or just type `bash` first.
```bash
cd ~/comfyui/ComfyUI
IMG=housetest.png        # put your object image into input/ first
# edit the LoadImage node's "image" value in the json, then:
PID=$(curl -s -X POST localhost:8188/api/prompt -H 'Content-Type: application/json' \
      -d @"$VAULT/attachments/trellis2_api_workflow_lowres.json" \
      | python3 -c "import json,sys;print(json.load(sys.stdin)['prompt_id'])")
echo "queued $PID"
while true; do H=$(curl -s localhost:8188/history/$PID); \
  [ "$H" != "{}" ] && { echo "$H" | python3 -m json.tool | head -40; break; }; sleep 15; done
ls -la output/3d/
```
(`$VAULT` = your checkout of this replication guide.)

## Batch pattern (course: 20 assets in a row)
Loop photos → patch the `LoadImage.image` field with `python3 - <<EOF json` →
POST each → poll each. Keep the server up; watch `nvidia-smi` the first time
through to make sure nothing else grabs VRAM mid-run.

Next: [[08 VRAM Playbook (12 GB and under)]]
