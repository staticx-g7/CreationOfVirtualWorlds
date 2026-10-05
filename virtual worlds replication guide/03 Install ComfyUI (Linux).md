---
tags: [replication, comfyui, linux]
---
# Install ComfyUI (Linux)

Verified 2026-10-03 (ComfyUI 0.36.0, venv Python 3.12, torch 2.14+cu130,
RTX 4080 Laptop). ~30 min.

> [!note] Already have ComfyUI?
> Skip to verification below, then check you have [[05 TRELLIS.2 Model Weights]].
> **TRELLIS.2 is native in ComfyUI core since Aug 2026** (v0.34+) — you do NOT
> need any custom nodes. An old install (< 0.34) is the #1 silent failure.

## 1. Clone + venv + dependencies
```bash
mkdir -p ~/comfyui
git clone https://github.com/comfyanonymous/ComfyUI ~/comfyui/ComfyUI
cd ~/comfyui
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130
uv pip install -r ComfyUI/requirements.txt
```

## 2. GPU sanity check (never skip)
```bash
~/comfyui/.venv/bin/python -c "import torch; \
  print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
# expect: 2.1x.x+cu130 True NVIDIA GeForce RTX ...
```

## 3. Launch — with the 12 GB flags from day one
```bash
cd ~/comfyui/ComfyUI && ../.venv/bin/python main.py \
    --listen 127.0.0.1 --port 8188 \
    --lowvram --disable-smart-memory --reserve-vram 2 &
```
Why these exact flags: [[08 VRAM Playbook (12 GB and under)]]. On ≥16 GB cards
you can drop them.

## 4. Verify
```bash
curl -s http://127.0.0.1:8188/system_stats | head -c 200
# expect JSON: "comfyui_version": "≥0.34" (fresh 2026-10-04 install: 0.38.0) ...
```
Browser: **http://127.0.0.1:8188** → you should see the node UI.
Also confirm TRELLIS.2 nodes exist (proves core version is new enough):
```bash
curl -s http://127.0.0.1:8188/object_info/Trellis2ShapeStage | head -c 120
# expect: {"Trellis2ShapeStage": {...   (NOT {} )
```

## 5. Desktop launcher (optional, what we ship)
[[attachments/ComfyUI.desktop]] → copy to `~/Desktop`, `chmod +x`. It launches
the server with the right flags and opens the browser.

**Killing the server — the footgun that bit us twice:**
```bash
pkill -f "port 818[8]"        # brackets stop the pattern matching the pkill
                              # command itself... but do NOT put the kill and
                              # the relaunch in the same shell line, or your
                              # wrapper's own cmdline matches and kills ITSELF.
```
Full story: [[14 Troubleshooting Field Guide#1. `pkill` killed my own shell (twice)]].

Next: [[05 TRELLIS.2 Model Weights]]
