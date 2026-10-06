---
tags: [replication, unreal, windows]
---
# Install Unreal Engine (Windows)

Same endpoint state as [[09 Install Unreal Engine (Linux)]]; differences only.
Windows is Unreal's native home: both launcher and source builds run smoother
than Linux here, and City Sample / NDI / most Marketplace packs are
Windows-only anyway ([[12 City Sample on Linux — Reality Check]]).

## Route A — Epic Games Launcher (recommended)
1. Install the launcher from https://www.unrealengine.com → **Unreal Engine →
   Download**.
2. Library → Engine → install **Unreal Engine 5.7.x** (~26 GB).
3. In the install **Options**: keep C++/source access + engine headers —
   compiling ANY C++ plugin (incl. [[11 Unreal MCP Setup]]) needs them. On
   Windows this is also the cheapest insurance there is.

Result: `Engine\Build\BatchFiles\Build.bat` exists → that's the door to
everything custom.

## Route B — GitHub source build (only if you need 5.8)
```powershell
# link your Epic account to GitHub first (accounts.unrealengine.com → Connections)
git lfs install
git clone -b 5.8 https://github.com/EpicGames/UnrealEngine D:\UnrealEngine-5.8
cd D:\UnrealEngine-5.8
.\Setup.bat                       # downloads dependencies, 30–60 min
.\GenerateProjectFiles.bat
.\Engine\Build\BatchFiles\Build.bat UnrealEditor Win64 Development
```
Hours of build time, 100+ GB free disk. Windows source builds are the most
reliable of all platforms — prefer this route on Windows if you need 5.8.
(`core.longpaths true` from [[02 Windows System Setup]] is mandatory for the clone.)

## Launch pattern
Double-clicking `Project.uproject` works on Windows (pick the engine version);
from CLI:
```powershell
& "<ENGINE>\Engine\Binaries\Win64\UnrealEditor.exe" "<ABS>\VWClassDemo\VWClassDemo.uproject"
```
> [!warning] Windows launch notes
> 1. Still use an **absolute** `.uproject` path
> 2. No `DISPLAY`/`setsid` dance, no `-opengl4`/`-vulkan` needed — DX12 is the
>    default and the good path (those flags are Linux troubleshooting levers)
> 3. The **VRAM contract** still applies — close the editor before AI
>    generation: [[08 VRAM Playbook (12 GB and under)]]

Crash dumps land in `<Project>\Saved\Crashes\` (and `%LOCALAPPDATA%\CrashReportClient`).

## Verify
- Window opens; Output Log has no red `LogInit` failures
- Python console works (we script everything in this course):
  `Window → Output Log → Commands: python3 exec("import unreal; print(unreal.EngineUtilsLib)")`

Next: [[10 Create the Demo Project]]
