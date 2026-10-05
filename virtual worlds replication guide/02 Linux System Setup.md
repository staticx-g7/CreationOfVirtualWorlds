---
tags: [replication, linux, setup]
---
# Linux System Setup

One-time OS prep. Ubuntu 22.04/24.04 assumed; adapt package names elsewhere.

## 1. Nvidia driver (must work before anything else)
```bash
nvidia-smi        # if this prints a table, skip this section
# Ubuntu: install a recent proprietary driver (550+; CUDA 13 wheels want new)
sudo ubuntu-drivers install        # or: sudo apt install nvidia-driver-580
sudo reboot                        # then re-run nvidia-smi
```
> [!tip] Laptops with hybrid graphics (Intel/AMD iGPU + Nvidia)
> Our course laptop uses `prime-run <cmd>` to force the Nvidia GPU. If your
> external display is wired to the iGPU, run GUI apps accordingly, but always
> run **AI generation and the editor on the Nvidia GPU** — check with
> `nvidia-smi` (the process must appear in its list).

## 2. Base tooling
```bash
sudo apt update
sudo apt install -y git curl wget unzip build-essential clang lld make cmake \
                    python3-venv ffmpeg
```
- `clang`/`lld`/`make`/`cmake`: Unreal needs them (plugin compiles — [[11 Unreal MCP Setup]])
- `ffmpeg`: video/frame tooling — [[13 Dataset Pipeline Tools]]

## 3. Fast Python env manager (`uv`)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env        # or re-open the shell
uv --version
```
We use `uv` because the system Python (3.14 on our box!) is **too new for
torch** — `uv` grabs a matching 3.12 for the ComfyUI venv in seconds.

## 4. Disk check
```bash
df -h "$HOME" | tail -1        # need ≥150 GB free — see [[01 Hardware and OS Requirements]]
```

Done? → [[03 Install ComfyUI (Linux)]]
