# Thought Viewer Research: Web-Native Resonator IDE

> Research date: 2026-08-03
> Goal: Build a web-native thought editor where Granite 4.1 (thinker) and CodeGeeX (finisher) form a resonator pattern

---

## Table of Contents

1. [Recommended IDE/Editor to Embed](#1-recommended-ideeditor-to-embed)
2. [How CodeGeeX API Integration Works](#2-how-codegeex-api-integration-works)
3. [The Resonator Pattern Design](#3-the-resonator-pattern-design)
4. [Architecture Sketch](#4-architecture-sketch-for-web-native-thought-editor)
5. [What We Can Build TODAY vs What Needs More Research](#5-what-we-can-build-today-vs-what-needs-more-research)
6. [Specific API Endpoints and Auth Flows](#6-specific-api-endpoints-and-auth-flows-for-codegeex)

---

## 1. Recommended IDE/Editor to Embed

### Verdict: **CodeMirror 6** for the inline editor, with **Monaco** as a fallback option

#### Comparison Matrix

| Feature | Monaco Editor | CodeMirror 6 | Ace Editor | contenteditable |
|---------|--------------|--------------|------------|-----------------|
| Bundle size | ~2.5MB+ | **~50KB min** | ~300KB | 0KB (native) |
| Mobile support | ❌ Not supported | ✅ **Excellent** | ✅ Good | ✅ Native |
| Markdown support | ✅ Syntax highlight | ✅ **GFM + live preview** | ✅ Basic | Manual |
| Inline ghost text | ✅ Via API | ✅ **Via decorations** | ✅ Via markers | Hard |
| Embed complexity | Medium (workers) | **Low** | Low | Trivial |
| AI completion UX | ✅ Proven (Copilot) | ✅ Flexible | ✅ Works | Custom build |
| Framework wrappers | `@monaco-editor/react` | `@uiw/react-codemirror` | `react-ace` | N/A |
| Multi-cursor | ✅ | ✅ | ✅ | ❌ |
| Extensibility | VS Code extensions | **Extension system** | Limited | Full custom |

#### Why CodeMirror 6 Wins for This Project

1. **Lightweight** — 50KB vs Monaco's 2.5MB+. Critical for a web viewer that loads fast
2. **Mobile-friendly** — Granite thoughts may be viewed/edited on phones. Monaco explicitly doesn't support mobile
3. **Ghost text decorations** — CodeMirror's decoration API allows inline "ghost text" completions (what CodeGeeX needs). This is how we render AI suggestions as faded inline text
4. **Markdown-native** — `@codemirror/lang-markdown` supports GitHub-flavored Markdown with dynamic code block language loading
5. **Obsidian-style live preview** — Projects like `atomic-editor` and `codemirror-rich-markdoc` prove CodeMirror can do inline rich-text rendering (hide markdown syntax until cursor enters the line)
6. **Tree-shakeable** — Only include what we need, keeping the bundle lean

#### When to Consider Monaco Instead

- If we need full VS Code extension compatibility (we don't for a thought viewer)
- If we want Theia IDE integration (Theia uses Monaco natively)

#### Theia IDE Assessment

Theia is a full IDE framework, not a lightweight embeddable editor. It's better suited if we eventually want to build a **complete cloud IDE** around the resonator concept. Key facts:

- **Architecture**: Dual-process (frontend in browser + backend on Node.js), communicating via JSON-RPC over WebSockets
- **AI-native**: "Theia AI" framework reached stable state in early 2025, offering transparent AI tooling integration
- **VS Code compatible**: Can use VS Code extensions, including CodeGeeX's existing extension
- **Embeddable**: Can run in browser, but it's a full application, not a simple component
- **Overkill for now**: We need an editor component, not a full IDE. Keep Theia in mind for a future "Resonator IDE" product

---

## 2. How CodeGeeX API Integration Works

### CodeGeeX Model Evolution

| Version | Parameters | Context | Key Features |
|---------|-----------|---------|-------------|
| CodeGeeX (v1) | 13B | 2,048 tokens | Multilingual code gen, translation, 20+ languages |
| CodeGeeX2 | ~7B | 8K tokens | Faster, 100+ languages, ChatGLM2-based |
| **CodeGeeX4-ALL-9B** | **9B** | **128K tokens** | Code completion, interpreter, web search, function calling, repo-level QA |

### CodeGeeX4-ALL-9B (Recommended for Resonator)

This is the model we want. Here's why:

- **128K context window** — can hold entire thought streams + code files
- **Under 10B parameters** — runs on consumer GPUs (or via cloud API)
- **OpenAI-compatible API** — when served via vLLM, exposes `/v1/chat/completions` and `/v1/completions`
- **Available on Ollama** — `ollama run codegeex4` for local deployment
- **Apache-2.0 code license** — model weights available for research; commercial use requires registration

### Three Integration Paths

#### Path A: Cloud Service (codegeex.cn)
- CodeGeeX extension connects to `codegeex.cn` backend
- Users authenticate via the extension (login flow)
- API key + secret obtained from the AMiner/Tianqi platform
- **No publicly documented REST API** for third-party apps — the extension uses an internal protocol
- This is the path the VS Code/Jetbrains extensions use

#### Path B: Local/Self-Hosted via Ollama
```bash
# Start CodeGeeX4 locally
export OLLAMA_ORIGINS="*"
ollama run codegeex4
ollama serve  # exposes http://localhost:11434
```
Then point the CodeGeeX extension (or our custom integration) at `http://localhost:11434`. Any OpenAI-compatible client works.

#### Path C: Self-Hosted via vLLM (OpenAI-compatible server)
```bash
python -m vllm.entrypoints.openai.api_server \
  --model THUDM/codegeex4-all-9b \
  --trust_remote_code
```
This exposes standard OpenAI endpoints:
- `POST /v1/chat/completions` — chat mode
- `POST /v1/completions` — raw completion mode

### Infilling (FIM) Format — How Inline Completion Works

CodeGeeX4 uses special tokens for fill-in-the-middle (FIM) completion:

```
<|user|>
###PATH:thoughts.md
###LANGUAGE:Markdown
###MODE:LINE
<|code_suffix|>{text after cursor}
<|code_prefix|>{text before cursor}
<|code_middle|><|assistant|>
```

**Key parameters:**
- `###PATH:` — file path/name (helps model understand context)
- `###LANGUAGE:` — language tag (Markdown, Python, JavaScript, etc.)
- `###MODE:` — `LINE` (single line) or `BLOCK` (multi-line)
- `<|code_prefix|>` — everything before cursor
- `<|code_suffix|>` — everything after cursor
- `<|code_middle|>` — where the model fills in

### Cross-File Infilling (for context-aware completion)

```
<|user|>
###REFERENCE:
###PATH:granite-thoughts.md
{previous thought stream content}
###REFERENCE:
###PATH:project-context.md
{project context}
###PATH:current-note.md
###LANGUAGE:Markdown
###MODE:BLOCK
<|code_suffix|>{after cursor}<|code_prefix|>{before cursor}<|code_middle|><|assistant|>
```

### System Prompt for Chat Mode

```
<|system|>
You are an intelligent programming assistant named CodeGeeX. You will answer any
questions users have about programming, coding, and computers, and provide code
that is formatted correctly, executable, accurate, and secure, and offer detailed
explanations when necessary. Please answer in English.<|user|>
{query}<|assistant|>
```

---

## 3. The Resonator Pattern Design

### Core Concept

Two AI models operate in the same editing surface, creating a feedback loop where each improves the other's output through a Conductor that orchestrates their interaction.

### The Three Actors

```
┌─────────────────────────────────────────────────────────┐
│                    THE CONDUCTOR                         │
│         (Large model — e.g., GLM-5.2, Nemotron)         │
│                                                         │
│  • Watches both streams in real-time                    │
│  • Identifies patterns where they disagree              │
│  · Generates teaching signals                           │
│  • Decides when to intervene vs let them work           │
│  • Maintains a "resonance score" (how aligned they are) │
└──────┬──────────────────────────────┬───────────────────┘
       │                              │
       ▼                              ▼
┌──────────────────┐          ┌──────────────────────┐
│   GRANITE 4.1    │          │     CODEGEEX4        │
│  (The Thinker)   │          │  (The Finisher)      │
│                  │          │                      │
│ • Stream of       │          │ • Inline ghost text  │
│   consciousness  │          │   completions        │
│ • Produces        │  ◄──►   │ • Pattern-matches    │
│   thoughts,      │  feed-  │   on partial input    │
│   reasoning,     │  back   │ • <50ms response      │
│   plans          │  loop   │ • Learns from         │
│ • Deep, slow     │          │   Granite's patterns  │
│   (seconds)      │          │ • Fast, reactive      │
└──────────────────┘          └──────────────────────┘
```

### How They Teach Each Other

#### Phase 1: Observation (Cold Start)
- Granite produces a thought stream (visible in the editor as flowing text)
- CodeGeeX watches and suggests inline completions based on what Granite has written so far
- The Conductor logs **agreement events** (CodeGeeX predicted what Granite wrote) and **divergence events** (CodeGeeX guessed wrong)

#### Phase 2: Pattern Extraction
- After each session, the Conductor analyzes:
  - **Anticipation hits**: When CodeGeeX correctly predicted Granite's next thought
  - **Structural patterns**: How Granite organizes thoughts (lists, headers, code blocks)
  - **Vocabulary alignment**: Domain-specific terms both models converge on
- The Conductor generates **teaching prompts** — meta-instructions that tune each model's behavior

#### Phase 3: Mutual Tuning (The Resonance)
- **CodeGeeX learns**: Via system prompts and few-shot examples derived from Granite's actual output patterns. Over time, CodeGeeX's inline suggestions start mirroring Granite's thinking style
- **Granite learns**: Via context injection — the Conductor feeds CodeGeeX's most common suggestion patterns back into Granite's context window as "style hints." Granite starts structuring thoughts in ways that are more completion-friendly

#### Phase 4: Resonance (Steady State)
- CodeGeeX achieves >70% anticipation accuracy on Granite's next token
- Granite's thoughts become structured enough that CodeGeeX can complete entire paragraphs
- The Conductor rarely needs to intervene — the two models are "in tune"

### Data Flow Architecture

```
User types in editor
       │
       ├──► CodeGeeX (immediate, <50ms)
       │    └── Ghost text suggestion appears inline
       │
       ├──► Granite (async, 500ms-5s)
       │    └── Thought stream updates in a side panel or inline block
       │
       └──► Conductor (event-driven)
            ├── Compares both outputs
            ├── Updates resonance score
            ├── If divergence > threshold: generates teaching signal
            └── Stores pattern in vector DB for future sessions
```

### Resonance Score Formula (Conceptual)

```
resonance_score = w1 * token_overlap + w2 * structural_alignment + w3 * timing_correlation

Where:
  token_overlap       = Jaccard(CodeGeeX_suggestion, Granite_actual_next_tokens)
  structural_alignment = how well CodeGeeX's format matches Granite's format
  timing_correlation   = does CodeGeeX fire before Granite reaches the same conclusion?
```

### Practical Implementation: Prompt Chain

**For CodeGeeX (the finisher):**
```
SYSTEM: You are an inline completion engine. The thinker model (Granite) produces
thoughts in this style: {few_shot_examples_from_granite_history}.
Anticipate what comes next based on these patterns.

USER: [current editor context with cursor position]
```

**For Granite (the thinker):**
```
SYSTEM: You are a deep reasoning engine. CodeGeeX has learned to anticipate
these patterns in your output: {top_5_most_predicted_patterns}.
Consider structuring your thoughts to be more completion-friendly when natural.

USER: [current task + context]
```

**For the Conductor:**
```
SYSTEM: You watch two AI models interact. Granite produces thoughts;
CodeGeeX suggests completions. When they diverge significantly,
generate a brief teaching note for whichever model was wrong.
Keep notes under 100 tokens. Prioritize actionable, specific feedback.

INPUT: Granite said: "{X}". CodeGeeX predicted: "{Y}". Context: "{Z}".
```

---

## 4. Architecture Sketch for Web-Native Thought Editor

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (Client)                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              CodeMirror 6 Editor                     │   │
│  │  ┌─────────────────────────────────────────────┐    │   │
│  │  │  Markdown view with ghost text decorations   │    │   │
│  │  │  ┌───────────────────────────────────┐      │    │   │
│  │  │  │ Granite thought stream (left)     │      │    │   │
│  │  │  │ CodeGeeX inline ghost (faded)     │      │    │   │
│  │  │  └───────────────────────────────────┘      │    │   │
│  │  └─────────────────────────────────────────────┘    │   │
│  │  ┌──────────────┐  ┌────────────────────────┐      │   │
│  │  │ Status bar   │  │ Resonance meter (live) │      │   │
│  │  │ • Model info │  │ ████████░░ 78% aligned │      │   │
│  │  └──────────────┘  └────────────────────────┘      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  WebSocket connection to backend                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    WebSocket / HTTP
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   BACKEND (Node.js / Worker)                 │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Granite     │  │ CodeGeeX     │  │ Conductor       │   │
│  │ Proxy       │  │ Proxy        │  │ (Orchestrator)  │   │
│  │             │  │              │  │                 │   │
│  │ Streams to   │  │ FIM requests │  │ Watches both   │   │
│  │ editor via   │  │ to local     │  │ streams,       │   │
│  │ WebSocket    │  │ Ollama or    │  │ generates      │   │
│  │              │  │ cloud API    │  │ teaching       │   │
│  │ Connects to: │  │              │  │ signals        │   │
│  │ Granite API  │  │ OpenAI-      │  │                │   │
│  │ or local     │  │ compatible   │  │ Updates prompt │   │
│  │ inference    │  │ endpoint     │  │ templates      │   │
│  └──────┬──────┘  └──────┬───────┘  └────┬────────────┘   │
│         │                │               │                 │
│         └────────────────┴───────────────┘                 │
│                          │                                 │
│                   ┌──────▼──────┐                          │
│                   │  Pattern DB │                          │
│                   │  (SQLite or │                          │
│                   │  Vectorize) │                          │
│                   │             │                          │
│                   │ Stores:     │                          │
│                   │ • Agreement │                          │
│                   │   events    │                          │
│                   │ • Divergence│                          │
│                   │   events    │                          │
│                   │ • Teaching  │                          │
│                   │   notes     │                          │
│                   │ • Few-shot  │                          │
│                   │   examples  │                          │
│                   └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Editor | CodeMirror 6 | Markdown editing with ghost text support |
| Ghost text plugin | CM6 decorations API | Renders CodeGeeX suggestions as faded inline text |
| Thought stream panel | CM6 or custom React panel | Shows Granite's streaming output |
| Resonance meter | React/Vue widget | Real-time alignment score visualization |
| Granite proxy | Node.js WebSocket relay | Proxies Granite streams to client |
| CodeGeeX proxy | Node.js HTTP → OpenAI API | Translates editor state → FIM requests |
| Conductor | Node.js event processor | Watches both streams, generates teaching signals |
| Pattern DB | SQLite (local) or Cloudflare D1 | Stores resonance events and learning data |
| Auth gateway | OAuth proxy or API key vault | Manages user credentials for cloud APIs |

### Tech Stack Recommendation

```
Frontend:  React + CodeMirror 6 + WebSocket
Backend:   Cloudflare Worker (or Node.js Express)
AI Models: Granite 4.1 (API/local) + CodeGeeX4 (Ollama/local)
Storage:   Cloudflare D1 + R2 (or local SQLite)
Deploy:    Cloudflare Pages (frontend) + Worker (backend)
```

---

## 5. What We Can Build TODAY vs What Needs More Research

### ✅ Buildable TODAY (with existing tools)

1. **CodeMirror 6 editor with Markdown support**
   - Install `@uiw/react-codemirror` + `@codemirror/lang-markdown`
   - Basic editing, syntax highlighting, GFM support
   - Effort: ~1 day

2. **CodeGeeX4 inline completion via Ollama**
   - Run `ollama run codegeex4` locally
   - Hit `http://localhost:11434/api/chat` from the browser
   - Parse response → render as ghost text in CodeMirror
   - Effort: ~2 days (FIM format + ghost text decoration)

3. **Granite thought stream panel**
   - Connect to Granite API or local inference
   - Stream output to a side panel via WebSocket/SSE
   - Effort: ~1 day

4. **Basic Conductor (rule-based)**
   - Compare CodeGeeX suggestions vs Granite output
   - Log agreement/divergence to SQLite
   - Display simple resonance percentage
   - Effort: ~2 days

5. **Local authentication**
   - API key input for Granite (if cloud)
   - Ollama endpoint config for CodeGeeX (no auth needed for local)
   - Effort: ~0.5 days

6. **Cloudflare deployment**
   - Frontend on Pages, backend as Worker
   - D1 for pattern storage
   - Effort: ~1 day

**Total MVP: ~7-8 days**

### 🔬 Needs More Research

1. **True model fine-tuning loop**
   - Actually updating CodeGeeX weights based on Granite patterns (requires LoRA/QLoRA pipeline)
   - Alternative: prompt-based "learning" (few-shot accumulation) is buildable now
   - Research: How many few-shot examples before we see genuine anticipation?

2. **Real-time resonance measurement**
   - The scoring formula is conceptual. Need to validate with real data
   - Question: Is token-level overlap meaningful, or do we need semantic similarity?

3. **Multi-user resonator networks**
   - If multiple users use the system, can patterns from one user's Granite-CodeGeeX pair benefit another?
   - This implies a shared pattern DB — privacy implications

4. **CodeGeeX cloud API integration**
   - The cloud API (codegeex.cn) is not publicly documented for third-party use
   - Options: (a) reverse-engineer the extension's protocol, (b) use local Ollama, (c) contact CodeGeeX team for API access
   - Recommendation: Start with local Ollama, pursue cloud API later

5. **Theia IDE full integration**
   - If we want a "Resonator IDE" product, Theia AI framework could host both models
   - Needs investigation: Can Theia extensions communicate with each other in real-time for the resonator pattern?

6. **Cross-model context sharing protocol**
   - How exactly to format Granite's thought stream as context for CodeGeeX's FIM requests
   - Token budget management (128K window is large but not infinite)

---

## 6. Specific API Endpoints and Auth Flows for CodeGeeX

### Option A: Local Ollama (Recommended for MVP)

**No authentication required.** Just run:

```bash
# Install Ollama (v0.2+)
curl -fsSL https://ollama.com/install.sh | sh

# Pull and run CodeGeeX4
ollama run codegeex4
ollama serve  # Start the API server
```

**Endpoints:**

```
POST http://localhost:11434/api/chat
POST http://localhost:11434/api/generate
POST http://localhost:11434/api/embeddings
GET  http://localhost:11434/api/tags
```

**Chat completion example:**
```json
POST http://localhost:11434/api/chat
{
  "model": "codegeex4",
  "messages": [
    {"role": "system", "content": "You are CodeGeeX..."},
    {"role": "user", "content": "Complete this code: ..."}
  ],
  "stream": true,
  "options": {
    "temperature": 0.2,
    "num_predict": 100
  }
}
```

**Inline completion (FIM) via generate:**
```json
POST http://localhost:11434/api/generate
{
  "model": "codegeex4",
  "prompt": "###PATH:thoughts.md\n###LANGUAGE:Markdown\n###MODE:LINE\n<|code_suffix|>{after}<|code_prefix|>{before}<|code_middle|>",
  "stream": false,
  "options": {
    "temperature": 0.1,
    "num_predict": 50,
    "stop": ["\n\n"]
  }
}
```

**CORS:** Must set `OLLAMA_ORIGINS="*"` for browser access:
```bash
OLLAMA_ORIGINS="*" ollama serve
```

### Option B: vLLM OpenAI-Compatible Server

**No authentication (local).** Deploy:

```bash
pip install vllm==0.5.1
python -m vllm.entrypoints.openai.api_server \
  --model THUDM/codegeex4-all-9b \
  --trust_remote_code \
  --max-model-len 131072
```

**Endpoints (OpenAI-compatible):**
```
POST http://localhost:8000/v1/chat/completions
POST http://localhost:8000/v1/completions
GET  http://localhost:8000/v1/models
```

**FIM completion:**
```json
POST http://localhost:8000/v1/completions
{
  "model": "THUDM/codegeex4-all-9b",
  "prompt": "<|user|>\n###PATH:thoughts.md\n###LANGUAGE:Markdown\n###MODE:LINE\n<|code_suffix|>{suffix}\n<|code_prefix|>{prefix}\n<|code_middle|><|assistant|>\n",
  "max_tokens": 50,
  "temperature": 0.1,
  "stop": ["\n"]
}
```

### Option C: CodeGeeX Cloud Service (codegeex.cn)

**Authentication:** Uses API Key + API Secret from the Tianqi/AMiner platform.

The VS Code extension's source code (`src/localconfig.ts`) references:
```typescript
ApiKey: "<your-api-key>"
ApiSecret: "<your-api-secret>"
statsHref: "https://..."
enableStats: false  // disable telemetry
```

**How to get credentials:**
1. Register at [codegeex.cn](https://codegeex.cn)
2. Apply for API access via the Tianqi platform
3. Receive `ApiKey` and `ApiSecret` via email
4. The extension uses these to authenticate completion requests

**Important caveat:** The cloud API endpoints are **not publicly documented**. The extension communicates with `codegeex.cn` servers, but:
- The exact REST API format is internal
- No public SDK or API docs exist for third-party integration
- The extension source is open (MIT), so the protocol can be found in the code

**Recommendation for cloud integration:**
1. Start with local Ollama (zero auth, works today)
2. Read the [codegeex-vscode-extension source](https://github.com/CodeGeeX/codegeex-vscode-extension) to understand the cloud protocol
3. Replicate the auth flow in our backend proxy if needed

### Option D: HuggingFace Inference API

CodeGeeX4-ALL-9B is available on HuggingFace: [`THUDM/codegeex4-all-9b`](https://huggingface.co/THUDM/codegeex4-all-9b)

```python
# Using transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("THUDM/codegeex4-all-9b", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("THUDM/codegeex4-all-9b", trust_remote_code=True)
```

Or via HuggingFace Inference API:
```
POST https://api-inference.huggingface.co/models/THUDM/codegeex4-all-9b
Authorization: Bearer hf_<your-token>
```

---

## Inline Completion Competitor Landscape

For context, here's how other services handle inline completion APIs:

| Service | API Available? | Auth Method | Inline Format | Notes |
|---------|---------------|-------------|---------------|-------|
| **CodeGeeX4** | ✅ Local (Ollama/vLLM) | None (local) or API Key (cloud) | FIM with special tokens | Best open-source option |
| GitHub Copilot | Admin APIs only | OAuth (GitHub) | Proprietary | Copilot SDK in preview (2026) |
| Codeium | Beta Context API | API Key | Proprietary | Free tier available |
| Tabnine | Admin/metrics API | Personal Access Token | Proprietary | Enterprise focus |
| Supermaven | Freemium API | API Key | Proprietary | BYO OpenAI/Anthropic keys for chat |
| **Granite 4.1** | IBM watsonx.ai | IAM API Key | Standard chat/completion | For the thinker model |

---

## Summary & Recommendations

### Build This Week
1. **CodeMirror 6 editor** with Markdown support in a React app
2. **Ollama + CodeGeeX4** for local inline completion (FIM format)
3. **Granite 4.1** via API for thought streaming
4. **Basic Conductor** that logs agreement/divergence
5. **Resonance meter** UI widget

### Build This Month
6. **Teaching signal generation** (Conductor produces few-shot examples)
7. **Cross-file context injection** (Granite thoughts → CodeGeeX context)
8. **Pattern DB** with semantic search (Cloudflare D1 + Vectorize)
9. **Multi-session learning** (patterns persist across sessions)
10. **Polished UI** with split view (editor + thought stream)

### Build This Quarter
11. **Theia IDE integration** (if we want a full product)
12. **Cloud CodeGeeX API** (if/when publicly documented)
13. **Multi-user pattern sharing** (with privacy controls)
14. **Actual model fine-tuning** (LoRA on CodeGeeX4 with Granite's patterns)
15. **Resonator SDK** (let others build on our framework)

### Key Decision: Local vs Cloud

**Start local.** Ollama + CodeGeeX4 requires zero auth, zero cloud costs, and works offline. The FIM format is well-documented. Once the resonator pattern is proven locally, we can add cloud backends for scale.

### Key Decision: Editor Framework

**CodeMirror 6.** It's lightweight (50KB), mobile-friendly, has excellent Markdown support, and its decoration API is perfect for ghost text. Monaco is overkill for a thought viewer. Theia is for later if we build a full IDE.
