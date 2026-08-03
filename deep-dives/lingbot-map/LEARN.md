# LEARN: LingBot-Map Deep Dive

> **Goal:** Understand *why* LingBot-Map works, not just *how* to use it.
>
> For builders, researchers, and tinkerers who want to develop intuition for streaming 3D reconstruction.

---

## Core Concepts

### 1. The 3D Reconstruction Problem

**The setup:** You have a camera moving through a scene. At each moment, the camera captures a 2D image — a projection of the 3D world. Can you recover the 3D world from a sequence of 2D images?

**What you need to recover:**
1. **Where was the camera?** (pose: position + orientation = 6 DoF)
2. **How far away is each pixel?** (depth: 1 value per pixel)
3. **Where is each pixel in 3D?** (3D point: recoverable from depth + pose + intrinsics)

**Why it's hard:**
- A single 2D image loses depth information (the projection is many-to-one)
- Small pose errors accumulate over time (drift)
- Different frames see different parts of the scene (occlusion)
- Lighting changes, motion blur, textureless surfaces...

### 2. Traditional Approaches (and Their Problems)

#### Structure from Motion (COLMAP, Visual SfM)

```
Photos → Feature matching (SIFT/SURF) → Sparse point cloud
      → Bundle adjustment (iterative optimization) → Dense reconstruction (MVS)
```

**Problem:** Slow (hours), needs distinct features, fails on textureless surfaces, requires careful parameter tuning.

#### SLAM Systems (ORB-SLAM3, DSO)

```
Video → Feature tracking → Pose graph optimization → Local bundle adjustment
     → Dense depth (semi-dense or stereo)
```

**Problem:** Sparse features limit geometric understanding, optimization adds latency, loop closure is complex.

#### Neural Radiance Fields (NeRF, Gaussian Splatting)

```
Multi-view images → Camera poses (known) → Volume rendering optimization
                 → Neural scene representation → Novel view synthesis
```

**Problem:** Needs known poses, requires per-scene optimization (minutes to hours), not metric-scale by default.

### 3. The Feed-Forward Revolution: VGGT and DUSt3R

The key insight: **stop optimizing at test time.** Instead, train a neural network on millions of scenes so it learns to predict geometry directly.

```
Images → Neural Network (trained on millions of scenes) → Poses + Depth + Points
```

- **VGGT (2025):** Processes all images together via a Vision Transformer. Great quality, but memory scales as O(N²) with frame count.
- **DUSt3R (2024):** Processes image pairs. Simple but limited to 2-image scenarios.
- **LingBot-Map (2026):** Processes images **one at a time** with a KV cache. O(1) memory per frame. Best of both worlds: streaming speed + global consistency.

---

## Understanding the Architecture

### 4. Why Two Types of Attention?

LingBot-Map alternates between **frame attention** and **global attention**:

```
[Frame Attn] → [Global Attn] → [Frame Attn] → [Global Attn] → ...
   (24 layers each, alternating)
```

**Frame attention** processes each image independently:
- Each frame's patches attend to each other (within-frame self-attention)
- No cross-frame information leakage
- Like running DINOv2 on each frame separately
- Cheap: O(P²) where P = patches per frame

**Global attention** lets frames communicate:
- Each frame's tokens attend to all past frames' tokens (causal)
- This is where camera tracking and geometric consistency happen
- Expensive in theory: O(S × P × S × P) for S frames
- But KV cache makes it O(S × P × P) per new frame

**Why alternate?** Pure global attention is too expensive. Pure frame attention can't track cameras or maintain geometric consistency. Alternating gives per-frame feature extraction + cross-frame geometric reasoning.

#### Exercise: Think About Attention Patterns

Consider a sequence of 100 frames at 518×378 resolution (37×27 = 999 patches per frame):

- **Without KV cache:** Global attention processes 100 × 1005 = 100,500 tokens at once. Attention matrix: 100,500² ≈ 10 billion entries. **Infeasible.**
- **With KV cache (streaming):** Each new frame adds 1005 tokens. It attends to the cached ~64 × 1005 ≈ 64,000 tokens. Attention: 1005 × 64,000 ≈ 64 million entries per frame. **Feasible at 20 FPS.**

### 5. The Scale Token: Grounding in Reality

**Problem:** A feed-forward model predicts geometry up to scale. Without external reference, it can't tell if a scene is 1 meter or 1 kilometer across.

**LingBot-Map's solution:** The first N frames (default 8) are **scale frames**. They get a special token (the scale token, value=1) that tells the model: "these frames establish the reference scale." All subsequent frames get scale token value=0, meaning "use the established scale."

This is learned during training: the model is trained on scenes with known metric scale, and the scale token provides the supervisory signal for metric grounding.

**Analogy:** Imagine being blindfolded and led into a room. The first few steps (where you can feel walls, furniture) establish your sense of the room's size. After that, you navigate by dead reckoning, periodically correcting with new touches. The scale frames are those first few grounding steps.

### 6. 3D RoPE: Temporal Position Encoding

**Problem:** In a long KV cache, how does the model know whether a cached token came from frame 5 or frame 5000?

**Standard RoPE** (2D): Encodes (x, y) position within an image. No temporal information.

**3D Video RoPE** (WanRotaryPosEmbed): Encodes (frame, y, x) position. Each dimension gets a different frequency band:

```python
# Head dimension split into 3 parts: temporal, height, width
# Default for ViT-L (head_dim=64): t_dim=24, h_dim=20, w_dim=20
# (exact split determined by fhw_dim parameter)
```

The temporal frequency is designed so that positions up to `max_frame_num` (default 1024) are distinguishable. Beyond that, positions "wrap around" and become ambiguous — this is why performance degrades beyond the training range.

#### Exercise: Visualize RoPE Frequencies

1. Generate 3D RoPE positions for frames 0, 1, 100, 500, 1000
2. Compute the pairwise dot products of the temporal embeddings
3. Plot how dot product decays with frame distance — it should be high for nearby frames and low for distant ones
4. What happens at frame 1024 vs 1025? (Hint: aliasing)

### 7. The KV Cache: Memory Management for Long Sequences

**The challenge:** At 518×378 resolution, each frame produces ~1005 tokens. With 24 transformer blocks, 16 heads, and 64-dim head, each frame's KV cache is:

```
Per frame: 2 (K+V) × 1005 tokens × 1024 dim × 24 blocks × 2 bytes (bf16)
         ≈ 94 MB
```

For 10,000 frames without eviction: **940 GB.** Obviously infeasible.

**The solution — Paged Sliding Window:**

```
KV Cache Layout:
┌──────────────────────────────────────────────┐
│ Scale Pages (8 frames × 1005 tokens)         │ ← Never evicted
├──────────────────────────────────────────────┤
│ Window Pages (64 frames × 1005 tokens)       │ ← FIFO eviction
├──────────────────────────────────────────────┤
│ Special Pages (append-only, packed densely)  │ ← Never evicted
└──────────────────────────────────────────────┘

Total: (8 + 64) × 94 MB ≈ 6.8 GB  ← Feasible!
```

**Key innovation:** Special tokens (camera, register, scale) are stored separately in append-only pages, packed densely across frames. This preserves cross-frame context even when patch tokens from old frames are evicted.

### 8. Keyframe Interval: Smart Compression

**Idea:** Not every frame needs to live in the KV cache. If frame 42 is very similar to frame 41, caching frame 41 is enough.

**Implementation:**
- Keyframes: KV stored in cache (normal behavior)
- Non-keyframes: `skip_append=True` → model attends to cached KV + current KV, but doesn't persist current KV

```
Frame 0-7:   Scale frames (always cached)
Frame 8:     Keyframe (cached)
Frame 9:     Non-keyframe (attends, doesn't cache) ← still produces predictions!
Frame 10:    Keyframe (cached)
Frame 11:    Non-keyframe
...
```

With `keyframe_interval=4`, only 25% of frames are cached → 4× memory reduction with minimal quality loss.

#### Exercise: Measure the Tradeoff

1. Run LingBot-Map on the courthouse example with `--keyframe_interval 1, 2, 4, 8`
2. Compare reconstruction quality (visual point cloud)
3. Plot GPU peak memory vs keyframe_interval
4. At what interval does quality visibly degrade?

### 9. Cross-Window Alignment: Stitching Independent Reconstructions

**Problem:** Windowed inference processes each window independently. Each window has its own coordinate frame. How do you merge them?

**The alignment pipeline:**

```
Window 1: [f0 ... f247] → predictions in Frame 1's coords
Window 2: [f216 ... f463] → predictions in Frame 2's coords  (overlap: f216-f247)
                                         ↓
                    Find similarity transform (s, R, t) that maps W2 → W1
                                         ↓
                    Apply transform to all of W2's predictions
                                         ↓
                    Stitch: concatenate with overlap de-duplication
```

**How (s, R, t) is estimated:**

1. Find paired keyframes in the overlap region (keyframes present in both windows)
2. From camera centers (pose_enc[0:3]) of paired keyframes:
   - **Rotation (R):** R_ab = R_a × R_b^T (relative rotation from quaternion decomposition)
   - **Translation (t):** t_ab = c_a - s × R_ab × c_b
   - **Scale (s):** Median of (depth_a / depth_b) across all paired keyframes' pixels

This is a **scaled SE(3) alignment** — the same transformation used in robotics for map merging.

### 10. The Camera Head: Iterative Refinement

The camera head doesn't predict poses in one shot. It iterates:

```
Iteration 1: Start with learnable "empty pose" → predict delta → apply activation
Iteration 2: Embed current pose prediction → modulate camera token → predict delta → add
Iteration 3: Same refinement...
Iteration 4: Final pose
```

This is inspired by Diffusion Transformers (DiTs): instead of denoising, it's **refining a pose estimate.** The adaptive LayerNorm (modulate features based on current estimate) lets the model "know what it already guessed" and correct accordingly.

Each iteration also attends to the camera KV cache — so it can see how the current frame's camera token relates to all previous frames' camera tokens.

**Speed vs accuracy:** `--camera_num_iterations 1` skips 3 refinement passes. About 30% faster, small accuracy hit. The KV cache for the camera head also shrinks 4×.

---

## Design Philosophy

### Why Feed-Forward, Not Optimization?

Traditional 3D reconstruction uses **optimization**: define a loss (reprojection error), initialize poses/depth, and gradient-descend until convergence. This works but is slow and can get stuck in local minima.

Feed-forward models **learn the optimization** during training. The network's weights encode the "optimization strategy" — given features, predict the answer directly. No iterative refinement at test time (except the camera head's 4 iterations, which are cheap).

**Tradeoff:** Feed-forward is fast but less accurate than heavy optimization. LingBot-Map compensates with:
- Large training dataset (millions of scenes)
- Strong backbone (DINOv2 ViT-Large)
- Temporal consistency mechanisms (3D RoPE, KV cache)
- Optional post-processing (windowed alignment)

### Why Causal, Not Bidirectional?

**Bidirectional** (all frames see each other): Better quality (more information per frame), but requires all frames in memory. VGGT's approach.

**Causal** (frame *i* only sees frames 0...*i*): Slightly worse quality (can't use future information), but enables true streaming — process each frame as it arrives.

LingBot-Map chooses causal for **practical deployment:** real-time AR/VR, robotics, and any application where you can't wait for all frames.

**Training trick:** Stage 1 trains bidirectionally (learning rich geometric features). Stage 2 fine-tunes causally (adapting to the streaming constraint). This gets the best of both worlds.

---

## Exercises

### Beginner

1. **Run the demo.** Follow the Quick Start guide. Explore the 3D viewer. What happens when you change the confidence threshold?

2. **Photograph a small object.** Take 30-50 photos circling an object on a table. Run LingBot-Map. How does the reconstruction look? What's missing?

3. **Compare indoor vs outdoor.** Run on `example/courthouse` (outdoor) and an indoor scene. Which works better? Why? (Hint: sky, scale, texture.)

4. **FPS experiment.** Run with `--camera_num_iterations 1` vs `4`. Time both. Is the speed difference worth the quality difference for your use case?

### Intermediate

5. **Keyframe interval sweep.** Run a 500-frame sequence with `keyframe_interval` = 1, 2, 4, 8, 16. At what interval does the pose trajectory start drifting? At what interval does the point cloud develop visible artifacts?

6. **SDPA vs FlashInfer.** Run the same sequence with `--use_sdpa` and without. Compare FPS and peak GPU memory. Is FlashInfer worth the installation overhead?

7. **Export to Blender.** Use the GLB export utility to create a `.glb` file. Import into Blender. Inspect the mesh topology. How dense is it? Can you identify failure modes (holes, floaters)?

8. **Depth vs points.** The model predicts both depth maps and 3D points. These should be consistent (unprojecting depth should give the points). Write a script to verify this. Is there a discrepancy?

### Advanced

9. **Windowed alignment validation.** Run a 2000-frame sequence in windowed mode. Extract the `chunk_scales` and `chunk_transforms` from predictions. Are the scale factors close to 1.0? What causes scale drift?

10. **Custom camera path.** Create a YAML preset that orbits the scene at three different heights. Render with `batch_demo.py`. How does the birdeye mode handle tall scenes differently from flat ones?

11. **Flow-based keyframe selection.** Read the `_compute_flow_magnitude` function in `gct_stream_window_v2.py`. What flow threshold would you choose for a slow indoor walkthrough vs a fast outdoor drone flight? Test your intuition.

12. **Embedding space analysis.** Extract the camera token embeddings (before the camera head) for each frame. Compute pairwise cosine similarity. Does the similarity structure correspond to camera proximity? Could this be used for loop closure detection?

---

## Further Reading

### Papers
- [VGGT: Visual Geometry Grounded Transformer](https://arxiv.org/abs/2503.11651) — LingBot-Map's direct predecessor
- [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) — Backbone
- [FlashInfer: Efficient and Customizable Attention Engine](https://arxiv.org/abs/2310.00127) — KV cache infrastructure
- [DUSt3R: Geometric 3D Vision Made Easy](https://arxiv.org/abs/2312.14132) — Pairwise 3D reconstruction
- [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864) — RoPE foundation

### Concepts
- **Bundle Adjustment:** The classical optimization that LingBot-Map replaces
- **SE(3) / Sim(3):** The Lie groups describing rigid / similarity transforms
- **Paged Attention:** Memory-efficient attention mechanism (from vLLM, adapted by FlashInfer)
- **DiT (Diffusion Transformer):** The iterative refinement pattern used by the camera head

### Code
- [VGGT](https://github.com/facebookresearch/vggt) — Compare the camera head and aggregator structure
- [DINOv2](https://github.com/facebookresearch/dinov2) — The backbone architecture
- [FlashInfer](https://github.com/flashinfer-ai/flashinfer) — The paged KV cache implementation

---

## Glossary

| Term | Definition |
|------|-----------|
| **Aggregator** | The transformer backbone that processes images and produces multi-scale features |
| **Camera Head** | The neural network that predicts camera poses (9-dim: T + quat + FOV) |
| **Causal Attention** | Attention where each frame can only see past frames, not future ones |
| **DPT Head** | Dense Prediction Transformer head — produces per-pixel depth/points |
| **Depth Map** | Per-pixel distance to the camera (metric) |
| **Extrinsics** | Camera pose as a 4×4 matrix (rotation + translation) |
| **FlashInfer** | Library for efficient paged attention with KV cache |
| **Intrinsics** | Camera internal parameters (focal length, principal point) |
| **Keyframe** | A frame whose KV is stored in cache (vs non-keyframe which is transient) |
| **KV Cache** | Stored Key and Value tensors from past attention computations |
| **Point Cloud** | Set of 3D points representing scene geometry |
| **Pose Encoding** | Compact 9-dim camera representation: T(3) + quat(4) + FOV(2) |
| **RoPE** | Rotary Position Embedding — encodes positions via rotation |
| **3D RoPE** | Video RoPE — extends spatial RoPE with temporal dimension |
| **Scale Frames** | Initial N frames processed together to establish scene scale |
| **Scale Token** | Special token marking scale frames (value=1) vs streaming frames (value=0) |
| **SDPA** | Scaled Dot-Product Attention — PyTorch's native attention (FlashInfer fallback) |
| **Sliding Window** | KV cache eviction policy — keep only the most recent N frames |
| **Streaming Inference** | Frame-by-frame processing with persistent KV cache |
| **Windowed Inference** | Processing long sequences as overlapping windows with fresh KV caches |
| **w2c / c2w** | World-to-camera / camera-to-world transformation matrices |
