---
tags: [replication, unreal, mcp]
---
# Unreal MCP Setup (UE 5.8 Native)

Let an AI coding agent drive the running editor — how `DemoWorld` was built and
the course's live finale. **UE 5.8 ships this in-engine**: the official
**ModelContextProtocol** plugin ("Unreal MCP") runs an MCP server *inside the
editor* (Streamable HTTP, JSON-RPC, default `http://127.0.0.1:8000/mcp`). No
external binary, no custom plugin, no compile step.

> [!note] Student-side twin
> The course vault carries the same recipe for students:
> *virtual worlds class* → `how to make this works/Unreal MCP Setup UE 5.8
> Native.md` (console commands, client dotfiles, curl recipes all documented
> in both).

> [!note] Verified 2026-10-04 on the course laptop (UE 5.8.3, Linux)
> Server autostarted from project config, protocol `2025-11-25` negotiated with
> OpenCode, **831 tools** across ~30 toolsets listed — incl. `PCGToolset` ×31,
> asset/actor/blueprint tools ×226, animation ×319, Niagara ×56.

**Legacy ≤ 5.7 only:** the old community bridge (`remiphilippe/mcp-unreal` Go
binary + custom plugin, ports 8090/30010) predates the native plugin and is no
longer followed here; Epic's own docs marked the plugin 5.8+. If you're pinned
to 5.7, that repo still works, but everything below assumes 5.8.

## 1. Enable the plugins (project)

In `<ABS>/VWClassDemo.uproject` under `"Plugins"` (or toggle in Edit → Plugins):
```json
{ "Name": "ModelContextProtocol", "Enabled": true },
{ "Name": "PCGToolset",           "Enabled": true },
{ "Name": "PCGBiomeCore",         "Enabled": true },
{ "Name": "PCGBiomeSample",       "Enabled": true },
{ "Name": "MCPClientToolset",     "Enabled": true }
```
Each enabled *Toolset* plugin contributes its tools to the server.

## 2. Autostart the server (project config)

`Config/DefaultEditorPerProjectUserSettings.ini`:
```ini
[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]
bAutoStartServer=True
ServerPortNumber=8000
ServerUrlPath=/mcp
bEnableToolSearch=False
```
`bEnableToolSearch`: `False` registers all 831 tools natively (demo-friendly,
context-heavy); `True` serves 3 discovery meta-tools + `call_tool` dispatch
(better for long agent sessions). Class of record:
`UModelContextProtocolSettings` (plugin source under
`Engine/Plugins/Experimental/ModelContextProtocol/`).

## 3. Launch the editor

```bash
DISPLAY=:0 setsid nohup <ENGINE>/Engine/Binaries/Linux/UnrealEditor \
    "<ABS>/VWClassDemo.uproject" -stdout >/tmp/ue-editor.log 2>&1 &
```
**Never add `-opengl4`** — measured: 2/2 launches with it died
	`VK_ERROR_DEVICE_LOST` ~25 s in ([[14 Troubleshooting Field Guide#10. UE editor dies of VK_ERROR_DEVICE_LOST ~25 s after launch]]).
The port opens once modules finish loading (cold first boot takes minutes).

## 4. Verify the server

```bash
SID=$(curl -s -D - -o /dev/null -X POST http://127.0.0.1:8000/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
  | grep -i mcp-session-id | tr -d '\r' | awk '{print $2}')
curl -s -X POST http://127.0.0.1:8000/mcp -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | grep -o '"name"' | wc -l
```
Expect **831** on the course plugin set. A spurious
`Call to unknown method "resources/templates/list"` error in the editor log is
a harmless client capability probe.

## 5. Register with your MCP client

**What must exist in the project directory?** Only steps 1–2 (plugin entries in
`.uproject` + the autostart ini). The server lives entirely in the editor.
Client registration then depends on which agent the student uses:

**OpenCode** (one command — it writes `mcp.servers` itself, nothing in the project):
```bash
opencode mcp add unreal58 --global --url http://127.0.0.1:8000/mcp
opencode mcp list        # → unreal58 connected
```

**Every other client — one editor console command** generates their config
files *into the project directory* automatically (verified from plugin source
`ModelContextProtocolClientConfig`):
```
ModelContextProtocol.GenerateClientConfig All      # or: ClaudeCode | Cursor | VSCode | Gemini | Codex
```
writes:

| File | Client |
|---|---|
| `.mcp.json` | Claude Code |
| `.cursor/mcp.json` | Cursor |
| `.vscode/mcp.json` | VS Code / Copilot |
| `.gemini/settings.json` | Gemini CLI |
| `.codex/config.toml` | Codex CLI (TOML, **write-once** — errors if file exists) |

JSON files merge (existing entries preserved); all point at the same
`http://localhost:<port>/mcp`. For course repos: commit these dotfiles next to
the `.uproject` so students get working agent configs on clone. Other
self-hosted clients: same URL, Streamable HTTP transport.

## 6. Smoke test through the agent
Ask it: *"create a cube named MCP_Probe in the current level"* → it discovers
the editor/actor toolset tools and the cube appears in the Outliner. First
request logs Epic's experimental AI-license banner — worth a course slide.

## 7. Day-to-day ops

**In the editor console** (`` ` `` key — command names from the plugin source):

| Console command | What it does |
|---|---|
| `ModelContextProtocol.StartServer` | start server (optional arg: port, e.g. `StartServer 8000`) |
| `ModelContextProtocol.StopServer` | stop it (editor keeps running) |
| `ModelContextProtocol.RefreshTools` | rebuild tool list — run after enabling/disabling toolset plugins |
| `ModelContextProtocol.GenerateClientConfig All` | write ready-made client configs (`.cursor/mcp.json`, `.vscode/mcp.json`, …) into the project — covers Cursor/VSCode/Claude Code/Gemini/Codex |

**From any shell** (curl, Streamable HTTP — replace `<tool>` + `<json-args>`):
```bash
# 1) open a session, 2) call any tool, read the result
SID=$(curl -s -D - -o /dev/null -X POST http://127.0.0.1:8000/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
  | grep -i mcp-session-id | tr -d '\r' | awk '{print $2}')
curl -s -X POST http://127.0.0.1:8000/mcp -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' -o /dev/null
curl -s -X POST http://127.0.0.1:8000/mcp -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"<tool>","arguments":{<json-args>}}}'
```

Browsing the 831 tools: filter the §4 `tools/list` response —
```bash
... tools/list request ... | jq -r '.result.tools[].name' | grep -i pcg
```

> [!tip] Hidden gold for the course: AgentSkills
> `tools/call` with `ToolsetRegistry.AgentSkillToolset.ListSkills` (no args —
> verified) returns Epic's **bundled skill docs**, e.g.
> `/PCGToolset/Skills/Skill_PCGGraphGeneration` — a written playbook telling
> agents how to do PCG graph work. Read-able teaching material for M5: it is
> literally the "how to build a PCG world" prompt, shipped by Epic.

**From the agent itself**: skip curl entirely — with `unreal58` connected, ask
things like *"spawn a cube named MCP_Probe"* or *"list PCG tools"* and the
right toolset tool fires.

> [!warning] Don't forget the VRAM contract
> Editor open = ~1.7 GB VRAM parked. Close it before ComfyUI runs, open it for
> Unreal/MCP work. [[08 VRAM Playbook (12 GB and under)]]

Next: [[13 Dataset Pipeline Tools]]
