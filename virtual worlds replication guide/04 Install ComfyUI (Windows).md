---
tags: [replication, comfyui, windows]
---
# Install ComfyUI (Windows)

Same endpoint state as [[03 Install ComfyUI (Linux)]]; differences only.

## 1. Install
Easiest: **ComfyUI Desktop installer** from https://comfy.org/download
(it manages Python + CUDA torch for you). Manual/portable route:
```powershell
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
python -m venv venv          # Python 3.12 (not 3.13/3.14!)
venv\Scripts\activate
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130
pip install -r requirements.txt
```

## 2. Launch (with low-VRAM flags for ≤12 GB cards)
```powershell
venv\Scripts\python main.py --lowvram --disable-smart-memory --reserve-vram 2
```
Portable zip users: edit `run_nvidia_gpu.bat` and add those flags after
`main.py`. Reasoning: [[08 VRAM Playbook (12 GB and under)]].

## 3. Verify
Browser http://127.0.0.1:8188 , then either in a second terminal:
```powershell
curl http://127.0.0.1:8188/object_info/Trellis2ShapeStage
```
…or in the UI search (press `n`): type **Trellis2** — you should find
`Trellis2ShapeStage`, `Trellis2TextureStage`, etc. Missing → update ComfyUI;
TRELLIS.2 is core since Aug 2026 (v0.34+), **no custom nodes exist anymore**.

## 4. Weights
Follow [[05 TRELLIS.2 Model Weights]] — same files, same folder layout, just
under `ComfyUI\models\` (Desktop app: Settings → Dev → model folder path).

Windows is also the **recommended student path for City Sample and NDI**
(both Windows-first) — see [[12 City Sample on Linux — Reality Check]].

Next: [[05 TRELLIS.2 Model Weights]]
