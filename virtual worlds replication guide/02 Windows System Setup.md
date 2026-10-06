---
tags: [replication, windows, setup]
---
# Windows System Setup

One-time OS prep. Windows 11 assumed; snippets are **PowerShell** (5.1+). Same
endpoint state as [[02 Linux System Setup]]; differences only.

## 1. Nvidia driver (must work before anything else)
```powershell
nvidia-smi        # prints a table? skip this section
```
Otherwise install the latest **Game Ready or Studio driver** from
https://www.nvidia.com/drivers (or via NVIDIA App → Drivers) — CUDA 13 wheels
want a recent driver. Reboot, re-run `nvidia-smi`.
> [!tip] Hybrid-graphics laptops (Intel/AMD iGPU + Nvidia)
> Windows usually picks the Nvidia GPU automatically for heavy apps; verify in
> Task Manager → Performance, or force it per app under Settings → System →
> Display → Graphics. **AI generation and the editor must run on the Nvidia
> GPU** — check the process appears in `nvidia-smi`.

## 2. Base tooling (`winget` ships with Windows 11)
```powershell
winget install -e --id Git.Git
winget install -e --id GitHub.GitLFS
winget install -e --id Gyan.FFmpeg
winget install -e --id Microsoft.VisualStudio.2022.BuildTools --override "--quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```
- **MSVC (VS Build Tools C++ workload)** replaces Linux's `clang`/`lld`: this is
  what Unreal uses to compile plugin C++ (incl. the toolset work in
  [[11 Unreal MCP Setup]]).
- **Git LFS** — the demo project's `Content/` assets live in LFS; without it a
  clone yields useless pointer files
  ([[10 Create the Demo Project#0. Shortcut — clone the finished project (skip sections 1–3)]]).
- Long paths — UE work trees bite here on Windows:
```powershell
git config --global core.longpaths true
git lfs install        # one-time
```

## 3. Fast Python env manager (`uv`)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
uv --version                  # reopen the shell if not on PATH yet
uv python install 3.12        # torch target; system 3.13/3.14 is too new
```
Same rationale as [[02 Linux System Setup#3. Fast Python env manager (`uv`)]].

## 4. Disk check
```powershell
Get-PSDrive C | Select-Object Free     # need ≥150 GB free — see [[01 Hardware and OS Requirements]]
```

Done? → [[04 Install ComfyUI (Windows)]]
