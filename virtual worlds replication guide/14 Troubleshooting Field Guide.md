---
tags: [replication, troubleshooting]
---
# Troubleshooting Field Guide

Every entry is a **true story from the 2026-10-03 build** — that's why some
read like jokes. Order ≈ how much time each one stole.

## 1. `pkill` killed my own shell (twice)
`pkill -f "main.py --listen"` terminated… the shell running the pkill, because
that shell's *own command line* contains the pattern (the relaunch text later
in the same one-liner!). The `main[.]py` bracket trick doesn't save you when
your command also contains the literal launch string.
**Fix:** kill in one command (`pkill -f "port 818[8]"`), relaunch in the *next*.

## 2. `Project file not found` — editor exits instantly
The Linux editor binary needs the **absolute** `.uproject` path; relative
paths fail even from the project's own folder. Always:
`UnrealEditor "/full/abs/path/Project.uproject" -stdout`.

## 3. The invisible 1.7 GB thief
Two OOMs in a row looked like "flags didn't work". They did — but the **Unreal
Editor left open from an earlier module held 1.7 GB**, and the ComfyUI error
message only counts *torch's* allocations ("allocated 7.16 GiB" while the card
was genuinely full of other things).
**Fix:** `nvidia-smi --query-compute-apps=pid,used_memory --format=csv`
before blaming the model. Close the editor during AI runs.

## 4. The TRELLIS.2 OOM cascade

> [!failure] GUI template dies in `VaeDecodeShapeTrellis` after minutes of sampling
> The shipped template is booby-trapped for 12 GB machines: the model switch
> defaults to **false** (Pixal3D branch) and the upsample node defaults to
> **1536**. Set switch=true, upsample=1024, close UE — then expect the *bake*
> wall later, which is the note 08 route instead. Measured: allocated 8.41 GiB,
> requested 2.47 GiB, limit 11.68. (Run 8, [[08 VRAM Playbook (12 GB and under)]].)
Four failed runs mapped a whole memory cliff — solved as a ladder, not a flag.
Decision tree + measurements: [[08 VRAM Playbook (12 GB and under)]].

## 5. Python-in-UE-5.7 API traps
- `unreal.EditorLevelLibrary.get_level_actors` — **doesn't exist** →
  `unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()`
- no `unreal.SkyLightActor` → the class is `unreal.SkyLight`, component via
  `get_component_by_class(unreal.SkyLightComponent)`
- components generally: `actor.get_component_by_class(...)`, not attribute spelunking
**Move:** anything API-drift-y → verify with `dir(unreal.X)` in the Python console
before writing it into a script. [[10 Create the Demo Project#3. Create DemoWorld (scripted, not clicky)]]

## 6. MCP `execute_script` returns no output
*(legacy ≤ 5.7 bridge only — `execute_script` is an `mcp-unreal` tool; the
5.8 native server has no such tool)*
The bridge answers `{success: true}` and swallows `print()`. Editor-side output
lands in LogPython/LogMCPUnreal — read it with the MCP **`get_output_log`**
tool (pattern-match your own marker string).

## 7. HuggingFace: the repo is `TRELLIS.2` with a dot
`Comfy-Org/TRELLIS_2` → 404 with a bland `n/a`. One character, one wasted
detour. Canonical list: [[05 TRELLIS.2 Model Weights]].

## 8. Template/model plumbing oddities
- The `comfyui-workflow-templates` pip package is a **stub** — templates are
  fetched from GitHub by the UI on demand. `GET /api/templates` returning
  nothing is **normal**, not a broken install.
- No internet in the classroom? Pre-stage the template JSON (GitHub
  `Comfy-Org/workflow_templates`) into the UI once, beforehand.
- Input image from the web failed (`HTML document` from Wikimedia): networks
  can bot-block. Use **your own renders/photos** — also better Trellis inputs
  anyway (single object rule: [[06 Your First 3D Model (GUI)#1. Input image rules (make or break)]]).

## 9. System Python too new for torch
Our distro shipped Python 3.14; torch wheels didn't exist for it. `uv venv
--python 3.12` solved it in one line: [[02 Linux System Setup#3. Fast Python env manager (`uv`)]].

## 10. UE editor dies of `VK_ERROR_DEVICE_LOST` ~25 s after launch
Measured 2026-10-04: two launches passed `-opengl4`, both Vulkan-crashed with
`VK_ERROR_DEVICE_LOST` (`TerminateOnGPUCrash`) about 25 s in, mid-UI-draw. The
known-good launch (Oct 3 and re-verified same evening) passes plain `-stdout`
and survives. UE 5.7's Linux editor is **Vulkan-only** — `-opengl4` is stale
Windows-era advice and the flag never appears in our launcher; do not add it.
If it ever bites you: drop the flag, relaunch with `-stdout`, and glance at
`nvidia-smi` first — the editor needs its ~1.9 GiB (see §3), so make sure
ComfyUI's queue is idle. The project, maps and plugin were innocent both times;
`Saved/Logs/<Project>.log` always names the real killer — read the tail.

## 11. Anything else 3D-related
Start at [[08 VRAM Playbook (12 GB and under)]]; then the course vault's own
`Troubleshooting.md` (module-scoped failures: import, PCG, NDI, sequencer).
