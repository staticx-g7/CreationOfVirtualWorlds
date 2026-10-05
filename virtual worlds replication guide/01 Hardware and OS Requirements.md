---
tags: [replication, logistics]
---
# Hardware and OS Requirements

Verified platform: **Ubuntu (Nvidia proprietary driver), RTX 4080 Laptop GPU
12 GB, 32 GB RAM, ~160 GB free disk** on 2026-10-03.

## Minimum vs comfortable

| Resource | Bare minimum | Comfortable | Where it bites |
|---|---|---|---|
| GPU VRAM | 8 GB (Nvidia) | 12 GB+ | TRELLIS.2 upsample stage hard-mins 1024³ — see [[08 VRAM Playbook (12 GB and under)]] |
| System RAM | 16 GB | 32 GB | model staging with `--novram` |
| Disk | **150 GB** | 250 GB | UE install ~26 GB + weights ~9–21 GB + outputs; (+**550 GB more** only if you extract City Sample — [[12 City Sample on Linux — Reality Check]]) |
| CPU | 4 cores | 8+ | mesh decimation, video encode |

## Check your machine (Linux)
```bash
nvidia-smi | head -15                    # driver + GPU + free VRAM
df -h "$HOME" | tail -1                  # free disk
free -g | head -2                        # RAM
python3 --version                        # any 3.10–3.12 is fine
```

> [!warning] The Nvidia driver matters more than anything else
> We install **torch with CUDA 13 wheels** — that needs a recent proprietary
> driver (`nvidia-smi` must work!). If it doesn't, fix that first:
> [[02 Linux System Setup]]. An AMD/Intel GPU will *not* follow this guide
> (torch-CUDA only); Windows students follow [[04 Install ComfyUI (Windows)]].

## OS routes
- **Linux (this guide's primary path):** everything verified — [[02 Linux System Setup]]
- **Windows 10/11:** ComfyUI + weights + Unreal are fully supported; MCP bridge
  works via the official Epic ModelContextProtocol plugin instead (UE 5.8+) —
  marked where routes diverge.
- **macOS:** ❌ not supported for this course stack (CUDA).

Next: [[02 Linux System Setup]]
