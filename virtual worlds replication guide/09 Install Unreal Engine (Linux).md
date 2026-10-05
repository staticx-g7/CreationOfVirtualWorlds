---
tags: [replication, unreal, linux]
---
# Install Unreal Engine (Linux)

Verified with **UE 5.7.4 promoted build, full `Engine/Source` included**, at
`~/Desktop/UnrealEngine/UE_5.7.4` on the course machine. 1–2 h (mostly download).

## Route A — Epic Games Launcher (recommended)
1. **Linux:** Epic's native Linux beta launcher (or install the Windows launcher
   under Bottles/Wine); **Windows:** normal launcher.
2. Install **Unreal Engine 5.7.x** (~26 GB).
3. **Keep `Engine/Source`** in the install options — compiling ANY C++ plugin
   (incl. the MCP plugin in [[11 Unreal MCP Setup]]) needs engine headers.

Result: `UE_5.7/Engine/Build/BatchFiles/Linux/Build.sh` exists → that's the door
to everything custom.

## Route B — GitHub source build (only if you need 5.8 — see [[12 City Sample on Linux — Reality Check]])
```bash
# needs: your Epic account linked to GitHub (accounts.unrealengine.com →
# Connections), then clone (LFS!)
git lfs install
git clone -b 5.8 https://github.com/EpicGames/UnrealEngine ~/UnrealEngine-5.8
cd ~/UnrealEngine-5.8 && ./Setup.sh && ./GenerateProjectFiles.sh
make UnrealEditor            # hours. 100+ GB disk for the build.
```
Prebuilt 5.7 Linux builds exist; 5.8 Linux ships same-day as source only.

## Launch pattern that actually works (learned the hard way)
```bash
DISPLAY=:0 setsid nohup <ENGINE>/Engine/Binaries/Linux/UnrealEditor \
    "<ABSOLUTE/PATH/TO/Project.uproject>" -stdout >/tmp/ue-editor.log 2>&1 &
```
> [!warning] Three launch rules
> 1. **Absolute** `.uproject` path — relative paths give `Project file not
>    found` and an instant exit (bit us)
> 2. Hybrid-graphics laptops may need `prime-run` before the binary, and
>    `-vulkan -graphicsadapter=0` (our course laptop's known-good line)
> 3. The editor is a **VRAM hog** — close it before AI generation:
>    [[08 VRAM Playbook (12 GB and under)]]

## Verify
- Window opens; Output Log has no red `LogInit` failures
- Python console works (we script everything in this course):
  `Window → Output Log → Commands: python3 exec("import unreal; print(unreal.EngineUtilsLib) ")`

Next: [[10 Create the Demo Project]]
