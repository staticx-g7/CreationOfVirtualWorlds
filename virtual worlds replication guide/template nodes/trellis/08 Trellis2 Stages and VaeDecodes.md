---
tags: [node, template, decode]
---
# Trellis2 Stages + VaeDecodes — where resolution (and OOM) lives

**What they are:** six nodes that move data between *latent space* (what the
samplers work in) and *geometry/texture space* (what a mesh is). Two “stage”
nodes feed the samplers, one sets resolution, three VAE decodes materialize the
result. **All the cubic-VRAM physics of this template is in this file.**

| Node · Widget | Default | What it does / what turning it does |
|---|---|---|
| `VaeDecodeStructureTrellis2 · resolution` | `32` | materializes the coarse structure grid. 32 is the protocol — not a quality dial, leave it |
| `Trellis2ShapeStage` | *no widgets* | structure → shape-latent for sampler ② |
| `Trellis2UpsampleStage · target_resolution` | `1024` | **THE dial.** Final voxel-grid resolution of the shape. **Hard floor 1024** (setting less is refused — this bit us). Cost is **cubic**: 1024 ≈ +2.5 GiB decode (our measured survivor), 1536 ≈ ~8.5 GiB, 2048 ≈ ~20 GiB (estimates — template default is 1536, *that's* why stock template dies on 12 GB) |
| `Trellis2TextureStage` + `VaeDecodeTextureTrellis` + texture `VAELoader` | texture VAE bf16 | produce the voxel-textured appearance for baking. No widgets worth turning |
| `VaeDecodeShapeTrellis` | *no widgets* | latent → actual vertices/faces. Runs *after* the upsample pass; its memory ∝ `target_resolution³` |

> [!warning] The 12 GB cliff is exactly here
> 1024: geometry completes ✅ (verified, our 164 MB GLB). 1536/2048 or the stock
> template default: OOM in the decode/upsample region ❌. Nothing about flags
> moves this wall — `--novram` just relocates the failure. Decision tree:
> [[08 VRAM Playbook (12 GB and under)]].

**Quality note:** resolution controls geometric *finesse* (thin legs, bevels,
text read-ability), not texture sharpness — that's [[09 BakeTextureFromVoxel]].

Prev: [[07 KSampler x4]] · Next: [[09 BakeTextureFromVoxel]]
