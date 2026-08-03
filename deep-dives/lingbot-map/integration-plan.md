# LingBot-Map × Slackwater/Lucineer Integration Plan

> **Date:** 2026-08-02
> **Status:** Strategic Analysis — Not Yet Implemented
> **Audience:** Lucineer system architect (Casey)

---

## 1. Executive Summary

LingBot-Map is a **feed-forward 3D foundation model** that reconstructs scenes from image streams in real-time (~20 FPS). For the Slackwater/Lucineer ecosystem, it represents a potential **perception backbone** — a way for in-game agents and the build system to "see" real-world spaces and translate them into game-ready 3D geometry.

This document maps the integration surface between LingBot-Map's capabilities and Slackwater's architecture (agent discovery, puffin calls, swarm intelligence, build pipeline, and the Roblox bridge).

---

## 2. Where LingBot-Map Fits in the Stack

### Current Slackwater Architecture Layers

```
┌─────────────────────────────────────────────────┐
│  Player Experience (game, UI, tutorials)         │
├─────────────────────────────────────────────────┤
│  Agent Layer (NPCs, builders, researchers)       │
│  ↕ Puffin Call Protocol                          │
├─────────────────────────────────────────────────┤
│  Build Pipeline (Scrapcraft → Lua → Roblox)      │
├─────────────────────────────────────────────────┤
│  ← LingBot-Map lives HERE                        │
│  Perception / World Ingestion Layer              │
│  (3D scan → point cloud → mesh → placement)     │
├─────────────────────────────────────────────────┤
│  Infrastructure (Roblox relay, Cloudflare, GPU)  │
└─────────────────────────────────────────────────┘
```

LingBot-Map is a **world ingestion primitive**: it converts real-world visual data into structured 3D geometry. This is directly relevant to several Slackwater capabilities:

1. **World building from reference:** Players or agents photograph a real place; LingBot-Map reconstructs it as a 3D point cloud; the build pipeline converts it into Roblox parts.
2. **Agent perception:** Agents that can "see" a player's environment can provide contextual building assistance.
3. **Spatial understanding:** Scene geometry enables agents to reason about space, scale, and layout — critical for the spatial grammar system.

---

## 3. Integration Points

### 3.1 → Agent Discovery (Puffin Calls)

**Connection:** Agents with 3D perception capabilities broadcast this via their puffin call.

```typescript
interface PuffinCall {
  capabilities: CapabilityBadge[];
  // NEW: perception badges
  // "spatial-perception": can process 3D scans
  // "scene-reconstruction": can convert images to point clouds
  // "depth-estimation": can estimate depth from images
}
```

An agent running LingBot-Map (or with API access to a LingBot-Map service) would advertise `spatial-perception` in its capabilities. Other agents seeking world geometry data would be attracted to this agent's puffin call.

**Implementation:** Add perception capability badges to the PuffinCall schema. No changes to LingBot-Map itself — it's an external capability.

### 3.2 → Swarm Intelligence

**Connection:** Multiple agents can contribute partial reconstructions that get merged.

LingBot-Map's windowed inference mode performs cross-window similarity alignment — this is conceptually identical to multiple agents each reconstructing a portion of a scene and then aligning their results. The `_pairwise_alignment()` method (scale, rotation, translation estimation from depth ratios and quaternions) is a direct analog of swarm-based map merging.

**Integration pattern:**
- Agent A scans the north half of a building → partial point cloud + poses
- Agent B scans the south half → partial point cloud + poses
- The alignment math from `gct_stream_window.py` merges them

**Implementation:** Expose the `_pairwise_alignment` and `_warp_predictions` methods as a standalone service that agents can call with their respective predictions.

### 3.3 → Build Pipeline (Scrapcraft → Lua → Roblox)

**Connection:** Point clouds from LingBot-Map become input geometry for the build system.

The current build pipeline goes: concept art → spatial decomposition → Lua parts → Roblox relay. LingBot-Map adds a new input modality:

```
Real-world photos → LingBot-Map → point cloud + depth maps
                                      ↓
                              Mesh reconstruction
                                      ↓
                          Spatial grammar analysis
                                      ↓
                        Lua part generation (Lucineer)
                                      ↓
                            Roblox relay
```

The challenge is **point cloud → mesh → Roblox parts**. LingBot-Map outputs dense per-pixel point clouds (~196K points/frame). This needs to be:
1. Downsampled and cleaned (the `--downsample_factor` flag handles this)
2. Converted to mesh (Poisson reconstruction or similar)
3. Decomposed into primitive shapes (boxes, cylinders) suitable for Roblox parts
4. Converted to Lua placement commands

**Implementation:** A new conversion service that ingests LingBot-Map NPZ output files and emits Lua part specifications. The existing `vis/glb_export.py` provides a starting point for mesh export.

### 3.4 → Spatial Grammar System

**Connection:** LingBot-Map's depth maps inform spatial grammar rules.

The Slackwater spatial grammar (`SPATIAL_GRAMMAR_v2.md`, `SEVEN_COURTS_SPATIAL_DESIGN.md`) defines how spaces are structured. LingBot-Map's reconstruction provides **ground truth spatial data** that can:

- Validate spatial grammar rules against real spaces
- Generate training data for spatial reasoning agents
- Provide scale and proportion reference for the "spatial decomposition" step

**Implementation:** Feed LingBot-Map reconstructions into the spatial grammar analyzer as reference data. No real-time integration needed — this is an offline analysis pipeline.

### 3.5 → Lucineer Agent (Master Builder)

**Connection:** Lucineer can use LingBot-Map as a "vision" tool.

Lucineer is the master builder agent. Giving it the ability to ingest real-world reference spaces enhances its capability:

- Player: "Build me a room like my kitchen"
- Player uploads kitchen photos
- Lucineer invokes LingBot-Map → gets 3D reconstruction
- Lucineer analyzes geometry → identifies spatial patterns
- Lucineer generates build plan adapted to Roblox constraints

**Implementation:** Wrap LingBot-Map's `inference_streaming()` as a tool callable by Lucineer via the tool system. The agent passes image paths; the tool returns point cloud + poses.

### 3.6 → MIDI Perception / Vision

**Connection:** The `MIDI_PERCEPTION_VISION.md` document envisions a perception system for agents.

LingBot-Map could serve as the **spatial perception layer** — answering questions like "how far away is that wall?", "what's the room layout?", "how high is the ceiling?". The depth maps and point clouds provide geometric grounding for perception queries.

---

## 4. Technical Integration Requirements

### 4.1 Hardware

| Requirement | Specification |
|-------------|--------------|
| GPU | NVIDIA GPU with ≥8GB VRAM (recommend ≥16GB for long sequences) |
| CUDA | 12.8+ |
| Compute capability | ≥ 8.0 (Ampere+) for bf16 |
| RAM | ≥16GB system RAM for CPU offloading |

### 4.2 Model Storage

- Checkpoint: ~1.5 GB (ViT-L/14-reg + heads)
- Sky segmentation model: ~20 MB (ONNX)
- Total: ~1.5 GB on disk

### 4.3 Service Architecture

Two deployment options:

**Option A: Embedded (in-process)**
- Load LingBot-Map directly into the agent runtime
- Pros: no network latency, direct tensor access
- Cons: GPU memory contention, Python dependency management

**Option B: Microservice**
- Run LingBot-Map as a separate HTTP service (FastAPI wrapper)
- Agents call REST API: `POST /reconstruct` with images → get NPZ/PLY
- Pros: isolation, language-agnostic, scalable
- Cons: network latency, serialization overhead

**Recommendation:** Option B for the Roblox bridge pipeline (where the build agent is already remote); Option A for direct agent integration (where Lucineer runs in the same Python process).

### 4.4 Data Pipeline

```
Player Device          Gateway              GPU Server
     │                    │                      │
     │── photos ─────────▶│                      │
     │                    │── images batch ─────▶│
     │                    │                      │── LingBot-Map inference
     │                    │◀── NPZ + PLY ───────│
     │                    │                      │
     │                    │── mesh + Lua ──▶ Roblox Relay
     │◀── build result ───│                      │
```

### 4.5 Dependencies to Add

```
# pyproject.toml additions for Slackwater
lingbot-map = {extras = ["vis"], version = "*"}
# OR, if running headless:
lingbot-map = "*"
flashinfer-python = "*"   # optional but strongly recommended
```

---

## 5. Integration Phases

### Phase 1: Reference Pipeline (Offline)
**Goal:** Prove the photo → Roblox parts pipeline end-to-end.

1. Install LingBot-Map on the GPU server
2. Take photos of a simple room (4 walls, door, window)
3. Run `demo.py --image_folder room_photos --mask_sky`
4. Export point cloud → PLY
5. Convert PLY → mesh (Open3D Poisson reconstruction)
6. Decompose mesh → primitive shapes (RANSAC fitting)
7. Generate Lua placement commands
8. Push to Roblox relay

**Deliverable:** A proof-of-concept where photographing a real room creates a Roblox replica.

### Phase 2: Agent Tool Integration
**Goal:** Lucineer can invoke reconstruction as a tool.

1. Wrap `inference_streaming()` in a tool interface
2. Add tool to Lucineer's chisel inventory
3. Lucineer can call: `reconstruct_from_images(image_paths) → point_cloud`
4. Lucineer analyzes point cloud dimensions, suggests build approach

**Deliverable:** Lucineer agent that can "see" reference spaces.

### Phase 3: Multi-Agent Swarm Mapping
**Goal:** Multiple agents contribute to a shared world map.

1. Expose alignment API (`_pairwise_alignment`, `_warp_predictions`)
2. Agents perform partial scans, submit to alignment service
3. Shared map accumulates merged reconstructions
4. Agents query shared map for spatial reasoning

**Deliverable:** A collaborative world-building experience where multiple agents each scan parts of a real space and collectively reconstruct it.

### Phase 4: Real-Time Perception
**Goal:** Live depth estimation for agent perception.

1. Run LingBot-Map in streaming mode on a live camera feed
2. Feed depth maps to perception system
3. Agents reason about distances, obstacles, spatial layout in real-time

**Deliverable:** Agents that perceive and respond to the player's real-world environment.

---

## 6. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| GPU resource contention with other services | Medium | Run on dedicated GPU; schedule inference windows |
| Model checkpoint size (1.5 GB) | Low | Use Git LFS or HuggingFace Hub for distribution |
| Roblox part limit (~1M parts per place) | High | Aggressive downsampling; mesh-based import instead of part-based |
| Pose accuracy in featureless environments | Medium | Combine with traditional SLAM for verification |
| FlashInfer CUDA compatibility | Low | SDPA fallback available (slower but functional) |
| Player privacy (camera access) | High | Explicit opt-in; on-device processing where possible |

---

## 7. Alternative / Complementary Tools

| Tool | Role | Complementary? |
|------|------|----------------|
| **DUSt3R / MASt3R** | Pairwise 3D reconstruction | Alternative for 2-image scenarios where streaming isn't needed |
| **Open3D** | Mesh reconstruction, ICP alignment | Yes — converts LingBot-Map point clouds to meshes |
| **InstantNGP / Gaussian Splatting** | Novel view synthesis | Complementary — uses LingBot-Map poses for camera initialization |
| **MiDaS / Depth Anything** | Monocular depth estimation | Simpler fallback when multi-view isn't available |
| **COLMAP** | Traditional SfM + MVS | Baseline comparison; slower but more accurate for static scenes |

---

## 8. Recommendation

**Prioritize Phase 1 (Reference Pipeline)** as a standalone spike. It demonstrates the full chain without requiring changes to the agent system. If the photo → Roblox pipeline proves viable, Phase 2 (agent tool integration) becomes a natural extension that adds the most value to the player experience.

The most exciting integration point is **Lucineer using reconstruction as a vision tool** — it transforms the master builder from a pure generator into a perception-driven designer that can reference real-world spaces.
