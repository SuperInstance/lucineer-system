# Chiaroscuro Capture — Concrete Build Plan

Date: 2026-09-27 · Verified against MDN + developer.chrome.com the same day (web_search was rate-limited; direct doc fetches used).

## Feature → API decisions

**1. Selection box.** Primary: **Region Capture** (`CropTarget.fromElement()` + `track.cropTo()`) — shipped, stable in Chrome (Chrome 104+; documented as shipping, not flag-gated, as of late 2026). Inject an overlay `<div>` the user drags/resizes; derive a CropTarget from it; call `getDisplayMedia({ preferCurrentTab: true, selfBrowserSurface: "include" })` then `await track.cropTo(cropTarget)`. Zero-copy (browser compositor crops), and the crop **follows the element** through scroll/resize/layout — no per-frame math. Upgrade option: **Element Capture** (`RestrictionTarget.fromElement()` + `track.restrictTo()`, Chrome 122+) removes occluding/occluded content; self-capture only.

**2. Background capture (browser not active).** Tab-capture tracks keep producing frames while the captured tab is unfocused/occluded — that's how tab-share in Meet works. The capture side stays live because frame delivery is **push-based streams, not rAF/timers**, and dedicated workers escape background-tab throttling. Record with `MediaRecorder` (universally shipped; prefer `video/webm;codecs=vp9`, fall back vp8, Safari mp4). Extension-native upgrade for capturing *other* tabs with no picker and no visible UI: `chrome.tabCapture.getMediaStreamId()` → stream consumed in an MV3 **offscreen document**; the worker pipeline is identical.

**3. Two-panel realtime viewer.** Left: `<video srcObject=croppedStream>`. Right: `<canvas>` whose control is **transferred to an OffscreenCanvas** living in the same worker (OffscreenCanvas is Baseline 2023: Chrome 69 / FF 105 / Safari 16.4). Worker does luminance sampling → glyph raster per VideoFrame; `ctx.drawImage(videoFrame, …)` accepts VideoFrame directly. Both panels update in lockstep off-main-thread.

**4. Loaded-in video file.** `<input type="file">` → object URL → hidden `<video>`. Two entry points into the *same* transform: (a) `video.captureStream()` → treat exactly like a capture track; or (b) `video.requestVideoFrameCallback()` + `new VideoFrame(videoEl)` per callback (WebCodecs VideoFrame is constructible from video/canvas/ImageBitmap). Pause/seek/playbackRate all work; drop rate below 1× for heavy ASCII densities.

## Pipeline (frame-grab → render → display)

1. Main thread: selection overlay → `getDisplayMedia({preferCurrentTab:true})` → `track.cropTo(cropTarget)` (or tabCapture stream, or file track).
2. `worker.postMessage({track}, [track])` — track is transferable.
3. Worker: `new MediaStreamTrackProcessor({track}).readable` → `ReadableStream<VideoFrame>`.
4. `readable.pipeThrough(asciiTransform)` — TransformStream samples pixels (copy into Uint8ClampedArray; luma = 0.2126R+0.7152G+0.0722B), quantizes to glyph ramp, draws glyphs on the transferred OffscreenCanvas.
5. Display: the OffscreenCanvas's placeholder `<canvas>` is the right panel; original `<video>` is the left panel.
6. Record: `readable.pipeTo(vtg.writable)` on a `VideoTrackGenerator` (spec form, worker-only) or `MediaStreamTrackGenerator` (Chrome's window+worker form, shipped Chrome 94) → `new MediaStream([vtg.track])` → MediaRecorder → webm blob. Note: MDN flags MediaStreamTrackProcessor "Limited availability" — Chrome exposes it in window *and* worker; Safari worker-only. **Target the worker context; it's the portable spec form and doubles as the throttling shield.**

## Fallback paths

- **No Region/Element Capture** (Firefox/Safari): software crop in the worker — draw full-surface frames, `drawImage` with source rect from overlay coordinates (poll `getBoundingClientRect` or hook rVFC). Loses auto-follow; acceptable v1 fallback.
- **No MediaStreamTrackProcessor**: hidden `<video>` + `requestVideoFrameCallback` + drawImage loop on main thread. Works, but is rAF-throttled when hidden → background capture degrades to foreground-only. This is the one feature with no clean cross-browser fallback; document it.
- **WSL2/Chrome caveats**: under WSLg, monitor/screen capture needs xdg-desktop-portal + PipeWire, which is typically broken/absent → empty picker or black frames. **Tab and window capture are browser-internal and unaffected** — another reason `preferCurrentTab`/tabCapture is the spine. GPU acceleration via D3D12 passthrough is flaky; if `chrome://gpu` shows SwiftShader fallback, the pipeline still works (it's CPU 2D-canvas + software VP8 encode by design); force `--disable-gpu` for determinism.

## Load-bearing choice

**Region Capture `cropTo()` on a `preferCurrentTab` self-capture track.** Every feature consumes its output as an ordinary MediaStreamTrack of VideoFrames — worker pipeline, dual-panel viewer, MediaRecorder, tabCapture and file modes all normalize to that same track contract. It's shipping (not flag-gated), zero-copy, layout-tracking, and background-safe; everything else is plumbing around it.
