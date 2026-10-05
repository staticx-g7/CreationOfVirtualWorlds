---
tags: [node, template, input]
---
# LoadImage

**What it is:** the one input that decides everything downstream — a photo (or
render) of ONE object on a plain-ish background. TRELLIS.2 is image-to-3D: it
reconstructs what it sees and *invents* what it can't (back side, hidden parts).

**Widgets**

| Widget | Template default | Turning it does |
|---|---|---|
| `image` | *(your upload)* | the single biggest quality lever in the whole graph |

**What a good input looks like** (learned the hard way, all of these help):
- object fills ~70 % of frame, dead-centered, whole object visible
- plain background, even lighting, no strong shadows on the ground
- 3/4 or straight-on view; slight perspective is fine
- **anything occluded gets hallucinated** — a chair with a jacket on the seat
  becomes a chair with a lump welded into it

> [!tip] Renders count as photos
> Dropping a UE viewport screenshot of your own mesh is a legitimate pipeline
> (render → refine → reimport). That's a whole Day-2 idea, not a hack.

**VRAM/time:** none here — but a cluttered photo forces more steps downstream
to compensate. It can't.

Prev: [[00 Node Map]] · Next: [[02 RemoveBackground]]
