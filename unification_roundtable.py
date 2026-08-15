import json, urllib.request, time, subprocess
from pathlib import Path
from loadkey import get_key

KEY = get_key()

OUT = Path("unification_roundtable")
OUT.mkdir(exist_ok=True)

def di(model, system, user, max_tokens=4096, temp=0.7):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    payload = json.dumps({"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ], "max_tokens": max_tokens, "temperature": temp}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

VISION = Path("UNIFICATION_VISION.md").read_text()[:4000]

print("=== R1: Seed-mini opens ===", flush=True)
t0 = time.time()
r1 = di("ByteDance/Seed-2.0-mini",
    "You are the most expansive thinker in a room of elite AI advisors. Open the boldest possible conversation.",
    VISION + "\n\nFrame the 5 most important questions. Give your boldest answer for each.",
    max_tokens=4096, temp=1.0)
(OUT / "01_seed_opens.md").write_text(r1)
print(f"  done {time.time()-t0:.0f}s", flush=True)

print("=== R2a: Seed-Pro ===", flush=True)
t0 = time.time()
r2a = di("ByteDance/Seed-2.0-pro",
    "You are the deep reasoning advisor. Find what's actually buildable.",
    f"Discussion opening:\n{r1[:3000]}\n\nFor each question: what's buildable? How? What's the ONE decade-defining idea?",
    max_tokens=4096, temp=0.5)
(OUT / "02a_seed_pro.md").write_text(r2a)
print(f"  done {time.time()-t0:.0f}s", flush=True)

print("=== R2b: Hermes-405B ===", flush=True)
t0 = time.time()
r2b = di("NousResearch/Hermes-3-Llama-3.1-405B",
    "You are the creative soul advisor. Find the emotional core.",
    f"Discussion opening:\n{r1[:3000]}\n\nWhat would make a player CRY? What would make an agent feel ALIVE? What is the emotional thesis?",
    max_tokens=4096, temp=0.85)
(OUT / "02b_hermes.md").write_text(r2b)
print(f"  done {time.time()-t0:.0f}s", flush=True)

print("=== R3a: Qwen3.5-397B ===", flush=True)
t0 = time.time()
r3a = di("Qwen/Qwen3.5-397B-A17B",
    "You are the systems thinker. Find hidden connections.",
    f"Opening:\n{r1[:2000]}\nSeed-Pro:\n{r2a[:1500]}\nHermes:\n{r2b[:1500]}\n\nWhat connects countdowns to beats to cognition? What if Vectorize used the Eisenstein lattice? What if builds were MIDI notes? Design the unified data structure.",
    max_tokens=4096, temp=0.5)
(OUT / "03a_qwen.md").write_text(r3a)
print(f"  done {time.time()-t0:.0f}s", flush=True)

print("=== R3b: Gemini ===", flush=True)
t0 = time.time()
r3b = di("google/gemini-3.1-pro",
    "You are the product strategist. What SHIPS?",
    f"Opening:\n{r1[:2000]}\n\nMVP? Demo? Moat? What NVIDIA tech makes this possible NOW? Write the launch press release.",
    max_tokens=4096, temp=0.6)
(OUT / "03b_gemini.md").write_text(r3b)
print(f"  done {time.time()-t0:.0f}s", flush=True)

print("=== R4: Seed-mini closes ===", flush=True)
t0 = time.time()
r4 = di("ByteDance/Seed-2.0-mini",
    "You are the discussion leader. Close with synthesis.",
    f"Opening:\n{r1[:1500]}\nSeed-Pro:\n{r2a[:1000]}\nHermes:\n{r2b[:1000]}\nQwen:\n{r3a[:1000]}\nGemini:\n{r3b[:1000]}\n\nSynthesize: the ONE thing to build, 3-sentence pitch, the name, first commit message, dedication.",
    max_tokens=4096, temp=0.9)
(OUT / "04_seed_closes.md").write_text(r4)
print(f"  done {time.time()-t0:.0f}s", flush=True)

print("\n=== COMPLETE ===", flush=True)
