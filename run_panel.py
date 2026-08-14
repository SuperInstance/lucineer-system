#!/usr/bin/env python3
"""Run multi-model panel discussion on browser-native AI enhancement."""
import json, urllib.request, time, sys, os

API_KEY = os.environ.get('DEEPINFRA_API_KEY', '')
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

CONTEXT = """Context: We have a Dynamic Cognition Architecture for an AI character called Slackwater. It has three layers:
(1) Local Thinker - a small model (Granite 2B) that generates a stream of consciousness at 1-2 thoughts/second,
(2) Conductor - a large model (GLM-5.2) that adjusts the Thinker prompts every 30s based on play quality metrics,
(3) Game - Roblox world providing state snapshots.

There is also a Thought Viewer - a web-native editor using CodeMirror 6 that displays the thought stream with inline AI completions via CodeGeeX. This uses a 'resonator pattern' where a thinker model and finisher model teach each other - CodeGeeX learns to anticipate Granite's patterns, and Granite's output becomes more completion-friendly over time.

The architecture includes a Journal format (JSONL with timestamp, beat, game_state, thought, lean, action_taken, quality_signals), a temporal encoding system (T-minus/MIDI-like beat patterns for play rhythms), and a Vectorize index for pattern storage.
"""

MODELS = {
    "creative": ("ByteDance/Seed-2.0-mini", "You are a creative AI architect participating in a panel discussion. Give bold, imaginative, outside-the-box answers. Be specific and technical but creative. 400-600 words.", 0.9),
    "systems": ("Qwen/Qwen3-Max", "You are a systems architect participating in a panel discussion. Focus on architecture, data flow, performance, and integration patterns. Be specific and technical. 400-600 words.", 0.7),
    "philosopher": ("NousResearch/Hermes-3-Llama-3.1-405B", "You are a philosopher of AI and consciousness participating in a panel discussion. Consider the deeper implications, the nature of the system being described, and what it means for human-AI interaction. Be thoughtful and profound but grounded. 400-600 words.", 0.8),
}

def call_model(model, system_prompt, user_prompt, temperature=0.8, max_tokens=900):
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }).encode()
    req = urllib.request.Request(API_URL, data=payload, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]

TOPICS = [
    {
        "id": "topic1",
        "title": "How could Gemini-in-Chrome enhance a real-time thought stream viewer?",
        "question": """QUESTION: How could Gemini-in-Chrome enhance a real-time thought stream viewer?

Gemini Nano runs built into Chrome, can access page DOM, and offers on-device AI APIs:
- Prompt API (general text generation)
- Summarization API
- Translation API  
- Writing API
- DOM access (can see what's on the page)

Think about:
- What happens when the browser itself has an AI engine that can see the same page the user sees?
- How does this differ from a server-side AI looking at the stream?
- What real-time enhancements become possible with zero latency, zero API costs, full privacy?
- How could Gemini Nano complement the existing Granite/CodeGeeX resonator pattern?"""
    },
    {
        "id": "topic2",
        "title": "What if the Local Thinker ran partly in the browser via WebGPU?",
        "question": """QUESTION: What if the Local Thinker ran partly in the browser via WebGPU?

Consider these browser-native ML technologies:
- Transformers.js (HuggingFace models running in browser via WASM/WebGPU)
- ONNX Runtime Web (optimized model execution)
- WebLLM (LLM inference entirely in browser using WebGPU)
- Chrome's built-in AI (Gemini Nano)

Currently the Local Thinker is Granite 2B on Ollama (CPU, ~500ms inference). What if it also ran in the browser?

Think about:
- Which parts of the cognition stack could be browser-native vs server-side?
- What models work well in-browser (Phi-3-mini, Qwen2.5-1.5B, Granite compact)?
- How does browser-native inference change the latency profile and architecture?
- Could we have a hybrid: browser model for instant reactions + server model for deep thoughts?
- What about offline operation?"""
    },
    {
        "id": "topic3",
        "title": "Design a Chrome Extension that watches the thought stream and suggests interventions",
        "question": """QUESTION: Design a Chrome Extension that watches the thought stream and suggests interventions.

The extension would:
- Monitor the thought stream (JSONL entries with thought text, quality_signals, lean/action data)
- Watch for patterns: repetitive thoughts, stuck states, quality drops, emotional shifts
- Suggest interventions to the Conductor (prompt changes, parameter tweaks)
- Potentially inject UI elements into the thought viewer

For your assigned perspective, design a specific aspect:
- Creative: What novel intervention types and UI patterns could the extension use?
- Systems: What's the technical architecture (content scripts, service workers, messaging)?
- Philosopher: When should the extension intervene vs let the AI find its own way? What's the ethics of shaping an AI's thoughts?"""
    },
    {
        "id": "topic4",
        "title": "How could a browser-native inline finisher (CodeGeeX-like) resonate with a server-side Granite model?",
        "question": """QUESTION: How could a browser-native inline finisher resonate with a server-side Granite model?

The 'resonator pattern' currently has:
- Granite (thinker) on server producing thought streams
- CodeGeeX (finisher) suggesting inline completions
- A Conductor watching both and generating teaching signals

What if the finisher ran IN the browser? Using WebLLM, Transformers.js, or Chrome's built-in AI?

Think about:
- The resonator pattern but split across client/server boundary
- Latency asymmetry: browser finisher at <50ms vs server thinker at 500ms+
- What teaching signals work best across this boundary?
- Could the browser model learn from the server model in real-time?
- How does this change the architecture and what new capabilities emerge?
- Could we crowdsource pattern learning across multiple browsers?"""
    },
    {
        "id": "topic5",
        "title": "What game mechanics become possible when the AI lives in the browser?",
        "question": """QUESTION: What game mechanics become possible when the AI lives in the browser?

When AI runs browser-native, it can:
- Access the DOM (read and modify the page)
- Be aware of other tabs and browser state
- React to mouse/keyboard events in real-time
- Use WebRTC for peer-to-peer communication
- Access webcam/microphone (with permission)
- Trigger notifications, change favicon, modify scroll position
- Run service workers in the background

Think about gameplay innovations:
- DOM-based interactions (the AI modifies the page as part of gameplay)
- Cross-tab experiences (AI spans multiple browser tabs/windows)
- Page context awareness (AI reacts to what websites you visit)
- ARG-like mechanics blending game and browser
- Multiplayer through WebRTC (AI agents talking to each other peer-to-peer)
- The browser AS the game world"""
    },
]

def run_topic(topic, perspective_key, perspective_label):
    model_id, system_prompt, temp = MODELS[perspective_key]
    user_prompt = CONTEXT + "\n" + topic["question"]
    print(f"  Calling {model_id} ({perspective_label})...", flush=True)
    try:
        result = call_model(model_id, system_prompt, user_prompt, temp)
        return result
    except Exception as e:
        return f"ERROR calling {model_id}: {e}"

# Run all topics
results = {}
for i, topic in enumerate(TOPICS):
    print(f"\n{'='*60}", flush=True)
    print(f"TOPIC {i+1}: {topic['title']}", flush=True)
    print(f"{'='*60}", flush=True)
    
    topic_results = {}
    for key, label in [("creative", "Creative"), ("systems", "Systems"), ("philosopher", "Philosophical")]:
        print(f"  [{label} perspective]...", flush=True)
        response = run_topic(topic, key, label)
        topic_results[key] = {"model": MODELS[key][0], "label": label, "response": response}
        print(f"  Done ({len(response)} chars)", flush=True)
        time.sleep(1)  # small delay between calls
    
    results[topic["id"]] = {
        "title": topic["title"],
        "question": topic["question"],
        "responses": topic_results
    }
    
    # Save partial results after each topic
    with open("/home/eileen/projects/lucineer-system/panel_raw_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved partial results.", flush=True)

print("\n\nALL TOPICS COMPLETE!", flush=True)
print(f"Total topics: {len(results)}", flush=True)
