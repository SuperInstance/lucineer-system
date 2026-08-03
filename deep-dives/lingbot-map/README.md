# LingBot-Map: Streaming 3D Reconstruction from Images

> **A feed-forward 3D foundation model that reconstructs scenes in real-time from image streams.**
>
> By the Robbyant Team · [Paper](https://arxiv.org/abs/2604.14141) · [GitHub](https://github.com/SuperInstance/lingbot-map) · [HuggingFace](https://huggingface.co/robbyant/lingbot-map)

---

## Table of Contents

- [What Is LingBot-Map?](#what-is-lingbot-map)
- [Why Use It?](#why-use-it)
- [Installation](#installation)
- [Model Download](#model-download)
- [Quick Start](#quick-start)
- [Full Walkthrough](#full-walkthrough)
  - [Step 1: Prepare Your Images](#step-1-prepare-your-images)
  - [Step 2: Run Streaming Inference](#step-2-run-streaming-inference)
  - [Step 3: Explore the 3D Viewer](#step-3-explore-the-3d-viewer)
  - [Step 4: Sky Masking for Outdoor Scenes](#step-4-sky-masking-for-outdoor-scenes)
  - [Step 5: Keyframe Interval for Long Sequences](#step-5-keyframe-interval-for-long-sequences)
  - [Step 6: Windowed Inference for Very Long Videos](#step-6-windowed-inference-for-very-long-videos)
  - [Step 7: Offline Rendering Pipeline](#step-7-offline-rendering-pipeline)
  - [Step 8: torch.compile Acceleration](#step-8-torchcompile-acceleration)
- [API Reference](#api-reference)
  - [Python API](#python-api)
  - [CLI Flags](#cli-flags)
  - [Output Format](#output-format)
- [Troubleshooting](#troubleshooting)
- [How It Works](#how-it-works)

---

## What Is LingBot-Map?

LingBot-Map (Geometric Context Transformer) is a deep learning model that takes a sequence of RGB images and produces a **dense 3D reconstruction** of the scene — camera poses, depth maps, and colored point clouds — all in a single feed-forward pass. No bundle adjustment, no feature matching, no iterative optimization.

**Key characteristics:**

- **Streaming:** Processes frames one-at-a-time with a KV cache, enabling real-time reconstruction
- **Drift-resistant:** 3D RoPE (Rotary Position Embedding) maintains geometric consistency over 10,000+ frames
- **Feed-forward:** Single forward pass per frame; no test-time optimization
- **Metric scale:** Scale frames establish real-world units
- **~20 FPS** at 518×378 resolution on a single GPU

---

## Why Use It?

| Use Case | How LingBot-Map Helps |
|----------|----------------------|
| **3D scanning a room** | Walk through with a camera → get a point cloud |
| **Visual SLAM** | Real-time camera tracking + dense depth |
| **AR/VR scene capture** | Reconstruct environments for immersive experiences |
| **Game world building** | Photograph a real place → import as 3D geometry |
| **Architectural documentation** | Photo collection → metric 3D model |
| **Robotics navigation** | Depth estimation + pose estimation for path planning |

**Compared to alternatives:**

| System | Speed | Length Limit | Optimization | Setup |
|--------|-------|-------------|-------------|-------|
| **LingBot-Map** | ~20 FPS | 10,000+ frames | None (feed-forward) | Just images |
| COLMAP | Hours | Unlimited | Bundle adjustment | Needs features |
| ORB-SLAM3 | ~30 FPS | Unlimited | Local BA | Needs features |
| DUSt3R | Seconds | 2 images | None | Image pair |
| NeRF/3DGS | Minutes | Fixed scene | Gradient descent | Multi-view |

---

## Installation

### Prerequisites

- **GPU:** NVIDIA GPU, compute capability ≥ 8.0 (Ampere or newer). Minimum 8 GB VRAM; 16+ GB recommended for long sequences.
- **CUDA:** 12.8 or compatible
- **Python:** 3.10, 3.11, or 3.12
- **OS:** Linux recommended (Windows/WSL2 works; macOS not supported — no CUDA)

### Step-by-Step Install

```bash
# 1. Create environment
conda create -n lingbot-map python=3.10 -y
conda activate lingbot-map

# 2. Install PyTorch (CUDA 12.8)
pip install torch==2.8.0 torchvision==0.23.0 \
    --index-url https://download.pytorch.org/whl/cu128

# 3. Clone and install LingBot-Map
git clone https://github.com/SuperInstance/lingbot-map.git
cd lingbot-map
pip install -e .

# 4. Install FlashInfer (strongly recommended)
pip install --index-url https://pypi.org/simple flashinfer-python

# 5. Install visualization dependencies
pip install -e ".[vis]"
```

### Verify Installation

```bash
python -c "from lingbot_map.models.gct_stream import GCTStream; print('OK')"
python -c "import flashinfer; print(f'FlashInfer {flashinfer.__version__}')"
```

---

## Model Download

Download pre-trained checkpoints from HuggingFace:

```bash
# Recommended checkpoint (best for long sequences)
huggingface-cli download robbyant/lingbot-map lingbot-map-long.pt \
    --local-dir ./checkpoints

# Balanced checkpoint (all-around performance)
huggingface-cli download robbyant/lingbot-map lingbot-map.pt \
    --local-dir ./checkpoints
```

| Checkpoint | Best For | HuggingFace |
|-----------|----------|-------------|
| `lingbot-map-long.pt` | Long sequences, large scenes (recommended) | [Download](https://huggingface.co/robbyant/lingbot-map) |
| `lingbot-map.pt` | Balanced short + long sequences | [Download](https://huggingface.co/robbyant/lingbot-map) |
| `lingbot-map-stage1.pt` | Bidirectional inference (VGGT-compatible) | [Download](https://huggingface.co/robbyant/lingbot-map) |

---

## Quick Start

```bash
# Your first 3D reconstruction!
python demo.py \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --image_folder example/courthouse \
    --mask_sky
```

This launches an interactive 3D viewer at `http://localhost:8080`. Open it in your browser to see the reconstructed point cloud, camera trajectory, and depth maps.

---

## Full Walkthrough

### Step 1: Prepare Your Images

LingBot-Map accepts either a folder of images or a video file.

**From a folder** (photos or extracted frames):
```bash
mkdir my_scene
# Copy JPEG or PNG images, named sequentially (000000.jpg, 000001.jpg, ...)
cp /path/to/photos/*.jpg my_scene/

python demo.py \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --image_folder my_scene --mask_sky
```

**From a video file:**
```bash
python demo.py \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --video_path walkthrough.mp4 \
    --fps 10 \
    --mask_sky
```

The `--fps` flag controls frame extraction rate. For a 30 FPS source video at `--fps 10`, every 3rd frame is used.

**Tips for good results:**
- Images should have **≥ 50% overlap** between consecutive frames
- Avoid pure rotation (keep some translation between frames)
- Consistent lighting helps (avoid dramatic exposure changes)
- 100–500 frames is a good starting point; scale up from there

### Step 2: Run Streaming Inference

The default mode is `streaming`:

```bash
python demo.py \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --image_folder my_scene \
    --mode streaming \
    --mask_sky \
    --conf_threshold 1.5 \
    --point_size 0.00001 \
    --downsample_factor 10
```

**What happens during inference:**

1. **Phase 1 (Scale):** The first 8 frames are processed together to establish scene scale and coordinate frame
2. **Phase 2 (Streaming):** Remaining frames are processed one-by-one, each attending to the KV cache of all previous keyframes
3. **Post-processing:** Pose encodings are converted to camera extrinsics (c2w), depth maps are converted to world points

Console output shows per-frame progress and GPU memory usage:
```
Processing 8 scale frames...
Streaming inference:  12%|██▎       | 35/283 [00:02<00:14, 17.3fps]
Inference done in 16.3s
GPU peak during inference: 6.82 GB
```

### Step 3: Explore the 3D Viewer

The [Viser](https://github.com/nerfstudio-project/viser) viewer provides:

- **Point cloud** — colored 3D points from depth unprojection
- **Camera frustums** — shows where each photo was taken
- **Trajectory line** — connects camera positions
- **Playback controls** — animate through frames

Controls:
- Click and drag to orbit
- Scroll to zoom
- Right-click drag to pan
- Use the control panel (left sidebar) to adjust point size, confidence threshold, etc.

### Step 4: Sky Masking for Outdoor Scenes

Outdoor scenes often have sky, which produces meaningless geometry. Enable sky masking:

```bash
# First-time: install onnxruntime
pip install onnxruntime        # CPU
# OR
pip install onnxruntime-gpu    # GPU (faster for large sets)

# Run with sky masking
python demo.py \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --image_folder outdoor_scene \
    --mask_sky \
    --sky_mask_dir ./sky_masks \
    --sky_mask_visualization_dir ./sky_viz
```

The sky segmentation model (`skyseg.onnx`) auto-downloads on first use. Masks are cached in `--sky_mask_dir` so subsequent runs skip re-processing.

### Step 5: Keyframe Interval for Long Sequences

For sequences longer than 320 frames, use keyframe interval to bound KV cache memory:

```bash
python demo.py \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --image_folder long_sequence \
    --keyframe_interval 2 \
    --mask_sky
```

**How it works:** Every Nth frame (after scale frames) is a keyframe. Keyframes' KV is stored in cache; non-keyframes still produce predictions but their KV isn't stored. This reduces memory by ~1/N×.

If `--keyframe_interval` is not specified and the sequence exceeds 320 frames, it's auto-selected:
```
Auto-selected --keyframe_interval=2 (num_frames=640 > 320).
```

### Step 6: Windowed Inference for Very Long Videos

For sequences >3,000 frames, use windowed mode:

```bash
python demo.py \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --video_path very_long_video.mp4 --fps 10 \
    --mode windowed \
    --window_size 128 \
    --overlap_keyframes 16 \
    --keyframe_interval 2 \
    --mask_sky
```

**Understanding window parameters:**

- `--window_size 128`: 128 KV-cache slots per window (including 8 scale frames)
- `--keyframe_interval 2`: Every 2nd streaming frame is cached → each window covers `8 + 120×2 = 248` actual frames
- `--overlap_keyframes 16`: Adjacent windows share 16 keyframes = `16×2 = 32` actual frames of overlap

Windows are processed independently with fresh KV caches, then aligned via similarity transforms (scale + rotation + translation estimated from overlapping depth maps and poses).

### Step 7: Offline Rendering Pipeline

For producing rendered flythrough videos of very long sequences:

```bash
# Additional dependencies
pip install -e ".[vis,render]"
pip install --index-url https://pypi.org/simple \
    kaolin -f https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.8.0_cu128.html
sudo apt install ffmpeg

# Build CUDA extensions
cd demo_render/render_cuda_ext && python setup.py build_ext --inplace && cd ../..

# Run the batch demo
python demo_render/batch_demo.py \
    --video_path indoor_walkthrough.MP4 \
    --output_folder ./output \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --config demo_render/config/indoor.yaml \
    --mode windowed --window_size 128 \
    --keyframe_interval 13 --overlap_keyframes 8 \
    --mask_sky \
    --camera_vis default \
    --keyframes_only_points \
    --frame_tag --frame_tag_position top_right \
    --save_predictions
```

**Output files:**

| File | Description |
|------|-------------|
| `<name>_pointcloud.mp4` | Rendered point-cloud flythrough video |
| `<name>_pointcloud_rgb.mp4` | Original RGB frames for reference |
| `<name>_pointcloud_config.yaml` | Full config snapshot |
| `batch_results.json` | Success/duration summary |

**Camera path customization:** Edit the YAML preset to design your virtual camera shot:

```yaml
camera:
  fov: 60.0
  transition: 30
  segments:
    - mode: follow         # Chase cam following the trajectory
      frames: [0, 1500]
      back_offset: 0.3
      up_offset: 0.08
      look_offset: 0.4
      smooth_window: 30
    - mode: birdeye        # Top-down reveal
      frames: [1500, 1800]
      reveal_height_mult: 2.5
    - mode: follow         # Back to chase cam
      frames: [1800, -1]
      back_offset: 0.3
      up_offset: 0.08
      look_offset: 0.4
```

Available modes: `follow`, `birdeye`, `static`, `pivot`.

### Step 8: torch.compile Acceleration

For ~5 FPS speedup on streaming inference:

```bash
python demo.py \
    --model_path ./checkpoints/lingbot-map-long.pt \
    --image_folder my_scene \
    --compile \
    --mode streaming
```

**Note:** Compile adds 30–60 seconds warmup time. It only applies to `--mode streaming` and requires FlashInfer (not compatible with SDPA + compile).

---

## API Reference

### Python API

#### Basic Usage

```python
import torch
from lingbot_map.models.gct_stream import GCTStream
from lingbot_map.utils.load_fn import load_and_preprocess_images
from lingbot_map.utils.pose_enc import pose_encoding_to_extri_intri

# Load model
model = GCTStream(
    img_size=518,
    patch_size=14,
    enable_3d_rope=True,
    max_frame_num=1024,
    kv_cache_sliding_window=64,
    kv_cache_scale_frames=8,
    use_sdpa=False,          # False = FlashInfer (recommended)
    camera_num_iterations=4,
).to('cuda').eval()

# Load checkpoint
ckpt = torch.load('checkpoints/lingbot-map-long.pt', map_location='cuda')
model.load_state_dict(ckpt.get('model', ckpt), strict=False)

# Load and preprocess images
images = load_and_preprocess_images(
    image_path_list=['img001.jpg', 'img002.jpg', ...],
    mode='crop',
    image_size=518,
    patch_size=14,
)  # Shape: [N, 3, 378, 518]

# Streaming inference
with torch.no_grad(), torch.amp.autocast('cuda', dtype=torch.bfloat16):
    predictions = model.inference_streaming(
        images.to('cuda'),
        num_scale_frames=8,
        keyframe_interval=1,
        output_device=torch.device('cpu'),  # Offload to CPU to save GPU memory
    )

# Access results
pose_enc = predictions['pose_enc']        # [1, N, 9] — T(3) + quat(4) + FOV(2)
depth = predictions['depth']              # [1, N, H, W, 1]
depth_conf = predictions['depth_conf']    # [1, N, H, W]
world_points = predictions['world_points']  # [1, N, H, W, 3]
world_points_conf = predictions['world_points_conf']  # [1, N, H, W]

# Convert pose encoding to extrinsics + intrinsics
extrinsics, intrinsics = pose_encoding_to_extri_intri(pose_enc, images.shape[-2:])
```

#### GCTStream Constructor Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `img_size` | 518 | Input image size (canonical crop to 518×378) |
| `patch_size` | 14 | ViT patch size |
| `embed_dim` | 1024 | Embedding dimension (ViT-Large) |
| `patch_embed` | `'dinov2_vitl14_reg'` | Patch embedding variant |
| `enable_3d_rope` | `True` | Enable 3D video RoPE for temporal encoding |
| `max_frame_num` | 1024 | Maximum frames for RoPE position encoding |
| `kv_cache_sliding_window` | 64 | Sliding window size for KV cache eviction |
| `kv_cache_scale_frames` | 8 | Number of always-resident scale frames |
| `kv_cache_cross_frame_special` | `True` | Keep special tokens from evicted frames |
| `kv_cache_include_scale_frames` | `True` | Include scale frames in KV cache |
| `use_sdpa` | `False` | Use SDPA instead of FlashInfer |
| `camera_num_iterations` | 4 | Camera head refinement iterations |

#### `inference_streaming()` Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `images` | `Tensor [S, 3, H, W]` or `[B, S, 3, H, W]` | Input images in [0, 1] |
| `num_scale_frames` | `int` | Number of initial scale estimation frames |
| `keyframe_interval` | `int` | Cache every Nth frame (1 = all frames) |
| `output_device` | `torch.device` | Device for outputs (use `cpu` to save GPU memory) |

#### `inference_windowed()` Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `images` | `Tensor` | Input images |
| `window_size` | `int` | Keyframes per window (including scale) |
| `overlap_size` | `int` | Overlap in actual frames |
| `overlap_keyframes` | `int` | Overlap in keyframes (takes precedence) |
| `num_scale_frames` | `int` | Scale frames per window |
| `keyframe_interval` | `int` | Keyframe interval within windows |
| `output_device` | `torch.device` | Output device |

### CLI Flags

See the [original README](https://github.com/SuperInstance/lingbot-map#-interactive-demo-demopy) for the full flag reference. Most important:

| Flag | Default | Description |
|------|---------|-------------|
| `--model_path` | (required) | Path to checkpoint |
| `--image_folder` | — | Folder of input images |
| `--video_path` | — | Video file input |
| `--fps` | 10 | Frame extraction rate (video mode) |
| `--mode` | `streaming` | `streaming` or `windowed` |
| `--keyframe_interval` | auto | Cache every Nth frame |
| `--window_size` | 64 | Window keyframes (windowed mode) |
| `--mask_sky` | off | Enable sky segmentation |
| `--compile` | off | torch.compile hot modules |
| `--use_sdpa` | off | Use SDPA instead of FlashInfer |
| `--offload_to_cpu` | off | Offload predictions to CPU |
| `--num_scale_frames` | 8 | Scale estimation frames |
| `--camera_num_iterations` | 4 | Camera refinement steps (set 1 for speed) |

### Output Format

All outputs are dictionaries of tensors with batch dimension first:

| Key | Shape | Description |
|-----|-------|-------------|
| `pose_enc` | `[B, S, 9]` | T(3) + quaternion(4) + FOV(2) |
| `depth` | `[B, S, H, W, 1]` | Per-pixel metric depth |
| `depth_conf` | `[B, S, H, W]` | Depth confidence (≥1.0 = high) |
| `world_points` | `[B, S, H, W, 3]` | Per-pixel 3D world coordinates |
| `world_points_conf` | `[B, S, H, W]` | Point confidence |
| `extrinsic` | `[B, S, 3, 4]` | Camera-to-world matrices |
| `intrinsic` | `[B, S, 3, 3]` | Camera intrinsics |
| `images` | `[B, S, 3, H, W]` | Original images |

---

## Troubleshooting

### CUDA Out of Memory

```
RuntimeError: CUDA out of memory.
```

**Solutions (in order of impact):**

1. Add `--offload_to_cpu` to move predictions off GPU
2. Reduce scale frames: `--num_scale_frames 2`
3. Use keyframe interval: `--keyframe_interval 4`
4. Use SDPA (lower memory): `--use_sdpa`
5. Process shorter sequences

### FlashInfer Not Found

```
ModuleNotFoundError: No module named 'flashinfer'
```

**Solution:** Install FlashInfer or use SDPA fallback:
```bash
pip install flashinfer-python
# OR
python demo.py ... --use_sdpa
```

### Poor Reconstruction Quality

**Symptoms:** Point cloud is noisy, misaligned, or has floating artifacts.

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| Too few images | Use ≥ 50 images with good overlap |
| Fast camera motion | Reduce video FPS: `--fps 5` |
| Low texture scenes | Add more lighting variation |
| Featureless surfaces (white walls) | Expected — model has little to work with |
| Sky contamination | Use `--mask_sky` |
| Pose drift (long sequences) | Use `--mode windowed` or increase `--keyframe_interval` |

### Pose Collapse (Long Sequences)

**Symptoms:** Camera trajectory suddenly jumps or rotates wildly.

**Cause:** KV cache exceeded training range (320 views) without sufficient keyframe reduction.

**Fix:**
```bash
# Switch to windowed mode
--mode windowed --window_size 128 --overlap_keyframes 16 --keyframe_interval 2
```

### Sky Segmentation Model Download Failure

```
ConnectionError: Failed to download skyseg.onnx
```

**Fix:** Download manually from [HuggingFace](https://huggingface.co/JianyuanWang/skyseg/resolve/main/skyseg.onnx) and place in the expected cache directory.

### torch.compile Errors

```
RuntimeError: Expected curr_block->next == nullptr
```

**Cause:** `expandable_segments:True` CUDA allocator conflicts with torch.compile's CUDA graph mode.

**Fix:** The code automatically handles this when `--compile` is passed. If you still see the error, ensure you're not setting `PYTORCH_CUDA_ALLOC_CONF` manually.

### Slow Inference

**Target:** ~20 FPS at 518×378 on a modern GPU.

**If you're slower:**

1. Ensure FlashInfer is installed (not SDPA)
2. Use `--compile` (adds warmup but ~5 FPS faster steady-state)
3. Reduce camera iterations: `--camera_num_iterations 1`
4. Check GPU is not thermal throttling
5. Ensure you're using bf16 (compute capability ≥ 8.0)

---

## How It Works

### Architecture Summary

```
Images → DINOv2 Patch Embed → Frame Attention (24 blocks, 2D RoPE)
                                    ↓
                            Global Attention (24 blocks, 3D RoPE, KV Cache)
                                    ↓
                    ┌───────────────┼───────────────┐
                    ↓               ↓               ↓
              Camera Head      Depth Head      Point Head
              (iterative)      (DPT)           (DPT)
                    ↓               ↓               ↓
                Poses (9-dim)   Depth + Conf    3D Points + Conf
```

### Key Innovations

1. **Scale Token:** The first N frames get a scale token value of 1; all others get 0. This teaches the model to anchor metric scale from the initial frames and propagate it through the stream.

2. **3D Video RoPE:** Extends 2D spatial RoPE to 3D (frame, y, x), giving the model temporal position awareness in the KV cache. This prevents the "are these tokens from frame 5 or frame 5000?" ambiguity.

3. **Paged KV Cache:** FlashInfer's paged attention allows efficient sliding-window eviction — old frames' KV is recycled, keeping memory bounded. Two streams: patch pages (recyclable) and special token pages (append-only, for persistent cross-frame context).

4. **Iterative Camera Refinement:** The camera head runs N iterations of: predict pose delta → apply delta → re-encode → modulate features. Like a DiT (Diffusion Transformer) but for camera poses. Each iteration refines the estimate using temporal context from the camera KV cache.

5. **Cross-Window Alignment:** For very long sequences, each window's predictions are aligned to the previous window via estimated similarity transforms (scale from depth ratios, rotation from quaternion decomposition, translation from camera centers).

### Training

The model is trained in two stages:
- **Stage 1:** Bidirectional inference (VGGT-compatible) — all frames see each other
- **Stage 2:** Causal streaming — frames only see past frames, teaching the model to maintain consistency through the KV cache

Training uses 320 views per sequence with video RoPE, which is why performance degrades beyond 320 KV-cached frames without keyframe intervals.

---

## Citation

```bibtex
@article{chen2026geometric,
  title={Geometric Context Transformer for Streaming 3D Reconstruction},
  author={Chen, Lin-Zhuo and Gao, Jian and Chen, Yihang and Cheng, Ka Leong
          and Sun, Yipengjing and Hu, Liangxiao and Xue, Nan and Zhu, Xing
          and Shen, Yujun and Yao, Yao and Xu, Yinghao},
  journal={arXiv preprint arXiv:2604.14141},
  year={2026}
}
```

---

## License

Apache License 2.0 — see [LICENSE.txt](https://github.com/SuperInstance/lingbot-map/blob/main/LICENSE.txt).
