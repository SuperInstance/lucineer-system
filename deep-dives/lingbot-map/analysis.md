# LingBot-Map: Architecture Analysis

> **Repository:** [SuperInstance/lingbot-map](https://github.com/SuperInstance/lingbot-map)
> **Paper:** [Geometric Context Transformer for Streaming 3D Reconstruction](https://arxiv.org/abs/2604.14141)
> **Authors:** Chen et al. (Robbyant Team)
> **License:** Apache 2.0
> **Analyzed:** 2026-08-02

---

## 1. Purpose & Scope

LingBot-Map is a **feed-forward 3D foundation model** for streaming 3D reconstruction from image sequences. It takes a stream of RGB images (video frames or photo collections) and produces, in real-time (~20 FPS at 518×378):

- **Camera poses** (extrinsics + intrinsics) per frame
- **Dense depth maps** with confidence scores
- **Dense 3D world points** (point cloud) with confidence scores
- **Camera trajectory** suitable for SLAM-like applications

The system is designed to handle sequences **exceeding 10,000 frames** without drift correction or bundle adjustment — a capability that distinguishes it from both prior streaming approaches (limited range) and optimization-based methods (too slow for real-time).

---

## 2. Architecture Overview

### 2.1 Top-Level Design

LingBot-Map follows a **Vision Transformer backbone + task-specific heads** architecture derived from VGGT (Visual Geometry Grounded Transformer) and DINOv2, with critical innovations for streaming:

```
Input Images → AggregatorStream (DINOv2 trunk + FlashInfer KV cache)
                    ↓
              Multi-scale features [4, 11, 17, 23]
                    ↓
         ┌──────────┼──────────┐
         ↓          ↓          ↓
   CameraHead   DPTHead    DPTHead
   (pose)       (depth)    (points)
```

### 2.2 Core Components

#### 2.2.1 AggregatorStream (`aggregator/stream.py`)

The heart of the system. It wraps a DINOv2 ViT-Large backbone with:

- **Patch Embedding:** DINOv2 `vitl14_reg` (ViT-L/14 with registers). Pretrained weights loaded from DINOv2 checkpoint; block weights initialized from the same checkpoint.

- **Special Tokens:** Per-frame tokens prepended to patch tokens:
  - 1 Camera token (used by CameraHead)
  - 4 Register tokens (from DINOv2-reg)
  - 1 Scale token (key innovation — see below)
  - Total: 6 special tokens + P patch tokens per frame

- **Alternating Attention:** `["frame", "global"]` block pattern:
  - **Frame blocks** (24 layers): Standard self-attention within each frame's tokens. Per-frame, no cross-frame communication. Uses 2D RoPE.
  - **Global blocks** (24 layers): Cross-frame attention via FlashInfer paged KV cache. Causal (frame *i* attends to frames 0..*i*). Uses 3D RoPE (video RoPE).

- **FlashInfer KV Cache** (`layers/flashinfer_cache.py`): A two-stream paged design:
  - **Patch stream** (recyclable): One page per frame, evicted via sliding window
  - **Special stream** (append-only): Special tokens from all frames packed densely
  - Scale frames never evicted; recent frames held in sliding window (default 64)
  - Enables O(window_size) memory instead of O(total_frames)

#### 2.2.2 Scale Token & Scale Frames

The first *N* frames (default 8) are **scale frames** processed together with bidirectional attention. They establish:

- Global scene scale (metric reconstruction)
- Coordinate frame origin
- Reference geometry for all subsequent frames

The scale token distinguishes scale frames from streaming frames: it takes value 1 for scale frames, 0 for streaming frames. This lets the model learn scale-conditioned representations.

#### 2.2.3 Prediction Heads

All heads operate on the concatenated output of frame + global attention intermediates (2 × embed_dim = 2048-dim input):

- **CameraCausalHead** (`heads/camera_head.py`): Iterative pose refinement using adaptive LayerNorm modulation (DiT-style). Predicts 9-dim pose encoding: [translation(3), quaternion(4), focal_length/FOV(2)]. Runs N iterations (default 4) of delta refinement. Has its own KV cache for cross-frame camera token attention.

- **DPTHead for Depth** (`heads/dpt_head.py`): Dense Prediction Transformer architecture. Multi-scale feature fusion from 4 intermediate layers. Output: depth map + confidence. Activation: `exp` for depth, `expp1` for confidence.

- **DPTHead for Points** (`heads/dpt_head.py`): Same DPT architecture, output_dim=4 (xyz + conf). Activation: `inv_log` for points (sign(y) × (exp(|y|) − 1)), `expp1` for confidence.

All heads run in **fp32** regardless of the inference dtype — the aggregator is cast to bf16/fp16, but `_predict_*` methods explicitly upcast inputs and run under `autocast(enabled=False)`.

#### 2.2.4 3D RoPE (Rotary Position Embedding)

- **Spatial:** 2D RoPE for within-frame patch positions (from DINOv2)
- **Temporal:** 3D video RoPE (`WanRotaryPosEmbed`) for cross-frame positions — extends spatial RoPE with a temporal dimension. Applied in global blocks and camera head.

The 3D RoPE encodes position as (frame_index, patch_y, patch_x), enabling the model to distinguish frames temporally even in a long KV cache.

---

## 3. Inference Modes

### 3.1 Streaming (`inference_streaming`)

Frame-by-frame processing with persistent KV cache:

1. **Phase 1:** Process `scale_frames` (default 8) together — bidirectional attention, establishes scene scale
2. **Phase 2:** Process remaining frames one-at-a-time — causal attention via KV cache

**Keyframe Interval** (`keyframe_interval > 1`): Skip caching non-keyframe frames. They still produce predictions but their KV isn't stored. Reduces memory from O(S) to O(S/kf_interval). Implemented via `_skip_append` flag on the KV cache.

### 3.2 Windowed (`inference_windowed`)

For sequences >3000 frames where streaming KV cache would exceed training range (320 views):

1. Split sequence into overlapping windows
2. Each window gets fresh KV cache + independent inference
3. Cross-window alignment via **similarity transform estimation**:
   - Pairwise alignment on overlapping keyframes
   - Scale from depth ratio (median of anchor_depth / target_depth)
   - Rotation from quaternion decomposition
   - Translation from center displacement
4. Stitch predictions with overlap de-duplication

The windowed mode also supports **flow-based keyframe selection** — dynamically choosing keyframes based on optical flow magnitude between current and last keyframe, rather than fixed intervals.

### 3.3 Compiled Streaming

`--compile` flag applies `torch.compile(mode="reduce-overhead")` to hot modules:
- Frame blocks (24)
- DINOv2 patch embed blocks
- Global block attention pre-norm, FFN residual, and projection

Requires CUDA graph warmup: 1 eager pass + 3 compiled passes (dress rehearsal) to capture and stabilize graph state.

---

## 4. Key Design Patterns

### 4.1 Template Method Pattern
`GCTBase` defines the skeleton (forward → aggregate → predict), subclasses implement `_build_aggregator()`, `_build_camera_head()`, `_aggregate_features()`.

### 4.2 Strategy Pattern
FlashInfer vs SDPA backends — swappable attention implementation selected at construction time via `use_sdpa` flag.

### 4.3 Paged Memory Management
The FlashInferKVCacheManager implements a sophisticated page-based memory scheme:
- Pages allocated from a pool
- Scale pages permanently resident
- Window pages evicted FIFO
- Special tokens packed across frames (6 tokens/frame → ~42 frames per special page)
- Rollback support for flow-based keyframe mode (defer eviction → rollback if frame not chosen as keyframe)

### 4.4 Mixed Precision Strategy
- Aggregator trunk: bf16/fp16 (cast at inference start)
- Prediction heads: fp32 (explicit upcast + autocast disabled)
- KV cache: configurable dtype

### 4.5 CPU Offloading
Per-frame predictions can be offloaded to CPU during inference (`output_device=cpu`), keeping GPU memory at O(1) frames for predictions.

---

## 5. File Structure & Responsibility Map

```
lingbot_map/
├── __init__.py                    # Package marker
├── models/
│   ├── gct_base.py                # ABC: forward(), _predict_*(), shared heads
│   ├── gct_stream.py              # Streaming inference (Phase 1 + Phase 2 loop)
│   ├── gct_stream_window.py       # Windowed inference + cross-window alignment
│   └── gct_stream_window_v2.py    # V2 with flow-based keyframe + debug KV stats
├── aggregator/
│   ├── base.py                    # ABC: patch embed, special tokens, block building, forward()
│   └── stream.py                  # Causal streaming: KV cache init, 3D RoPE, global attention
├── layers/
│   ├── attention.py               # Attention variants: FlashInfer, SDPA, Causal
│   ├── block.py                   # Transformer blocks: Block, FlashInferBlock, SDPABlock, CameraBlock
│   ├── flashinfer_cache.py        # Paged KV cache manager (two-stream design, 661 lines)
│   ├── rope.py                    # 2D RoPE + WanRotaryPosEmbed (3D video RoPE)
│   ├── vision_transformer.py      # DINOv2 ViT variants (small/base/large/giant2)
│   ├── patch_embed.py             # Conv patch embedding
│   ├── mlp.py                     # Standard MLP
│   ├── swiglu_ffn.py              # SwiGLU FFN (for DINOv2 giant)
│   ├── drop_path.py               # Stochastic depth
│   └── layer_scale.py             # Layer scale (learnable residual scaling)
├── heads/
│   ├── camera_head.py             # CameraHead + CameraCausalHead + CameraDecoder
│   ├── dpt_head.py                # DPT dense prediction head
│   ├── head_act.py                # Activation functions (inv_log, exp, expp1, etc.)
│   └── utils.py                   # UV grid + sinusoidal positional embeddings
├── utils/
│   ├── geometry.py                # SE3 inverses, depth unprojection, point map utils
│   ├── pose_enc.py                # Pose encoding ↔ extrinsics/intrinsics conversion
│   ├── rotation.py                # Quaternion ↔ rotation matrix conversions
│   └── load_fn.py                 # Image loading + preprocessing (crop, resize)
└── vis/
    ├── __init__.py                # Exports PointCloudViewer, viser_wrapper, predictions_to_glb
    ├── point_cloud_viewer.py      # Interactive Viser viewer with animated playback
    ├── viser_wrapper.py           # Quick visualization wrapper
    ├── glb_export.py              # Export to GLB 3D format (via trimesh)
    ├── sky_segmentation.py        # ONNX sky segmentation (auto-download from HuggingFace)
    └── utils.py                   # CameraState dataclass, color maps

demo.py                            # Main interactive demo (viser viewer)
gct_profile.py                     # FPS profiling tool
demo_render/                       # Offline rendering pipeline
├── batch_demo.py                  # Batch processing + video output
├── rgbd_render/                   # Full RGBD rendering system (voxel, octree, frustum cull)
├── render_cuda_ext/               # CUDA extensions (voxel morton, frustum cull)
├── interactive_viewer/            # Web-based NPZ → GLB viewer
└── config/                        # YAML presets (default, indoor, outdoor)
```

---

## 6. Dependencies

### Core
- **PyTorch 2.8.0** (CUDA 12.8) — model framework, `torch.compile`
- **torchvision** — image transforms
- **DINOv2** (ViT-L/14-reg) — pretrained backbone
- **VGGT** — architectural inspiration (pose encoding, camera head design)

### Performance
- **FlashInfer** — paged KV cache attention (optional but recommended; fallback to SDPA)
- **NVIDIA Kaolin** — GPU voxelization for rendering pipeline only

### Visualization
- **Viser** — interactive 3D web viewer (NeRF Studio project)
- **Trimesh** — GLB export
- **OpenCV** — image I/O, video processing
- **Matplotlib** — colormaps

### Utility
- **einops** — tensor reshaping
- **huggingface_hub** — model download, PyTorchModelHubMixin
- **safetensors** — checkpoint format
- **scipy** — rotation utilities
- **ONNX Runtime** — sky segmentation model inference

---

## 7. Performance Characteristics

| Metric | Value |
|--------|-------|
| Inference speed | ~20 FPS at 518×378 resolution |
| Training RoPE range | 320 views |
| Max tested sequence | ~25,000 frames (13 min indoor walkthrough) |
| GPU memory (streaming) | O(scale_frames + sliding_window) ≈ O(72 frames) |
| Model architecture | ViT-L/14-reg (1024-dim, 24+24 blocks, 16 heads) |
| Patch size | 14×14 pixels |
| Input resolution | 518×378 (canonical crop) |
| Pose encoding | 9-dim: T(3) + quat(4) + FOV(2) |
| Point cloud | Dense per-pixel (518×378 = ~196K points/frame) |
| Precision | bf16 aggregator, fp32 heads |

---

## 8. Novel Contributions

1. **Geometric Context Transformer (GCT):** Unifies coordinate grounding (scale token), dense geometric cues (DPT heads), and long-range drift correction (trajectory memory via KV cache + 3D RoPE) in a single streaming framework.

2. **Anchor Context (Scale Token):** The scale token mechanism allows the model to learn a scene-global scale reference without explicit metric supervision. Scale frames establish the coordinate frame; all subsequent frames are grounded to it.

3. **Pose-Reference Window:** The camera head's own KV cache maintains a history of camera token evolution, enabling iterative refinement that considers temporal context (not just the current frame's features).

4. **Trajectory Memory (3D RoPE + Paged KV Cache):** The combination of 3D video RoPE with FlashInfer's paged attention allows the model to maintain geometric consistency over thousands of frames without drift, bounded by the sliding window size rather than total sequence length.

5. **Keyframe-based KV Compression:** The `keyframe_interval` mechanism transparently reduces KV cache memory by 1/N× without dropping predictions — non-keyframes attend to cached KV but don't persist their own.

6. **Cross-Window Similarity Alignment:** The windowed inference mode performs pairwise scaled-SE3 alignment using depth ratios and quaternion decomposition on overlapping keyframes, enabling reconstruction of arbitrarily long sequences.

---

## 9. Relationship to Prior Work

| System | Relationship |
|--------|-------------|
| **VGGT** (Meta, 2025) | Direct ancestor. Camera head, pose encoding, DPT heads, and aggregator structure are extended from VGGT. LingBot-Map adds streaming inference, KV cache, scale token, and 3D RoPE. |
| **DINOv2** (Meta, 2023) | Backbone provider. The ViT-L/14-reg architecture and pretrained weights are used for patch embedding and block initialization. |
| **FlashInfer** | Infrastructure for paged KV cache. LingBot-Map's `FlashInferKVCacheManager` is a custom two-stream wrapper around FlashInfer's page-based attention API. |
| **DUSt3R / MASt3R** | Contemporary 3D foundation models. DUSt3R uses pairwise inference; LingBot-Map uses streaming causal inference for scalability. |
| **SLAM systems** (ORB-SLAM3, etc.) | Traditional SLAM uses sparse features + bundle adjustment. LingBot-Map replaces feature matching with learned attention and BA with feed-forward prediction. |

---

## 10. Limitations & Open Questions

- **No loop closure mechanism:** Beyond windowed mode, there's no explicit loop closure (detecting that the camera returned to a previously visited location and correcting accumulated drift). The 3D RoPE temporal encoding provides implicit positional awareness but not explicit re-localization.
- **Training range limit (320 views):** Performance degrades beyond 320 KV-cached views. The keyframe interval and windowed mode mitigate this but don't fundamentally solve it.
- **No evaluation benchmark released:** The TODO lists "Release evaluation benchmark" as pending.
- **Single-GPU only:** No multi-GPU inference support (context parallelism code exists but is disabled: `enable_ulysses_cp = False`).
- **Outdoor/aerial demos pending:** Only indoor walkthrough examples are released.
