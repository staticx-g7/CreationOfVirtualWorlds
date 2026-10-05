---
tags: [replication, data, tools]
---
# Dataset Pipeline Tools

The Day-2 payoff: footage + scene metadata → a validated training dataset.
The tools live in the course vault under `Data Pipeline Tools/` and are
**stdlib-only Python 3.10+ / bash + ffmpeg** — no pip installs, runs anywhere.
Grab that folder as-is; this note is the how-to-run-it.

## Dependency
```bash
ffmpeg -version | head -1     # installed in [[02 Linux System Setup]]
```

## The pipeline, in course order
```bash
cd "<the Data Pipeline Tools folder>"

# 1. clip → numbered frame stack (+ probe metadata sidecar)
./extract_frames.sh recordings/clip001.mp4 frames/clip001

# 2. frames + UE scene manifest → dataset with train/val/test + metadata.jsonl
#    (manifest comes from the UE side: Content/Python/generate_scene_metadata.py)
python3 build_dataset.py --frames frames --manifest manifest.json \
       --out dataset --val-split 0.15

# 3. rule-based captions → text→video training pairs
python3 caption_clips.py --dataset dataset

# 4. validate BEFORE burning GPU hours
python3 validate_dataset.py --dataset dataset
```

## Where the pieces came from in this build
| Piece | Built in |
|---|---|
| `clip001.mp4` (footage) | [[10 Create the Demo Project]] — sequencer camera + Movie Render Queue (or an NDI recording on Windows: [[12 City Sample on Linux — Reality Check#NDI status (the M6 streaming module)]]) |
| `manifest.json` | `generate_scene_metadata.py` (project's `Content/Python/`) — actor names/positions/materials per frame range |
| AI props inside the clip | [[06 Your First 3D Model (GUI)]] |

## Check your output looks right
```bash
head -2 dataset/metadata.jsonl | python3 -m json.tool   # one JSON per clip
find dataset -name "*.png" | wc -l                      # frames present
python3 validate_dataset.py --dataset dataset           # expect: 0 errors
```
Common validation catches: split leakage (same clip in train+val — fix by
renaming clip dirs), missing frame sequences from interrupted renders.

## Training handoff (course M9)
`dataset/` uploads straight into the video-gen fine-tune loop (the course's
JUPITER 4×GH200 demo) — `metadata.jsonl` + caption pairs are the contract.

Last mile: [[15 Verification Checklist]]
