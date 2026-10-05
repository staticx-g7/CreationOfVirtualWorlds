---
tags: [replication, unreal, citysample, status]
---
# City Sample on Linux — Reality Check

**Status: partially blocked — read this before planning anything around City
Sample.** The course teaser (walking a Metropolis-scale city, sensor-grid data)
still works via the instructor's captures; full local replication on Linux is
in progress. Facts verified 2026-10-03 against the actual 2026 City Sample
distribution (112 GB zip).

## What the 2026 release actually is

| Fact | Value | Consequence |
|---|---|---|
| Engine version | `EngineAssociation: "5.8"` | needs UE **5.8** — 5.7 projects won't open it |
| Bundled binaries | **Win64 only** (built 2026-09-10) | Windows: download → unzip → run. That's the supported path |
| Linux support | declared in `TargetPlatforms` but **no Linux binaries shipped** | Linux = compile the project yourself |
| Size | 112 GB zip → **~550 GB extracted** | check `df -h` twice |
| Extra Linux preconditions | UE 5.8 **source build** for Linux (GitHub clone, `make UnrealEditor`, hours + 100 GB) **and** Epic-account↔GitHub linkage | the real bottleneck |

## The three routes

### A. Windows sender (recommended for students)
Download from Fab on a Windows box → unzip → Play. 5.8 editor included.
This is what the course assumes if you want the full city live.

### B. Linux, full build (instructor route — in progress)
1. UE 5.8 from source per [[09 Install Unreal Engine (Linux)#Route B — GitHub source build (only if you need 5.8 — see [12 City Sample on Linux — Reality Check])]]
2. Extract the project (~550 GB free needed)
3. `Build.sh CitySampleEditor Linux Development -Project=…` (long)
4. Expect engine-plugin gaps to patch along the way — treat as an adventure,
   not a workshop step

### C. Course fallback (what the timetable actually uses)
Instructor-captured city footage + `VWClassDemo` for hands-on modules —
identical learning outcomes for M7's dataset lessons:
[[13 Dataset Pipeline Tools]] consumes captured footage either way.

## NDI status (the M6 streaming module)
- UE **NDI plugin: Windows-only** in practice (2026 Fab plugin Linux support
  unconfirmed); no NDI runtime on our Linux box, and distro ffmpeg ships
  without `ndi` filters
- **Course decision: run the NDI demo on the Windows sender** (City Sample
  box) → `ndi-rs`/OBS or ffmpeg-NDI grabs the stream; Linux students receive
  the recorded multicast for the M8 dataset step
- Retest a Linux sender (Fab plugin) when the engine is on 5.8 — track here.
