# Browser-Native AI: Deep Research for the Slackwater Cognition Architecture

> **Research date:** 2026-08-03
> **Goal:** Evaluate every browser-native AI capability and how it could enhance the Slackwater thought viewer, Local Thinker, Conductor loop, and resonator pattern.
> **Context:** The Dynamic Cognition Architecture uses a Local Thinker (Granite 2B / Llama 3.2 1B) that generates a stream-of-consciousness journal, a Conductor (server-side LLM) that steers it, and a Game layer (Roblox/Slackwater) that provides state. The Thought Viewer is the web-native window into this loop.

---

## Table of Contents

1. [Chrome Built-in AI APIs (Gemini Nano)](#1-chrome-built-in-ai-apis-gemini-nano)
2. [WebGPU / WebNN — Browser-Native ML Inference](#2-webgpu--webnn--browser-native-ml-inference)
3. [Chrome Extensions API](#3-chrome-extensions-api)
4. [Chrome Side Panel API](#4-chrome-side-panel-api)
5. [Web Audio API](#5-web-audio-api)
6. [WebSocket / Server-Sent Events](#6-websocket--server-sent-events)
7. [IndexedDB / OPFS](#7-indexeddb--opfs)
8. [Web Workers / SharedArrayBuffer](#8-web-workers--sharedarraybuffer)
9. [Canvas / WebGL / WebGPU Compute](#9-canvas--webgl--webgpu-compute)
10. [WebRTC](#10-webrtc)
11. [Progressive Web App (PWA)](#11-progressive-web-app-pwa)
12. [Omnibox API](#12-omnibox-api)
13. [Synthesis: Architecture Integration Map](#13-synthesis-architecture-integration-map)

---

## 1. Chrome Built-in AI APIs (Gemini Nano)

### What it is

Chrome ships with **Gemini Nano** — a ~2.7B parameter on-device model — built directly into the browser (Chrome 138+, stable as of mid-2025). The model is downloaded on first use (~22 GB disk space required, runs on GPU >4 GB VRAM or CPU ≥16 GB RAM, 4+ cores). Chrome exposes multiple purpose-built APIs on top of this model:

#### Available APIs (Chrome 138–148, 2025–2026)

| API | Status | Chrome Version | What It Does |
|-----|--------|---------------|--------------|
| **Prompt API** (`LanguageModel`) | ✅ Stable (Chrome 138) | 138+ | Free-form natural language prompts to Gemini Nano. Supports system/user/assistant roles, streaming, multimodal input (text + image + audio), temperature/topK control (extensions only), initial prompts for context, prefix completion. |
| **Summarizer API** (`Summarizer`) | ✅ Stable (Chrome 138) | 138+ | Generates summaries in 4 types (key-points, tldr, teaser, headline) × 3 lengths (short/medium/long) × 2 formats (markdown/plain-text). Supports `sharedContext`, language specification (en, ja, es, de, fr), LoRA-enhanced quality. |
| **Writer API** (`Writer`) | 🟡 Origin Trial (Chrome 137–148) | 137+ | Creates new content from a task description + context. Configurable tone (formal/neutral/casual), format (markdown/plain-text), length (short/medium/long). Streaming and request-based output. |
| **Rewriter API** (`Rewriter`) | 🟡 Origin Trial (Chrome 137–148) | 137+ | Rewrites existing text — make longer/shorter, change tone. Companion to Writer. |
| **Translator API** (`Translator`) | ✅ Stable | Desktop only | On-device translation between 40+ languages. Per-language-pair model download. Streaming support. |
| **Language Detector** (`LanguageDetector`) | ✅ Stable | Desktop only | Detects the language of input text. |
| **Proofreader API** (`Proofreader`) | 🔬 Early Preview | EPP only | Grammar/spelling/style correction. |

#### Key Technical Details

```javascript
// Prompt API — the most flexible
const availability = await LanguageModel.availability();
// 'available' | 'downloadable' | 'downloading' | 'unavailable'

const session = await LanguageModel.create({
  initialPrompts: [
    { role: 'system', content: 'You are a thought stream analyzer...' },
    { role: 'user', content: previousThought },
    { role: 'assistant', content: previousAnalysis },
  ],
  monitor(m) {
    m.addEventListener('downloadprogress', (e) => {
      console.log(`Downloaded ${e.loaded * 100}%`);
    });
  },
});

// Streaming output
const stream = session.promptStreaming("Analyze this thought pattern...");
for await (const chunk of stream) {
  console.log(chunk);
}

// Multimodal input (Chrome 148+)
const result = await session.prompt([
  { type: "text", text: "What's in this image?" },
  { type: "image", image: imageBitmap },
]);

// Audio input (Chrome 148+, requires GPU)
const audioResult = await session.prompt([
  { type: "audio", audio: audioBuffer },
]);
```

**Extension-specific features:**
- `LanguageModel.params()` returns `{defaultTopK, maxTopK, defaultTemperature, maxTemperature}`
- Extensions can set `topK` and `temperature` on session creation (web pages cannot)
- Extensions register via `chrome-extension://YOUR_EXTENSION_ID` in origin trials

### How It Enhances the Cognition Architecture

This is the **most transformative capability** for the thought viewer. Here's why:

1. **Client-Side Thought Analysis** — The viewer can run Gemini Nano locally to classify thoughts (novelty, emotional register, spatial awareness) without a server round-trip. The Conductor's quality-scoring step can happen in the browser.

2. **Real-Time Summarization** — The Summarizer API can compress 30 thoughts into a headline or key-points list in <500ms, entirely on-device. This gives the viewer a "what just happened" banner that updates live.

3. **Thought Rewriting/Refinement** — The Writer/Rewriter APIs could let users interactively refine thought prompts — "make this thought more curious" or "rewrite in a more analytical tone" — directly in the viewer.

4. **Privacy-Preserving Pattern Detection** — Because Gemini Nano runs on-device, sensitive thought journals never leave the browser. This matters if the thought viewer is ever shared or demoed.

5. **Multimodal Thought Input** — Audio input (Chrome 148+) means voice thoughts. Image input means the Local Thinker could "see" screenshots of the game state.

6. **Zero-Cost Inference** — No API costs. Every thought analysis, every summary, every rewrite is free. The Conductor's server-side budget is reserved for deep reasoning only.

### Replaces or Complements?

**Complements** the server-side Conductor. Gemini Nano (~2.7B) cannot replace GLM-5.2 or Claude Opus for deep reasoning, prompt strategy, or complex analysis. But it **can replace**:
- The quality-scoring micro-service (novelty, specificity metrics)
- The summarization service for the viewer
- The translation layer (if multi-language viewers)
- Lightweight pattern detection (repetition alerts, tone shifts)

**Could partially replace** the Local Thinker itself — if the Local Thinker's job is generating 2-4 sentence thoughts from game state, Gemini Nano can do that in-browser at reasonable speed. But Granite 2B via Ollama gives more control over the model and doesn't require Chrome.

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| Thought summarizer in viewer | 🟢 Small (1-2 days) | `Summarizer.create()` + streaming, fallback to API |
| Quality scoring in viewer | 🟡 Medium (3-5 days) | Prompt API with few-shot examples for scoring |
| Thought rewriter UI | 🟡 Medium (3-5 days) | Writer API + CodeMirror ghost text |
| Replace Local Thinker with Gemini Nano | 🔴 Large (1-2 weeks) | Full architecture change, loses model control |
| Multimodal thoughts (audio/image) | 🔴 Large (1 week) | Chrome 148+ only, requires GPU |

### Production Readiness

- **Prompt API**: ✅ Production-ready (Chrome 138 stable). Origin trial for sampling parameters (topK/temperature on web).
- **Summarizer API**: ✅ Production-ready (Chrome 138 stable).
- **Writer/Rewriter API**: 🟡 Origin trial through Chrome 148. Will ship stable.
- **Translator API**: ✅ Production-ready, desktop only.
- **Hardware requirements**: Significant — 22 GB disk, 4+ GB VRAM or 16 GB RAM. This limits audience. Must have graceful fallback to server-side APIs.

---

## 2. WebGPU / WebNN — Browser-Native ML Inference

### What it is

**WebGPU** is the modern browser GPU API (successor to WebGL), shipping in Chrome 113+, Edge 113+, Safari 17.4+. It provides first-class support for general-purpose GPU (GPGPU) computations — not just graphics. It can access discrete GPUs (NVIDIA, AMD) and integrated GPUs (Intel, Apple Silicon).

**WebNN** (Web Neural Network API) is a higher-level API specifically for ML inference. It abstracts away GPU shader writing and provides direct access to hardware ML acceleration (TensorFlow Lite delegation, Core ML on macOS, DirectML on Windows). WebNN is available in Chrome behind flags and in origin trials; ONNX Runtime Web supports it as an execution provider.

#### Frameworks for Browser-Native ML

| Framework | What It Does | WebGPU | WebNN | Model Format | Bundle Size |
|-----------|-------------|--------|-------|-------------|-------------|
| **Transformers.js** (v4.2) | Hugging Face models in browser — NLP, vision, audio, multimodal | ✅ `device: 'webgpu'` | ✅ (via ONNX Runtime) | ONNX | ~50KB (lib only) |
| **ONNX Runtime Web** | Microsoft's inference engine — any ONNX model | ✅ | ✅ `deviceType: 'gpu'` | ONNX | ~1.5MB (wasm) |
| **TensorFlow.js** | Google's browser ML library | ✅ (via WebGL/WebGPU backend) | 🔬 Experimental | TFJS format | ~1MB |

#### Can We Run Small Models in Browser?

**Yes.** Transformers.js supports running these models directly in the browser with WebGPU acceleration:

| Model | Size (quantized) | Speed (WebGPU) | Use Case |
|-------|-----------------|----------------|----------|
| **Llama 3.2-1B** | ~700 MB (q4) | ~15-30 tok/s | Local Thinker replacement |
| **Llama 3.2-3B** | ~1.7 GB (q4) | ~8-15 tok/s | Higher quality thinker |
| **Granite 3.1-2B** | ~1.2 GB (q8) | ~10-20 tok/s | Exact Local Thinker model |
| **Phi-3-mini (3.8B)** | ~2.2 GB (q4) | ~6-12 tok/s | Strong reasoning locally |
| **Qwen 2.5-1.5B** | ~900 MB (q4) | ~15-30 tok/s | Fast thinker |
| **DistilBERT** | ~65 MB (q8) | <50ms inference | Classification, sentiment |
| **YOLOv8-nano** | ~12 MB | ~30 fps | Object detection (vision system) |
| **Whisper-tiny** | ~75 MB | Near-real-time | Speech-to-text |
| **bge-m3** (embeddings) | ~300 MB (q8) | Fast | Semantic search of thoughts |

```javascript
// Running Granite 2B in the browser with Transformers.js
import { pipeline } from '@huggingface/transformers';

const thinker = await pipeline(
  'text-generation',
  'onnx-community/granite-3.1-2b-instruct-q4',
  { device: 'webgpu', dtype: 'q4' }
);

const stream = await thinker("The dock looks unfinished...", {
  max_new_tokens: 100,
  streaming: true,
});
```

### How It Enhances the Cognition Architecture

1. **The Local Thinker Can Run IN the Browser** — Instead of requiring Ollama on a server, the thought viewer itself can host the thinker. This eliminates network latency (~500ms → ~50ms for first token) and makes the viewer fully self-contained.

2. **Client-Side Embeddings for Thought Search** — Run bge-m3 in the browser to embed thoughts as they're generated. The viewer gets instant semantic search over the thought journal without a Vectorize round-trip.

3. **In-Browser Vision System** — YOLOv8-nano can run at 30fps on WebGPU, analyzing game screenshots directly in the browser tab. The vision system doesn't need a server.

4. **Pattern Matching on Device** — Small classification models can detect thought patterns (repetitive, breakthrough, stuck) in real-time, updating the viewer UI without server calls.

5. **Privacy-First Mode** — A fully local thought viewer: local model, local embeddings, local vision, local journal. Nothing leaves the device. Ideal for demos, sensitive content, offline use.

### Replaces or Complements?

**Can replace:**
- Ollama server (for the Local Thinker, with Llama 1B or Granite 2B on WebGPU)
- Server-side embedding service (bge-m3 runs fine in browser)
- Server-side classification (sentiment, novelty scoring)

**Cannot replace:**
- The Conductor (needs GLM-5.2 / Claude Opus — too large for browser)
- Heavy vision models (full YOLOv8-large, SAM, etc.)
- Training/fine-tuning (inference only, no training in browser)

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| Browser-native Local Thinker | 🔴 Large (1-2 weeks) | Model loading, WebGPU detection, fallback chain |
| In-browser embeddings | 🟡 Medium (3-5 days) | Transformers.js pipeline, IndexedDB caching |
| Client-side sentiment/novelty | 🟢 Small (1-2 days) | Pre-trained model, pipeline API |
| Browser vision system (YOLO) | 🔴 Large (1-2 weeks) | Model conversion, video frame pipeline |

### Production Readiness

- **WebGPU**: ✅ Production-ready (Chrome, Edge, Safari). Firefox still partial.
- **WebNN**: 🟡 Behind flags / origin trial. Not yet stable across browsers.
- **Transformers.js**: ✅ Production-ready (v4.2, used by major products).
- **ONNX Runtime Web**: ✅ Production-ready.
- **Model availability**: Growing. Llama 3.2, Granite, Phi-3, Qwen, and hundreds more have ONNX conversions on Hugging Face.
- **Performance**: Depends heavily on GPU. Discrete GPUs match or beat CPU inference. Integrated GPUs are slower but usable. Fallback to WASM is ~3-5x slower.

---

## 3. Chrome Extensions API

### What it is

Chrome Extensions (Manifest V3) provide deep integration with the browser through 50+ APIs. An extension can access:

| API | What It Provides | Relevance |
|-----|-----------------|-----------|
| `chrome.tabs` | Query tabs, read URL/title/favIcon, capture visible tab screenshot, detect language, send messages to content scripts | **Game state monitoring** — watch the Roblox tab, capture screenshots for vision |
| `chrome.scripting` | Inject content scripts, execute CSS/JS on pages | **DOM analysis** — read game UI state from the Roblox page |
| `chrome.sidePanel` | Persistent side panel UI alongside browsing | **Thought stream viewer** — the killer feature (see §4) |
| `chrome.omnibox` | Register keyword in address bar | **Quick commands** — type "slackwater summarize" to get a thought summary |
| `chrome.notifications` | Rich system notifications (basic, image, list, progress) | **Conductor alerts** — "Thought pattern shifted", "Breakthrough detected" |
| `chrome.bookmarks` | Read/create/organize bookmarks | Save interesting thought moments |
| `chrome.history` | Search browsing history | Context for what the user was doing |
| `chrome.clipboard` | Read/write clipboard (write only; read requires user gesture) | Copy thoughts, share insights |
| `chrome.contextMenus` | Right-click menu items | "Analyze this thought", "Send to Conductor" |
| `chrome.storage` | Extension storage (local + sync) | Thought journal persistence synced across devices |
| `chrome.alarms` | Scheduled code execution | Periodic Conductor check-ins |
| `chrome.idle` | Detect user idle/active state | Pause thinker when user is away |
| `chrome.identity` | OAuth2 authentication | User identity for multi-device sync |
| `chrome.offscreen` | Offscreen documents for DOM processing without visible page | Background thought processing |
| `chrome.commands` | Keyboard shortcuts | Quick toggle for side panel, "new thought" trigger |
| `chrome.action` | Toolbar icon with badge, popup | Status indicator (thought count, current mood) |
| `chrome.webRequest` | Intercept/observe network requests | Monitor game API calls for state |
| `chrome.debugger` | Chrome DevTools Protocol access | Deep page inspection (development only) |
| `chrome.dns` | DNS resolution | Network diagnostics |
| `chrome.system.cpu` | CPU info | Check if local model can run |
| `chrome.system.memory` | RAM info | Same |
| `chrome.system.display` | Display info | Multi-monitor awareness |
| `chrome.gcm` | Google Cloud Messaging | Push notifications from server |
| `chrome.tts` / `chrome.ttsEngine` | Text-to-speech | **Voice for thoughts** — narrate the stream |

### How It Enhances the Cognition Architecture

A Chrome extension is the **ideal host** for the thought-stream viewer because:

1. **It lives alongside the game** — The side panel stays open while the user plays Roblox. No window-switching.
2. **It can read the page** — Content scripts can inspect the Roblox game DOM for state data (health, position, inventory) without a separate API.
3. **It can capture screenshots** — `chrome.tabs.captureVisibleTab()` feeds the vision system.
4. **It has the omnibox** — Type "sw think about the dock" in the address bar to inject a thought.
5. **It gets notifications** — The Conductor's commentary can appear as native notifications.
6. **It can use the built-in AI APIs** — Extensions have full access to `LanguageModel`, `Summarizer`, `Writer`, etc., plus extra features (temperature/topK control).
7. **It persists** — `chrome.storage.sync` keeps the thought journal across devices.
8. **It has keyboard shortcuts** — Quick-capture a thought, toggle the panel, trigger analysis.

### Replaces or Complements?

**Replaces**: The need for a separate web app. The extension IS the viewer.

**Complements**: The server-side Conductor (still runs server-side), the game itself (still Roblox).

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| Basic side panel extension shell | 🟢 Small (1 day) | Manifest V3 + sidePanel + basic HTML |
| Thought stream display | 🟢 Small (1-2 days) | WebSocket or SSE to thought journal |
| Tab monitoring + screenshot capture | 🟡 Medium (2-3 days) | Content scripts, captureVisibleTab |
| Omnibox integration | 🟢 Small (1 day) | Register keyword, handle events |
| Notifications | 🟢 Small (half day) | chrome.notifications.create() |
| Built-in AI integration | 🟡 Medium (2-3 days) | Feature detection + Prompt API |
| Full extension with all features | 🟡 Medium (1-2 weeks) | Polish, fallbacks, MV3 compliance |

### Production Readiness

✅ Fully production-ready. Manifest V3 is the standard. Chrome Web Store publishing is well-documented. Firefox and Safari have partial extension API compatibility (WebExtensions).

---

## 4. Chrome Side Panel API

### What it is

`chrome.sidePanel` (Chrome 114+, MV3) provides a persistent panel alongside the browser's main content. Key capabilities:

- **Persistent across navigation** — stays open when user switches tabs (if configured globally)
- **Tab-specific panels** — different panel content per tab via `setOptions({ tabId, path })`
- **Toolbar icon toggle** — `setPanelBehavior({ openPanelOnActionClick: true })`
- **Programmatic open** — `sidePanel.open({ windowId })` on user gesture
- **Multiple panels** — switch between different HTML pages
- **Full Chrome API access** — as an extension page, side panels can use all extension APIs
- **User can pin** — stays visible even when Chrome's built-in panels are shown

```javascript
// Global side panel — same content everywhere
chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });

// Tab-specific — only show thought viewer on Roblox
chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {
  if (tab.url?.includes('roblox.com')) {
    await chrome.sidePanel.setOptions({
      tabId, path: 'thought-viewer.html', enabled: true
    });
  }
});
```

### How It Enhances the Cognition Architecture

This is the **perfect home for the thought-stream viewer**:

1. **Always-visible while playing** — User plays Roblox in the main tab, thought stream scrolls in the side panel. Zero context switching.
2. **Live updates** — WebSocket/SSE connection streams thoughts in real-time as they're generated.
3. **Conductor commentary inline** — When the Conductor annotates a thought, it appears inline in the panel.
4. **Interactive controls** — Sliders for temperature, buttons to "nudge" the thinker, a "summarize" button (uses built-in Summarizer API).
5. **Tab-aware** — Only appears on Roblox tabs, or appears everywhere with different content.
6. **Resizable** — User adjusts panel width based on how much thought detail they want.

### Replaces or Complements?

**Replaces**: The need for a separate browser window or web app for the viewer.

### Build Effort

🟢 **Small** (1-2 days for basic panel, 1 week for full-featured viewer)

The side panel is just an HTML page with full extension API access. Build it with:
- CodeMirror 6 for the thought display (as recommended in THOUGHT_VIEWER_RESEARCH.md)
- WebSocket connection to the thought journal server
- Built-in AI APIs for summarization/analysis
- chrome.storage for persistence

### Production Readiness

✅ Production-ready. Chrome 114+, stable API. Used by many production extensions.

---

## 5. Web Audio API

### What it is

The Web Audio API is a comprehensive system for real-time audio processing in the browser. It provides:

- **AudioContext** — the processing graph
- **Sources** — oscillators, audio buffers, media streams, media elements
- **Effects** — BiquadFilter, Convolver, Delay, DynamicsCompressor, WaveShaper
- **Spatial audio** — PannerNode, AudioListener for 3D positioning
- **Analysis** — AnalyserNode for real-time frequency/time-domain data (FFT)
- **Synthesis** — OscillatorNode for generating tones, AudioBufferSourceNode for samples
- **MediaStream** — microphone input via `getUserMedia()`
- **Offline processing** — OfflineAudioContext for non-real-time rendering
- **Worklets** — AudioWorklet for custom DSP in a dedicated audio thread

### How It Enhances the Cognition Architecture

1. **Voice Input for Thoughts** — `getUserMedia()` → AnalyserNode → Whisper model (via Transformers.js) gives voice-to-thought input. User speaks, viewer transcribes and injects as a thought.

2. **Ambient Sound Generation** — Generate procedural ambient audio that reflects the thought stream's emotional register:
   - Calm thoughts → slow pad drones (OscillatorNode + low-pass filter + reverb)
   - Curious thoughts → gentle arpeggios
   - Excited thoughts → faster tempo, brighter harmonics
   - This creates a **sonification of cognition** — you can hear the AI thinking.

3. **T-minus / MIDI Temporal Encoding Playback** — The cognition architecture encodes events as MIDI-like temporal patterns. Web Audio can literally play these patterns as audio — a "thought rhythm" that makes patterns audible and recognizable.

4. **Real-Time Audio Analysis** — If the game has audio (Roblox does), AnalyserNode can detect audio events (explosions, music changes, speech) and feed them as observations to the thinker.

5. **Text-to-Speech for Thoughts** — Narrate the thought stream using the Web Speech API (`speechSynthesis`) or Chrome's TTS extension API. "Audible thinking."

### Replaces or Complements?

**Complements** — Web Audio adds a new modality (audio) to the existing architecture. Doesn't replace any server-side component.

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| Basic ambient sonification | 🟡 Medium (3-5 days) | Map thought fields → synth params |
| Voice input → transcription | 🟡 Medium (3-5 days) | getUserMedia + Whisper via Transformers.js |
| T-minus pattern playback | 🟢 Small (2-3 days) | Scheduler + OscillatorNode |
| TTS narration | 🟢 Small (1 day) | speechSynthesis API or chrome.tts |
| Real-time audio analysis | 🟢 Small (1-2 days) | AnalyserNode + event detection |

### Production Readiness

✅ Production-ready. Web Audio API is stable in all modern browsers. AudioWorklet is stable. `getUserMedia()` requires HTTPS and user permission.

---

## 6. WebSocket / Server-Sent Events

### What They Are

**WebSocket** provides full-duplex, bidirectional communication over a single persistent TCP connection. The browser opens a connection to the server, and both sides can send messages at any time. Low latency (~1-10ms per message after handshake).

**Server-Sent Events (SSE)** provide one-directional (server → client) streaming over HTTP. Simpler than WebSocket, uses standard HTTP, auto-reconnects on disconnect. The `EventSource` API is minimal:

```javascript
const source = new EventSource('/thought-stream');
source.onmessage = (e) => {
  const thought = JSON.parse(e.data);
  displayThought(thought);
};
```

**WebTransport** (emerging) provides UDP-based, multiplexed, low-latency communication with backpressure support. Currently Chrome-only (uses HTTP/3). May eventually replace WebSocket for many use cases.

#### Comparison to File-Watcher Approach

The current architecture uses JSONL files + a file watcher. Here's how WebSocket/SSE compares:

| Aspect | File Watcher (current) | WebSocket | SSE |
|--------|----------------------|-----------|-----|
| Latency | 100-500ms (polling interval) | 1-10ms | 10-50ms |
| Direction | One-way (file → watcher) | Bidirectional | Server → client only |
| Browser support | N/A (server-side) | Universal | Universal |
| Reconnection | Manual | Manual | Automatic (built-in) |
| Complexity | Low (just file I/O) | Medium (server + client) | Low (HTTP endpoint) |
| Multiplexing | One file per stream | Multiple channels | One stream per connection |
| Backpressure | N/A | No (buffer fills) | No |
| Binary data | Via file | ✅ Yes | Text only |
| Best for | Local development | Real-time games, chat | Live updates, feeds |

### How They Enhance the Cognition Architecture

1. **Live Thought Streaming** — SSE is perfect for streaming thoughts from the server (where the Local Thinker runs) to the browser (where the viewer lives). Near-zero latency, automatic reconnection, trivial server implementation.

2. **Bidirectional Control** — WebSocket lets the viewer send commands back: "increase temperature", "inject this thought", "switch to exploration mode". The Conductor can receive viewer input in real-time.

3. **Multi-Client Sync** — WebSocket enables multiple viewers (dev machine + phone + second monitor) all seeing the same thought stream simultaneously.

4. **Replace the File Watcher** — The current architecture writes thoughts to JSONL and uses a file watcher. A WebSocket/SSE server that reads the same JSONL file (or receives thoughts directly from the thinker) and streams them to browsers is cleaner and lower-latency.

### Replaces or Complements?

**Replaces** the file-watcher pattern for the viewer connection. The JSONL journal still exists for persistence and training, but the viewer gets real-time streaming instead of file polling.

**Complements** the existing architecture — the thinker still writes to JSONL; an SSE endpoint just tails that file and streams it.

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| SSE endpoint (Node.js/Worker) | 🟢 Small (half day) | `res.writeHead(200, {'Content-Type': 'text/event-stream'})` + tail JSONL |
| WebSocket server | 🟡 Medium (1-2 days) | `ws` library or Cloudflare Durable Object |
| Client-side SSE consumer | 🟢 Small (1 hour) | EventSource API, 10 lines |
| Client-side WebSocket consumer | 🟢 Small (2 hours) | WebSocket API + reconnection logic |
| Full real-time layer | 🟡 Medium (2-3 days) | Server + client + error handling + backpressure |

### Production Readiness

✅ Both WebSocket and SSE are universally supported, stable, production-ready. The choice is architectural: SSE for thought streaming (simpler), WebSocket if the viewer needs to send commands back.

**Recommendation for Slackwater:** Use SSE for thought streaming (server → viewer) + HTTP POST for viewer commands (viewer → server). Simpler than WebSocket, sufficient for the use case.

---

## 7. IndexedDB / OPFS

### What it is

**IndexedDB** is a transactional, object-oriented database built into every modern browser. It stores structured data (objects, files, blobs) indexed by key. Available in Web Workers. Same-origin policy enforced.

- **Capacity**: Typically several hundred MB to multiple GB per origin (browser-eviction policies apply; persistent storage can be requested)
- **Performance**: Asynchronous I/O, good for bulk reads/writes, index-based queries
- **Transactions**: All operations occur within transactions
- **Object stores**: Like tables but schema-flexible

**OPFS (Origin Private File System)** is part of the File System API. It provides:
- A private, origin-scoped file system not visible to the user
- **Synchronous file access** via `FileSystemSyncAccessHandle` (in Web Workers only)
- **High-performance in-place writes** — designed for large files, WASM memory, game assets
- Ideal for: model weights, thought journal databases, audio/video files

```javascript
// IndexedDB — store thoughts
const db = await idb.openDB('slackwater', 1, {
  upgrade(db) {
    const store = db.createObjectStore('thoughts', { keyPath: 'timestamp' });
    store.createIndex('beat', 'beat');
    store.createIndex('action', 'lean.action');
    store.createIndex('quality', 'quality_signals.novelty');
  }
});
await db.add('thoughts', thought);

// OPFS — store model weights or large blobs
const root = await navigator.storage.getDirectory();
const modelDir = await root.getDirectoryHandle('models', { create: true });
const fileHandle = await modelDir.getFileHandle('granite-2b.q4.onnx', { create: true });
const writable = await fileHandle.createWritable();
await writable.write(modelArrayBuffer);
await writable.close();
```

### How It Enhances the Cognition Architecture

1. **The Journal Lives in the Browser** — The entire thought journal can be stored in IndexedDB: every thought, game state snapshot, Conductor commentary, quality metric. Queryable by beat, action type, novelty score. No server needed for the viewer.

2. **Model Caching in OPFS** — If running browser-native models (Transformers.js), model weights (~700MB-2GB) are cached in OPFS. First load downloads from CDN; subsequent loads are instant from local storage.

3. **Offline-First Viewer** — With thoughts in IndexedDB and models in OPFS, the viewer works completely offline. Open Chrome, read thoughts, run analysis — no server.

4. **Historical Replay** — Query IndexedDB for thoughts from a specific time range, beat sequence, or quality range. Replay any moment in the cognition loop.

5. **Training Data Accumulation** — The viewer accumulates thought-action-quality triples in IndexedDB, which can be exported for model fine-tuning.

### Replaces or Complements?

**Can replace**: Server-side JSONL files for the viewer's working copy. The server still maintains its own journal.

**Complements**: The server-side Vectorize index — the browser can hold a local copy of recent embeddings for fast semantic search.

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| IndexedDB thought store | 🟢 Small (1-2 days) | Use `idb` library for ergonomic API |
| OPFS model caching | 🟢 Small (1 day) | Transformers.js handles this internally |
| Historical query/replay UI | 🟡 Medium (3-5 days) | Date pickers, timeline scrubbing, filtering |
| Export for training | 🟢 Small (1 day) | Serialize IndexedDB → JSONL/CSV |

### Production Readiness

✅ Both fully production-ready. IndexedDB is universally supported. OPFS is supported in Chrome, Edge, Firefox, Safari (2023+). `idb` library makes IndexedDB ergonomic.

---

## 8. Web Workers / SharedArrayBuffer

### What it is

**Web Workers** run JavaScript in background threads, independent of the main UI thread.

| Worker Type | Scope | Use Case |
|-------------|-------|----------|
| **Dedicated Worker** | Single page | Heavy computation for one tab |
| **Shared Worker** | Multiple pages (same origin) | Shared state, single WebSocket connection |
| **Service Worker** | Network proxy, offline | PWA backbone, push notifications, background sync |

Workers communicate via `postMessage()` (structured clone, not shared memory by default). They can use `fetch()`, IndexedDB, and most Web APIs, but **cannot access the DOM**.

**SharedArrayBuffer** enables true shared memory between threads. Requires cross-origin isolation (`COOP: same-origin`, `COEP: require-corp` headers). Enables:
- Zero-copy data transfer between main thread and workers
- Atomic operations (Atomics API)
- True multi-threaded computation

**Atomics.wait()/notify()** — allows workers to wait for conditions and be notified, enabling efficient producer-consumer patterns.

```javascript
// Main thread — spawn a thought analysis worker
const worker = new Worker('thought-analyzer.js');

// SharedArrayBuffer for zero-copy thought data
const buffer = new SharedArrayBuffer(1024 * 1024); // 1MB
const view = new Float32Array(buffer);

worker.postMessage({ type: 'init', buffer });
// Later:
view[0] = noveltyScore;
Atomics.notify(view, 0); // Wake the worker
```

### How It Enhances the Cognition Architecture

1. **Reflex Matcher in a Worker** — The reflex/pattern matcher (detecting repetition, novelty, emotional shifts) runs in a dedicated worker, never blocking the UI thread. Thoughts stream in via postMessage; analysis results stream out.

2. **Local Thinker in a Worker** — If running the thinker via Transformers.js, inference happens in a worker. The main thread handles only UI updates.

3. **SharedArrayBuffer for Vision Pipeline** — If YOLO runs on screenshots, the pixel data can be shared between the capture thread and the inference thread with zero copying.

4. **Service Worker for Background Sync** — When the browser is offline, the service worker queues thought data. When connectivity returns, it syncs to the server automatically.

5. **WebSocket in a Shared Worker** — A single WebSocket connection shared across all open tabs/panels. One connection, many viewers.

### Replaces or Complements?

**Complements** — Workers are an implementation detail of the client. They make everything smoother but don't change the architecture.

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| Thought analysis worker | 🟢 Small (1-2 days) | Dedicated worker + postMessage |
| Transformers.js in worker | 🟡 Medium (2-3 days) | Model loading + inference in worker context |
| SharedArrayBuffer pipeline | 🔴 Large (1 week) | Cross-origin isolation setup + buffer management |
| Service worker for offline | 🟡 Medium (3-5 days) | Cache strategy + background sync |

### Production Readiness

- **Web Workers**: ✅ Universal, stable.
- **SharedArrayBuffer**: ✅ Supported but requires cross-origin isolation headers (COOP/COEP). This can break third-party resources. Works well for first-party apps.
- **Service Workers**: ✅ Universal, stable. Core PWA technology.

---

## 9. Canvas / WebGL / WebGPU Compute

### What it is

The browser provides three tiers of GPU access:

| API | Generation | Focus | Compute Shaders | ML Support |
|-----|-----------|-------|-----------------|------------|
| **Canvas 2D** | Basic | 2D drawing | ❌ | ❌ |
| **WebGL 1/2** | 2011/2017 | Graphics (OpenGL ES 2.0/3.0) | ✅ (via transform feedback) | Limited (via textures/shaders) |
| **WebGPU** | 2023+ | Graphics + Compute | ✅ First-class | ✅ Native compute shaders |

**WebGPU Compute Shaders** allow general-purpose GPU computation:
- Read/write storage buffers
- Workgroups and dispatch
- Atomic operations
- Perfect for matrix multiplication, convolutions, attention — the core ops of neural networks

**TensorFlow.js** and **ONNX Runtime Web** both use WebGPU compute shaders under the hood when `device: 'webgpu'` is specified.

### How It Enhances the Cognition Architecture

1. **Client-Side Vision Models** — Run YOLOv8-nano or similar object detection on game screenshots directly in the browser using WebGPU. The vision system that feeds the Local Thinker can be entirely client-side.

2. **GPU-Accelerated Embeddings** — Run bge-m3 or similar embedding models on the GPU for instant semantic search over the thought journal.

3. **Custom Compute Kernels** — Write WebGPU compute shaders for the reflex matcher's pattern detection algorithms. Spatial/temporal pattern matching on the GPU could analyze hundreds of thoughts in parallel.

4. **Visualization** — WebGL/WebGPU can render beautiful thought-relationship graphs, temporal patterns, or 3D cognitive maps. A "thought constellation" visualization.

5. **Real-Time Image Classification** — Classify game screenshots (indoor/outdoor, day/night, building/nature) to enrich the game state without server calls.

### Replaces or Complements?

**Can replace**: Server-side vision system (YOLO runs fine on WebGPU in browser).

**Complements**: The Local Thinker (which could also run on WebGPU via Transformers.js).

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| YOLOv8 in browser (via Transformers.js) | 🟡 Medium (3-5 days) | Model loading + video frame capture + inference |
| Custom WebGPU compute kernel | 🔴 Large (1-2 weeks) | WGSL shader expertise needed |
| Thought constellation visualization | 🔴 Large (1-2 weeks) | Three.js + WebGL + force-directed graph |
| Image classification pipeline | 🟡 Medium (3-5 days) | Transformers.js pipeline |

### Production Readiness

- **Canvas 2D**: ✅ Universal, stable.
- **WebGL 1/2**: ✅ Universal, stable. Used by TensorFlow.js WebGL backend.
- **WebGPU**: ✅ Production-ready in Chrome, Edge, Safari 17.4+. Firefox partial. Compute shaders stable.
- **Model availability**: YOLOv8-nano, ResNet, MobileNet, and many more have WebGPU-compatible ONNX versions.

---

## 10. WebRTC

### What it is

WebRTC (Web Real-Time Communication) enables peer-to-peer audio, video, and data communication between browsers without requiring data to pass through a server (though a signaling server is needed for connection setup).

Key components:
- **RTCPeerConnection** — represents a connection between two peers
- **MediaStream** — audio/video tracks (camera, microphone, screen share)
- **RTCDataChannel** — bidirectional arbitrary data transfer between peers (SCTP over DTLS)
- **STUN/TURN servers** — NAT traversal infrastructure (Google provides free STUN)

Data channels support:
- Reliable/ordered mode (like TCP) or unreliable/unordered (like UDP)
- Transfer of strings, ArrayBuffers, Blobs
- Sub-millisecond latency for local connections
- Configurable bandwidth management

### How It Enhances the Cognition Architecture

1. **Shared Thought Viewing** — Multiple people can view the same thought stream in real-time via WebRTC data channels. Imagine: developer on desktop, reviewer on phone, both watching the Local Thinker's stream. The server sends thoughts to one peer, which meshes to others.

2. **Low-Latency Thought Sharing** — For collaborative analysis: one user's annotations/insights about the thought stream are shared to all viewers instantly via data channels.

3. **Voice/Video Commentary** — Viewers can discuss the thought stream with voice/video via WebRTC media streams. A "watch party" for AI cognition.

4. **Screen Sharing Integration** — Share the game view (Roblox) alongside the thought stream for remote demos or collaborative debugging.

5. **Distributed Thinking** — (Speculative) Multiple browser instances could split the cognitive workload — one runs vision, another runs embeddings, results shared via data channels.

### Replaces or Complements?

**Complements** — WebRTC adds multi-user/collaborative capabilities. The core cognition loop is single-node. WebRTC is for when you want to share it.

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| Basic data channel thought sharing | 🟡 Medium (3-5 days) | Signaling server + RTCPeerConnection |
| Multi-peer mesh | 🔴 Large (1-2 weeks) | Mesh or star topology, peer management |
| Voice/video watch party | 🔴 Large (2-3 weeks) | Media stream management, UI |
| Screen share for demos | 🟡 Medium (3-5 days) | `getDisplayMedia()` |

### Production Readiness

✅ Fully production-ready. WebRTC is used by Google Meet, Discord, Zoom web client. `RTCDataChannel` is universally supported. STUN servers are freely available. For production, you'll want your own TURN server for users behind strict NATs.

---

## 11. Progressive Web App (PWA)

### What it is

A PWA is a web application that uses Service Workers, a Web App Manifest, and modern web APIs to provide an app-like experience:

- **Installable** — "Add to Home Screen" on mobile, "Install" in desktop Chrome. Gets its own window, icon, launches without browser chrome.
- **Offline-first** — Service Worker caches assets and data. App works without network.
- **Push Notifications** — Server sends push notifications via the Push API + service worker, even when the app isn't open.
- **Background Sync** — Service worker queues actions when offline, syncs when online.
- **App-like UX** — No browser address bar, standalone display mode, splash screen.
- **Share Target** — Register as a share target in the OS share sheet.
- **File Handling** — Register as a handler for specific file types.

```json
// manifest.json
{
  "name": "Slackwater Thought Viewer",
  "short_name": "Thoughts",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0a0a",
  "theme_color": "#6366f1",
  "icons": [/* ... */],
  "shortcuts": [
    {
      "name": "Live Stream",
      "url": "/?view=live"
    },
    {
      "name": "Journal",
      "url": "/?view=journal"
    }
  ]
}
```

### How It Enhances the Cognition Architecture

1. **Installable Thought Viewer** — User installs the viewer on their phone/desktop. Opens it like an app. Full-screen thought stream, no browser distractions.

2. **Push Notifications from the Conductor** — When the Conductor detects a breakthrough, pattern shift, or anomaly, it sends a push notification to the installed PWA. User gets alerted even if the viewer isn't open.

3. **Offline Journal Access** — Service worker caches recent thoughts. User can browse the journal on a plane, on commute, anywhere.

4. **Background Sync** — If the viewer captures user annotations or configuration changes while offline, they sync to the server when connectivity returns.

5. **Home Screen Shortcut** — Quick access. "Live Stream" and "Journal" shortcuts go directly to the right view.

### Replaces or Complements?

**Complements** — The PWA is the deployment/distribution mechanism for the viewer. It works alongside the Chrome extension (extension for desktop browsing, PWA for mobile/standalone).

### Build Effort

| Feature | Effort | Notes |
|---------|--------|-------|
| Basic PWA (manifest + service worker) | 🟢 Small (1 day) | Web App Manifest + minimal service worker |
| Offline caching strategy | 🟡 Medium (2-3 days) | Cache API + IndexedDB + fallback chain |
| Push notifications | 🟡 Medium (2-3 days) | Push API + VAPID keys + server push service |
| Background sync | 🟢 Small (1-2 days) | Service Worker `sync` event |
| Install prompts + shortcuts | 🟢 Small (half day) | `beforeinstallprompt` event |

### Production Readiness

✅ Fully production-ready. PWAs are supported by Chrome, Edge, Safari (partial — no push on iOS Safari until iOS 16.4+, now supported), Firefox. Service Workers are universal. Push API works on desktop and Android. iOS support arrived in 16.4+.

---

## 12. Omnibox API

### What it is

`chrome.omnibox` lets a Chrome Extension register a keyword with the address bar. When the user types the keyword followed by a space, the browser enters "extension mode" — every keystroke is sent to the extension, and the extension can provide suggestions.

Features:
- Register a keyword (e.g., `"sw"` for Slackwater)
- `onInputStarted` — user typed the keyword
- `onInputChanged` — user is typing; extension provides suggestions
- `onInputEntered` — user accepted input; extension takes action
- `onInputCancelled` — user pressed Escape
- Suggestions support rich formatting (URL, match, dim styles)
- Default suggestion with `setDefaultSuggestion()`
- Can open in current tab, new foreground tab, or new background tab

```javascript
// Register keyword
{ "omnibox": { "keyword": "sw" } }

// Handle input
chrome.omnibox.onInputChanged.addListener((text, suggest) => {
  suggest([
    { content: 'sw summarize', description: '<match>summarize</match> — Summarize recent thoughts' },
    { content: 'sw mood', description: '<match>mood</match> — Show current thought mood' },
    { content: 'sw nudge explore', description: '<match>nudge</match> explore — Push thinker toward exploration' },
  ]);
});

chrome.omnibox.onInputEntered.addListener((text) => {
  if (text === 'summarize') runSummarizer();
  if (text.startsWith('nudge')) injectNudge(text);
});
```

### How It Enhances the Cognition Architecture

1. **Quick Commands Without Switching Tabs** — User types `sw summarize` in the address bar to get a summary of recent thoughts. `sw mood` shows the current emotional register. `sw nudge explore` pushes the thinker toward exploration.

2. **Thought Search from Address Bar** — `sw dock` searches the thought journal for thoughts about "dock" and shows results as suggestions.

3. **Frictionless Interaction** — The omnibox is always one keystroke away (Ctrl+L). No need to switch to the side panel or open the extension popup.

### Replaces or Complements?

**Complements** — Omnibox is a quick-access entry point. It works alongside the side panel (which is the main viewer).

### Build Effort

🟢 **Small** (half day to 1 day). Register keyword, handle events, wire to existing functions.

### Production Readiness

✅ Production-ready. Stable since Chrome 9+. Universal.

---

## 13. Synthesis: Architecture Integration Map

### The Full Browser-Native Thought Viewer Stack

Here's how all 12 capabilities combine into a single coherent system:

```
┌──────────────────────────────────────────────────────────────────┐
│                    CHROME EXTENSION (MV3)                        │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │  OMNIBOX    │  │  SIDE PANEL  │  │   NOTIFICATIONS         │ │
│  │  (sw cmd)   │  │  (Viewer UI) │  │   (Conductor alerts)    │ │
│  └──────┬──────┘  └──────┬───────┘  └────────────┬────────────┘ │
│         │                │                        │              │
│         └────────────────┼────────────────────────┘              │
│                          ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                  SERVICE WORKER                           │   │
│  │  • SSE connection to thought server                      │   │
│  │  • Push notifications (Push API)                         │   │
│  │  • Background sync                                       │   │
│  │  • Offline caching                                       │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              WORKERS (background threads)                │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │   │
│  │  │ Thinker     │  │ Pattern      │  │ Vision (YOLO)  │  │   │
│  │  │ (Trans.js   │  │ Matcher      │  │ (Trans.js +    │  │   │
│  │  │  + WebGPU)  │  │ (reflexes)   │  │  WebGPU)       │  │   │
│  │  │             │  │              │  │                │  │   │
│  │  │ Granite 2B  │  │ Novelty,     │  │ Screenshot →   │  │   │
│  │  │ or Llama 1B │  │ repetition,  │  │ Object detect  │  │   │
│  │  │ via ONNX    │  │ shift detect │  │ via ONNX       │  │   │
│  │  └─────────────┘  └──────────────┘  └────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              BUILT-IN AI (Gemini Nano)                   │   │
│  │  • Summarizer API → "what just happened" banner         │   │
│  │  • Prompt API → quality scoring, thought classification │   │
│  │  • Writer API → interactive thought rewriting           │   │
│  │  • Translator API → multi-language viewer               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              PERSISTENCE                                 │   │
│  │  • IndexedDB → thought journal (queryable)              │   │
│  │  • OPFS → model weights, large blobs                    │   │
│  │  • chrome.storage.sync → user prefs, device sync        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              AUDIO                                      │   │
│  │  • Web Audio API → ambient sonification of thoughts     │   │
│  │  • getUserMedia → voice input → Whisper transcription   │   │
│  │  • speechSynthesis → TTS narration of thought stream    │   │
│  │  • T-minus MIDI playback → cognitive rhythm             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              GPU (WebGPU)                               │   │
│  │  • Compute shaders for pattern matching                 │   │
│  │  • Model inference (Transformers.js backend)            │   │
│  │  • Visualization (thought constellation)                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
                          │                    ▲
                          │ SSE (thoughts)     │ HTTP POST (commands)
                          ▼                    │
┌──────────────────────────────────────────────────────────────────┐
│                    SERVER (Cloudflare Worker / Node)             │
│                                                                  │
│  • Local Thinker (GLM-5.2 / Granite via Ollama)                 │
│  • Conductor (GLM-5.2 / Claude Opus — deep reasoning)           │
│  • Game state API (Roblox relay)                                 │
│  • JSONL journal persistence                                      │
│  • Vectorize embeddings (bge-m3)                                 │
└──────────────────────────────────────────────────────────────────┘
                          │                    ▲
                          │ WebSocket          │ Game state
                          ▼                    │
┌──────────────────────────────────────────────────────────────────┐
│                    GAME (Roblox / Slackwater)                    │
└──────────────────────────────────────────────────────────────────┘
```

### Phased Build Plan

#### Phase 1: Core Viewer (1-2 weeks)
**Goal:** Live thought stream visible in browser

| Component | Tech | Effort |
|-----------|------|--------|
| Side Panel Extension | `chrome.sidePanel` + HTML/JS | 2 days |
| SSE endpoint | Cloudflare Worker or Node server | 1 day |
| Thought display | CodeMirror 6 (as per THOUGHT_VIEWER_RESEARCH.md) | 2 days |
| IndexedDB journal | `idb` library | 2 days |
| Basic controls | Temperature slider, pause/play | 1 day |
| Notifications | `chrome.notifications` | half day |

#### Phase 2: Browser-Native Intelligence (2-3 weeks)
**Goal:** In-browser AI features that reduce server dependency

| Component | Tech | Effort |
|-----------|------|--------|
| Summarizer banner | `Summarizer` API (Chrome 138+) | 2 days |
| Quality scoring | `LanguageModel` (Prompt API) | 3 days |
| Omnibox commands | `chrome.omnibox` | 1 day |
| Pattern matcher worker | Dedicated Web Worker | 3 days |
| Embeddings in browser | Transformers.js + bge-m3 + WebGPU | 3 days |
| PWA + offline | Service Worker + manifest | 2 days |

#### Phase 3: Full Browser-Native Cognition (4-6 weeks)
**Goal:** The thinker itself runs in the browser

| Component | Tech | Effort |
|-----------|------|--------|
| Local Thinker in browser | Transformers.js + Granite 2B + WebGPU | 2 weeks |
| Vision system (YOLO) | Transformers.js + screenshot capture | 1 week |
| Ambient sonification | Web Audio API + synthesis | 1 week |
| Voice input | getUserMedia + Whisper | 3 days |
| Push notifications | Push API + VAPID | 3 days |
| Multi-viewer (WebRTC) | RTCDataChannel thought sharing | 1 week |

#### Phase 4: Polish & Distribution (2-3 weeks)
**Goal:** Production-quality, installable, shareable

| Component | Tech | Effort |
|-----------|------|--------|
| Thought constellation viz | Three.js + WebGPU | 2 weeks |
| Interactive thought rewriting | Writer API + CodeMirror ghost text | 3 days |
| PWA install flow | `beforeinstallprompt` + shortcuts | 1 day |
| Chrome Web Store publish | MV3 review process | 3 days |
| Fallback chain | Server-side API when built-in AI unavailable | 3 days |

### Priority Recommendations

**Build first (highest impact, lowest effort):**
1. 🥇 **Side Panel Extension + SSE** — The viewer exists. Live thoughts stream into a persistent panel.
2. 🥈 **Built-in Summarizer API** — Zero-cost, zero-latency summaries in the viewer header.
3. 🥉 **IndexedDB journal** — Thoughts persist in the browser. Historical browsing.
4. 🏅 **Omnibox commands** — Quick keyboard-driven interaction.

**Build second (medium impact, medium effort):**
5. **Pattern matcher worker** — Real-time novelty/repetition detection in the browser.
6. **Quality scoring via Prompt API** — The Conductor's scoring step, client-side.
7. **PWA + push notifications** — Installable, alerts on breakthroughs.
8. **Ambient sonification** — Hear the thoughts.

**Build later (high impact, high effort):**
9. **Local Thinker in browser** — Full independence from the server.
10. **Vision system** — YOLO in the browser.
11. **Thought constellation** — 3D visualization of thought relationships.
12. **Multi-viewer via WebRTC** — Collaborative thought watching.

### Graceful Degradation Chain

Every browser-native feature needs a fallback for when the hardware/browser doesn't support it:

```
WebGPU model inference
    ↓ (no WebGPU)
WASM model inference (slower)
    ↓ (no Transformers.js support)
Chrome Built-in AI (Gemini Nano)
    ↓ (no built-in AI / insufficient hardware)
Server-side API (GLM-5.2 via Cloudflare Worker)
    ↓ (offline)
IndexedDB cached results + read-only journal
```

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Chrome built-in AI requires high-end hardware | High | Medium | Fallback to server-side APIs |
| WebGPU not available on all devices | Medium | Medium | Fallback to WASM in Transformers.js |
| Extension review delays on Web Store | Low | Low | Load unpacked during development |
| SharedArrayBuffer requires COOP/COEP headers | Medium | Low | Use postMessage instead (minor perf cost) |
| Gemini Nano model quality insufficient | Medium | Medium | Use for classification only, not generation |
| Browser storage eviction | Low | High | Request `navigator.storage.persist()` |

---

## Summary

The browser in 2026 is a capable AI runtime. Chrome's built-in Gemini Nano, WebGPU-powered model inference, and the Chrome Extension platform collectively enable a thought viewer that is:

- **Real-time** — SSE streams thoughts with <50ms latency
- **Intelligent** — Built-in AI summarizes, classifies, and analyzes thoughts client-side
- **Autonomous** — Can run the Local Thinker entirely in-browser via Transformers.js + WebGPU
- **Persistent** — IndexedDB + OPFS store the full journal and model weights locally
- **Ambient** — Side panel stays open while browsing/playing; omnibox gives instant access
- **Installable** — PWA installs on phone/desktop with push notifications
- **Multi-sensory** — Web Audio sonifies thoughts; TTS narrates them; WebGL visualizes them
- **Private** — Everything can run on-device, no data leaves the browser
- **Graceful** — Each capability degrades cleanly to server-side fallbacks

The recommended path is to start with the Side Panel Extension + SSE (Phase 1, 1-2 weeks) and layer in browser-native intelligence from there. The architecture is designed so every capability is additive — each one enhances the viewer without requiring the others.

**Total estimated effort for full vision:** 10-14 weeks (one developer). Core viewer in 1-2 weeks. Production-grade with browser-native AI in 4-6 weeks.