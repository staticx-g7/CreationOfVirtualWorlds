---
tags: [replication, unreal, project]
---
# Create the Demo Project

The course's Unreal home: **`VWClassDemo`** — a project pre-configured with the
right plugins plus one scripted level (`DemoWorld`: lighting + fog + ground +
8 labelled prop slots) that Day 1 fills with AI assets. 30 min.
Assumes [[09 Install Unreal Engine (Linux)]] (or [[09 Install Unreal Engine (Windows)]]) done.

## 0. Shortcut — clone the finished project (skip sections 1–3)

The course repo ships the completed project as **`VirtualWorldsDemo/`** (same
setup as below, plus PCG content and imported packs), with every `Content/`
asset stored in **Git LFS**:

```bash
git lfs install     # once per machine — installed in [[02 Linux System Setup#2. Base tooling]]
git clone https://github.com/staticx-g7/CreationOfVirtualWorlds.git
cd CreationOfVirtualWorlds/VirtualWorldsDemo
```

PowerShell twin (LFS from `winget install -e --id GitHub.GitLFS`, see
[[02 Windows System Setup#2. Base tooling (`winget`)]]):
```powershell
git lfs install
git clone https://github.com/staticx-g7/CreationOfVirtualWorlds.git
cd CreationOfVirtualWorlds\VirtualWorldsDemo
```

Then open `VirtualWorldsDemo.uproject` with the editor from
[[09 Install Unreal Engine (Linux)]] / [[09 Install Unreal Engine (Windows)]].
`Saved/`, `Intermediate/`, `DerivedDataCache/` are gitignored — a fresh clone
is skeleton + assets only, so the **first launch rebuilds shaders/DDC and is
slow**.

> [!warning] LFS pull size + pointer-file failure mode
> `Content/` is **~3.4 GB over LFS**. If the `.uasset` files come out tiny
> (a few hundred bytes of text), you cloned before `git lfs install` — run
> `git lfs pull` inside the repo. Mind your host's LFS quota (GitHub free
> private = 1 GiB storage/bandwidth).

Sections 1–3 below are how the project was built — read them to understand
what you cloned, then continue at §4 or [[11 Unreal MCP Setup]].

## 1. Project skeleton
Create `VWClassDemo/VWClassDemo.uproject`:
```json
{
  "FileVersion": 3,
  "EngineAssociation": "5.7",
  "Category": "Courses",
  "Description": "Demo project: AI asset import, PCG, footage export, datasets.",
  "Plugins": [
    { "Name": "PCG", "Enabled": true },
    { "Name": "PythonScriptPlugin", "Enabled": true },
    { "Name": "PythonFoundationPackages", "Enabled": true },
    { "Name": "SequencerScripting", "Enabled": true },
    { "Name": "RemoteControl", "Enabled": true },
    { "Name": "ModelingToolsEditorMode", "Enabled": true }
  ]
}
```
Add an empty `Config/` folder — launch the editor once with the absolute path
(pattern in [[09 Install Unreal Engine (Linux)#Launch pattern that actually works (learned the hard way)]])
and UE generates the default ini set.

> [!tip] Plugin rationale (say these in class)
> **PCG** = Day-1 world building · **PythonScriptPlugin** = everything scripted ·
> **SequencerScripting** = camera/footage automation · **RemoteControl** = the
> port [[11 Unreal MCP Setup]] rides on · **ModelingTools** = in-editor cleanup of AI meshes.

## 2. Build the project + compile plugins
With C++ plugins in `Plugins/` (the MCP plugin, [[11 Unreal MCP Setup#2 Plugin into the project]]):
```bash
<ENGINE>/Engine/Build/BatchFiles/Linux/Build.sh UnrealEditor Linux Development \
    -Project="<ABS>/VWClassDemo/VWClassDemo.uproject" -TargetType=Editor
# ~35 s on the course laptop — this works with NO C++ game code of your own
```
Windows twin:
```powershell
& "<ENGINE>\Engine\Build\BatchFiles\Build.bat" UnrealEditor Win64 Development -Project="<ABS>\VWClassDemo\VWClassDemo.uproject" -TargetType=Editor
```

## 3. Create DemoWorld (scripted, not clicky)
1. Editor → **File → New Level → Empty Level**
2. **Output Log → python3** tab, run
   [[attachments/create_demo_level.py]] (`exec(open("<path>/create_demo_level.py").read())`)
3. It spawns: Sun (intensity 8), realtime SkyLight 2.5, height fog, a 2 km
   Ground plane, and `PropSlot_00…07` cubes in a circle with
   `BasicShapeMaterial` — then saves as `/Game/Maps/DemoWorld`.

Python-API gotchas we hit (5.7.4) are already handled in the script; the top
three: `EditorLevelLibrary.get_level_actors` **does not exist** (use
`EditorActorSubsystem.get_all_level_actors`), the class is `unreal.SkyLight`
(no `SkyLightActor`), and components come from `actor.get_component_by_class(...)`.
Full list: [[14 Troubleshooting Field Guide#5. Python-in-UE-5.7 API traps]].

## 4. Get an AI asset in (the Day-1 exercise, in miniature)
1. Generate a GLB first if you haven't: [[06 Your First 3D Model (GUI)]]
2. Editor → Content Browser → **Import to /Game…** → pick the GLB → keep defaults
3. Drag it into a `PropSlot` → delete that slot cube
4. Quick QC with ModelingTools if the mesh is heavy (AI GLBs are 10⁶+ tris at full res)

## 5. Verify
- Outliner shows `Sun, SkyLight, ExponentialHeightFog, Ground, PropSlot_00–07`
- Level saved (title bar has no `*`)
- Your GLB sits in a slot and renders with its baked textures

Next: [[11 Unreal MCP Setup]] → then [[13 Dataset Pipeline Tools]]
