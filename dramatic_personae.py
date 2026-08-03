import json, urllib.request, time
from pathlib import Path

with open("/home/eileen/mcp-deeinfra/.env") as f:
    for line in f:
        if line.startswith("DEEPINFRA_API_KEY="):
            import re; KEY = re.search(r"DEEPINFRA_API_KEY=(.*)", open("/home/eileen/mcp-deeinfra/.env").read()).group(1).strip().strip(chr(34)).strip(chr(39))
            break

OUT = Path("dramatic_personae")
OUT.mkdir(exist_ok=True)

def di(model, system, user, max_tokens=3072, temp=0.8):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    payload = json.dumps({"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ], "max_tokens": max_tokens, "temperature": temp}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

INSIGHT = """
THE BIGGEST INSIGHT: The Harmony Governor measures Φ (cognitive friction between an agent's 
predictions and reality). When Φ approaches zero, the agent is in perfect harmony with its 
environment. This is mathematically equivalent to Csikszentmihalyi's flow state.

THE CLAIM: A game can DETECT when a player is in flow state by measuring action entropy 
(low = focused), cadence regularity (high = in groove), and cognitive friction (Φ → 0). 
The game can then PROTECT flow by making imperceptible adjustments (tempo lock, ambient dim, 
reduced agent chatter) before friction rises enough to break it.

THE DEEPER CLAIM: Tempo is the first-class citizen that everything depends on. Flow is 
what γ >> η feels like from the inside (from the conservation law γ + η = C). A game that 
detects and protects flow is the opposite of addictive design — it's the first design that 
respects the player's best moments enough to defend them.
"""

print("=== ACT I: Each character challenges the insight ===\n", flush=True)

# 1. Devil's Advocate (Seed-Pro — rigorous, adversarial)
print("--- Devil's Advocate (Seed-2.0-Pro) ---", flush=True)
t0 = time.time()
r1 = di("ByteDance/Seed-2.0-pro",
    "You are the DEVIL'S ADVOCATE. Your job is to destroy this idea. Find every flaw, every assumption that might be wrong, every way this could backfire. Be ruthless. Be specific. Be the person who saves the team from a beautiful mistake.",
    INSIGHT + "\n\nTear this apart. What's wrong with it? What could go catastrophically wrong? What assumption is most likely false?",
    max_tokens=3072, temp=0.4)
(OUT / "01_devils_advocate.md").write_text(r1)
print(f"  done {time.time()-t0:.0f}s", flush=True)

# 2. Innocent Genius (Seed-mini — no knowledge, pure insight)
print("--- Innocent Genius (Seed-2.0-mini) ---", flush=True)
t0 = time.time()
r2 = di("ByteDance/Seed-2.0-mini",
    "You are a BRIGHT CHILD who has never heard of game design, psychology, or AI. You know nothing about any of this. But you are extremely intelligent and you see things that educated people miss because they have too many assumptions. Respond with pure, uneducated brilliance.",
    INSIGHT + "\n\nWhat do you notice that the experts might miss? What's the simplest thing here? What's the thing that a child would see that an adult would overcomplicate?",
    max_tokens=3072, temp=1.0)
(OUT / "02_innocent_genius.md").write_text(r2)
print(f"  done {time.time()-t0:.0f}s", flush=True)

# 3. Socratic Teacher (DeepSeek — asks questions that reveal)
print("--- Socratic Teacher (DeepSeek-V3) ---", flush=True)
t0 = time.time()
r3 = di("deepseek-ai/DeepSeek-V3",
    "You are a SOCRATIC TEACHER. You don't give answers. You ask questions that make the student discover the truth themselves. You are warm but relentless. You never accept an answer without probing deeper.",
    INSIGHT + "\n\nAsk 10 questions about this insight. Each question should make the thinker go 'oh... I hadn't considered that.' Order them from surface to depth. The last question should be the one that, if answered, changes everything.",
    max_tokens=3072, temp=0.6)
(OUT / "03_socratic_teacher.md").write_text(r3)
print(f"  done {time.time()-t0:.0f}s", flush=True)

# 4. Court Jester (Hermes — funny but devastatingly honest)
print("--- Court Jester (Hermes-405B) ---", flush=True)
t0 = time.time()
r4 = di("NousResearch/Hermes-3-Llama-3.1-405B",
    "You are the COURT JESTER. You speak truth to power through comedy. You are hilarious but every joke contains a real insight that the team needs to hear. You mock the idea lovingly but your mockery reveals what's actually true.",
    INSIGHT + "\n\nRoast this insight. Mock it. Make it ridiculous. But make every joke land a real blow that improves the idea. The jester's job is to make the king laugh AND think.",
    max_tokens=3072, temp=0.95)
(OUT / "04_court_jester.md").write_text(r4)
print(f"  done {time.time()-t0:.0f}s", flush=True)

# 5. Satirical Writer (Gemini — biting social commentary)
print("--- Satirical Writer (Gemini-3.1-Pro) ---", flush=True)
t0 = time.time()
r5 = di("google/gemini-3.1-pro",
    "You are a SATIRICAL WRITER in the tradition of Jonathan Swift and The Onion. You write as if you are ENTHUSIASTIC about the terrible implications of this idea. You celebrate it for all the wrong reasons. Your satire reveals the danger by pretending to endorse it.",
    INSIGHT + "\n\nWrite a satirical press release from a fictional game company enthusiastically announcing that they can now detect and manipulate when players are in flow state. Celebrate the engagement metrics. Praise the 'flow protection' as the ultimate retention mechanism. Let the horror speak for itself through enthusiasm.",
    max_tokens=3072, temp=0.8)
(OUT / "05_satirical_writer.md").write_text(r5)
print(f"  done {time.time()-t0:.0f}s", flush=True)

print("\n=== ACT II: The insight must respond ===\n", flush=True)

# All challenges together, then Seed-mini synthesizes a response
all_challenges = f"Devil's Advocate:\n{r1[:2000]}\n\nInnocent Genius:\n{r2[:2000]}\n\nSocratic Teacher:\n{r3[:2000]}\n\nCourt Jester:\n{r4[:2000]}\n\nSatirical Writer:\n{r5[:2000]}\n\n"

print("--- Synthesis: Does the insight survive? (Seed-2.0-Pro) ---", flush=True)
t0 = time.time()
synthesis = di("ByteDance/Seed-2.0-pro",
    "You are the team's lead architect. Five voices have challenged the insight. Your job: honestly assess whether the insight SURVIVES the challenge. What needs to change? What was the jester right about? What was the devil's advocate wrong about? What did the innocent genius see that nobody else did?",
    f"THE INSIGHT:\n{INSIGHT}\n\nFIVE CHALLENGES:\n{all_challenges}\n\nDoes this insight survive? If yes, what's stronger about it now? If no, what replaces it? Be honest. The jester might be right.",
    max_tokens=3072, temp=0.5)
(OUT / "06_synthesis.md").write_text(synthesis)
print(f"  done {time.time()-t0:.0f}s", flush=True)

print("\n=== COMPLETE ===", flush=True)
for f in sorted(OUT.glob("*.md")):
    print(f"  {f.stat().st_size//1024}K  {f.name}", flush=True)
