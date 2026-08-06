# Song Cover Research — 2026-08-06

## Problem
Casey's original recording (`onedayine.mp3`, 11 seconds, 128kbps MP3, 44.1kHz stereo) fails MMX cover mode with:
```
API error: invalid params, cover mode does not support instrumental music (no lyrics detected, dtw_result is empty)
```

## Root Cause Analysis

### The MMX Cover Pipeline
MiniMax music cover mode uses Dynamic Time Warping (DTW) to align the reference audio's vocal content with new lyrics/style. The pipeline:
1. Analyzes reference audio for vocal content (ASR + beat detection)
2. Uses DTW to map vocal timing
3. Generates a new cover using the vocal map + style prompt

**Critical limitation**: If step 1 fails (no vocals detected), the entire pipeline rejects the request — even when `--lyrics` are explicitly provided. The DTW analysis runs on the *audio itself*, not the lyrics input.

### Why It Failed for Casey's Recording
1. **Duration too short**: 11.21 seconds is barely above the 6s minimum. DTW needs enough vocal data to establish alignment patterns.
2. **Low quality recording**: 128kbps, likely a phone recording or rough demo
3. **Vocals likely too quiet/muddy** for MMX's ASR to detect
4. **Demucs vocal isolation didn't help**: Even after isolating and aggressively boosting vocals, DTW still failed — suggesting the recording quality is below MMX's detection threshold

## What Was Tried

| Approach | Result | Notes |
|----------|--------|-------|
| Original audio | ❌ DTW empty | Baseline failure |
| Loudnorm normalization | ❌ DTW empty | ffmpeg loudnorm filter |
| Vocal boost (EQ + volume) | ❌ DTW empty | highpass 200Hz, lowpass 8kHz, volume 3x |
| Demucs vocal isolation | ❌ DTW empty | htdemucs model, clean separation |
| Demucs vocals + aggressive boost | ❌ DTW empty | volume 10x + loudnorm + EQ |
| Explicit lyrics provided | ❌ DTW empty | `--lyrics` flag doesn't bypass audio analysis |

## Working Approach: Generate Then Cover

Since cover mode requires detectable vocals in the reference audio, the workaround is a two-step pipeline:

### Step 1: Generate a reference track
```bash
mmx music generate --prompt "Acoustic indie folk..." --lyrics-optimizer --out reference.mp3
```
This creates a 4-minute track with clear, detectable vocals.

### Step 2: Cover the generated track
```bash
mmx music cover --prompt "Acoustic indie folk..." --audio-file reference.mp3 --out cover.mp3
```
Cover mode succeeds because the generated track has studio-quality vocals that DTW can easily analyze.

### Results
- `generate_simple.mp3` — 4:02, 7.5MB ✅
- `generate_polished.mp3` — 3:58, 7.3MB ✅ (more tailored to Casey's desired style)
- `cover_from_generated.mp3` — 3:58, 7.3MB ✅ (cover of simple generate)
- `cover_polished.mp3` — (pending, cover of polished generate)

## Alternative Approaches (Not Pursued)

### Open-Source AI Cover Tools
1. **RVC (Retrieval-Based Voice Conversion)** — Most popular open-source voice cloning for singing. Could clone Casey's voice from the 11s sample and apply it to a generated instrumental. Requires GPU for best results.
2. **So-VITS-SVC** — Higher quality than RVC but needs more training data. Original project unmaintained but community forks active.
3. **DiffSinger** — Singing voice synthesis from musical scores (lyrics + pitch + timing). Could create exact covers from sheet music.
4. **SoulX-Singer** (Feb 2026) — Zero-shot singing voice synthesis for unseen singers. Promising but untested.

### Vocal Isolation Tools
- **Demucs v4 (HTDemucs)** — Meta's state-of-the-art separator. Installed and working. Successfully separated vocals from Casey's recording.
- **UVR (Ultimate Vocal Remover)** — GUI tool supporting multiple models including Demucs.
- **Spleeter** — Deezer's older separator, less accurate than Demucs.

### Alternative Services
- **Suno** — Popular AI music generator, different pipeline than MiniMax
- **Udio** — High-quality AI music, known for vocal quality
- **ACE-Step** — Open-source, free unlimited use, requires local deployment
- **Musicfy** — 100k+ AI voices, can clone your own voice
- **TopMediai** — 8000+ AI voice models, train your own

## Recommendation

For Casey's specific use case (covering a personal song with clear lyrics):

1. **Immediate**: Use `mmx music generate` with detailed style prompt + `--lyrics-optimizer`. This produces high-quality results without needing the original audio at all. If Casey provides actual lyrics, use `--lyrics` instead of `--lyrics-optimizer` for exact control.

2. **Better**: Have Casey provide the actual lyrics. Use `mmx music generate --lyrics "<actual lyrics>"` with the folk style prompt. This gives both the right words and the right sound.

3. **Best (future)**: If Casey wants his actual voice on the cover, train an RVC model on a longer, cleaner recording of him singing, then apply voice conversion to the generated track.

## Technical Setup Notes
- ffmpeg installed via `static-ffmpeg` Python package (no sudo needed)
- Demucs v4.1.0 installed via `pip --break-system-packages`
- Path: `/home/eileen/.local/lib/python3.14/site-packages/static_ffmpeg/bin/linux/`
- MMX CLI at `~/.npm-global/bin/mmx`
- Covers directory: `/home/eileen/projects/covers/`
