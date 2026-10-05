---
tags: [replication, checklist, moc]
---
# Verification Checklist

Run top to bottom; each box has its **expected output**. 100 % green = you have
replicated the course machine. Last full pass: 2026-10-03.

## Machine
- [ ] `nvidia-smi | head -15` → driver + "RTX …", **no stray processes**
- [ ] `df -h "$HOME" | tail -1` → ≥ 150 GB free
- [ ] `~/comfyui/.venv/bin/python -c "import torch;print(torch.cuda.is_available())"` → `True`

## ComfyUI
- [ ] Server answers: `curl -s localhost:8188/system_stats | grep -o comfyui_version[^,]*` → any **≥ 0.34** (fresh installs 2026-10-04 answer `0.38.0` — newer is fine)
- [ ] TRELLIS.2 native: `curl -s localhost:8188/object_info/Trellis2ShapeStage | head -c 30` → `{"Trellis2ShapeStage"` (**not** `{}`)
- [ ] Weights complete (compare to [[05 TRELLIS.2 Model Weights#The files (reference — sizes match the block above)]]):
      `du -sh ~/comfyui/ComfyUI/models/{diffusion_models,vae,clip_vision,background_removal}` → ≈ 5.3 G / 2 G / 1.2 G / 450 M

## Generation (the real test)
- [ ] Full pipeline ran end-to-end: `ls ~/comfyui/ComfyUI/output/3d/` → ≥ one `.glb` (few MB)
- [ ] `file output/3d/*.glb` → `glTF binary model, version 2`
- [ ] On ≤12 GB cards: you ran the ✅ shape-only route ([[attachments/trellis2_api_workflow_shape_only.json]]) and know **why** textures need ≥16 GB: [[08 VRAM Playbook (12 GB and under)]]
- [ ] On ≥16 GB cards: GLB opens in a viewer with **textures**, not just grey mesh

## Unreal
- [ ] Editor launches from an **absolute** path (pattern in [[09 Install Unreal Engine (Linux)]])
- [ ] `VWClassDemo` opens with 0 plugin errors in the Output Log
- [ ] Outliner in `DemoWorld` shows `Sun · SkyLight · ExponentialHeightFog · Ground · PropSlot_00–07`
- [ ] One AI-generated GLB imported and placed in a slot

## MCP 5.8 native server
- [ ] Initialize handshake on `http://127.0.0.1:8000/mcp` returns a session id (curl recipe in [[11 Unreal MCP Setup#4. Verify the server]])
- [ ] `tools/list` reports the toolset inventory (course set: **831 tools**)
- [ ] `opencode mcp list` → `unreal58 connected`
- [ ] Agent can spawn an actor (`MCP_Probe` cube appears in Outliner)

## Data pipeline
- [ ] `python3 validate_dataset.py --dataset <your dataset dir>` → `0 errors`
- [ ] `head -1 <dataset>/metadata.jsonl | python3 -m json.tool` → valid JSON

## Done
All green → you are course-ready. Anything red → [[14 Troubleshooting Field Guide]]
first, tutor second. Back to [[00 Start Here]].
