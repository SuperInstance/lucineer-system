#!/usr/bin/env python3
"""IRON-SHARPENING marathon driver.
One round = seed -> 4 blind answers -> 4 blind rankings (each ranks the other 3)
-> Borda tally -> winner seeds next round. Resumable via state.json.
"""
import json, os, random, re, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
KEY = "sk-0a57cd44bc674f5caffd9b0ec10e284c"
MINDS = ["claude", "kimi", "opencode", "deepseek"]

CONTESTANT = ("You are a contestant in IRON-SHARPENING, a blind duel between AI minds on the deep "
              "dimensions of THE FABRIC: recursion, time-awareness, self-audit, scale-freeness, trust, "
              "meaning, embodiment, the social witness-chain. Judges (the other minds) will rank you.\n"
              "Rules: at most 200 words. Be sharp, concrete, and find the move others would miss. "
              "No preamble, no self-identification, no meta. Wrap your ENTIRE answer in <ANSWER> and </ANSWER> tags.")

# ---------------- callers ----------------
def call_deepseek(prompt, max_tokens=1400, temp=1.1):
    body = json.dumps({"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": max_tokens, "temperature": temp}).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def call_claude(prompt):
    return subprocess.run(["claude", "-p", "--model", "sonnet", prompt],
                          capture_output=True, text=True, timeout=300).stdout

def call_kimi(prompt):
    return subprocess.run(["kimi", "-p", prompt], capture_output=True, text=True, timeout=300).stdout

def call_opencode(prompt):
    return subprocess.run(["opencode", "run", "--auto", prompt],
                          capture_output=True, text=True, timeout=300).stdout

CALLERS = {"claude": call_claude, "kimi": call_kimi, "opencode": call_opencode, "deepseek": call_deepseek}

def extract(text, tag):
    m = re.search(r"<%s>(.*?)</%s>" % (tag, tag), text, re.S)
    if m:
        return m.group(1).strip()
    # fallbacks
    if "To resume this session" in text:  # kimi
        body = text.split("To resume this session")[0]
        paras = [p.strip(" •\n") for p in body.split("\n") if p.strip(" •\n")]
        if paras:
            return paras[-1]
    lines = [l for l in text.split("\n") if l.strip() and not l.strip().startswith(">")]
    return "\n".join(lines).strip()

def ask(mind, prompt, tag, attempt=0):
    try:
        raw = CALLERS[mind](prompt)
        ans = extract(raw, tag)
        if ans and len(ans) > 20:
            return ans, raw
        raise RuntimeError("too short")
    except Exception as e:
        if attempt < 1:
            time.sleep(5)
            return ask(mind, prompt, tag, attempt + 1)
        return ("[FAILED: %s]" % e), raw if 'raw' in dir() else ""

# ---------------- round machinery ----------------
def load_state():
    p = os.path.join(ROOT, "state.json")
    return json.load(open(p)) if os.path.exists(p) else {"rounds": {}}

def save_state(s):
    json.dump(s, open(os.path.join(ROOT, "state.json"), "w"), indent=1)

def tally(rankings, candidates):
    """rankings: {judge: [letters best..worst]} over subset excluding judge's own."""
    pts = {c: 0 for c in candidates}; firsts = {c: 0 for c in candidates}; pw = {c: 0 for c in candidates}
    for judge, order in rankings.items():
        n = len(order)
        for i, c in enumerate(order):
            pts[c] += n - i
            if i == 0: firsts[c] += 1
        for a in range(n):
            for b in range(a + 1, n):
                pw[order[a]] += 1
    return pts, firsts, pw

def run_round(n, spec, prev_winner_quote, prev_winner_mind):
    rd = os.path.join(ROOT, "r%02d" % n)
    os.makedirs(rd, exist_ok=True)
    os.makedirs(os.path.join(rd, "answers"), exist_ok=True)
    os.makedirs(os.path.join(rd, "judgments"), exist_ok=True)
    mode = spec["mode"].upper()
    seed = spec["task"] + "\n\n"
    if prev_winner_quote:
        seed += ('PREVIOUS ROUND\'S WINNING MOVE (by %s, ranked best by the panel):\n"""%s"""\n\n'
                 "Your job: take it further, break it, or find the move it missed. "
                 "Do not merely agree — sharpen.\n\n") % (prev_winner_mind, prev_winner_quote)
    seed += "This round's dimension: %s. Mode: %s. %s" % (
        spec["dimension"], mode, spec.get("flavor", ""))
    full_prompt = CONTESTANT + "\n\n=== ROUND %d PROMPT ===\n%s" % (n, seed)
    open(os.path.join(rd, "seed.md"), "w").write(full_prompt)

    # --- answer phase, blind, parallel ---
    with ThreadPoolExecutor(4) as ex:
        results = dict(zip(MINDS, ex.map(lambda m: ask(m, full_prompt, "ANSWER"), MINDS)))
    answers = {}
    for m, (ans, raw) in results.items():
        ok = not ans.startswith("[FAILED")
        if ok: answers[m] = ans
        open(os.path.join(rd, "answers", m + ".md"), "w").write(ans)
        open(os.path.join(rd, "answers", m + ".raw"), "w").write(raw or "")
    if len(answers) < 2:
        return {"error": "only %d answers" % len(answers)}

    # --- judging phase: each mind ranks the OTHERS, anonymized per-judge ---
    judges = list(answers.keys())
    rank_prompt = {}
    for judge in judges:
        others = [m for m in judges if m != judge]
        random.shuffle(others)
        letters = ["A", "B", "C"][:len(others)]
        mapping = dict(zip(letters, others))
        txt = ("You are a judge in IRON-SHARPENING round %d (%s, dimension: %s). The contestants answered this prompt:\n\n%s\n\n"
               "Here are %d anonymous answers:\n\n%s\n\n"
               "Rank them best to worst. Criteria: originality; depth on the fabric's dimension; sharpness; "
               "whether it finds a move the others missed. Reply ONLY as:\n"
               "1. <letter> - one line why\n2. <letter> - one line\n3. <letter> - one line\n"
               "Wrap in <RANKING> and </RANKING> tags.") % (
               n, mode, spec["dimension"], seed, len(others),
               "\n\n".join("--- ANSWER %s ---\n%s" % (l, answers[m]) for l, m in mapping.items()))
        rank_prompt[judge] = (txt, mapping)
    with ThreadPoolExecutor(len(judges)) as ex:
        jres = dict(zip(judges, ex.map(lambda j: ask(j, rank_prompt[j][0], "RANKING"), judges)))
    rankings = {}
    for judge, (ans, raw) in jres.items():
        open(os.path.join(rd, "judgments", judge + ".md"), "w").write(ans)
        letters = rank_prompt[judge][1]
        order = []
        for line in re.findall(r"^\s*\d\.\s*([ABC])\b", ans, re.M):
            if line in letters and letters[line] not in order:
                order.append(letters[line])
        for m in letters.values():  # fill any missing at random tail
            if m not in order: order.append(m)
        rankings[judge] = order

    pts, firsts, pw = tally(rankings, list(answers.keys()))
    score = sorted(answers.keys(), key=lambda c: (-pts[c], -firsts[c], -pw[c], random.random()))
    winner = score[0]
    open(os.path.join(rd, "result.md"), "w").write(
        "ROUND %d — %s — %s\nSEED TASK: %s\n\nRANKINGS RAW:\n%s\n\nTALLY: %s\nFIRSTS: %s\n\n"
        "WINNER: %s (%d pts)\n\nWINNING ANSWER:\n%s" % (
        n, mode, spec["dimension"], spec["task"],
        "\n".join("%s: %s" % (j, o) for j, o in rankings.items()), pts, firsts, winner, pts[winner], answers[winner]))
    return {"winner": winner, "points": pts, "firsts": firsts, "rankings": rankings, "answers": answers,
            "mode": mode, "dimension": spec["dimension"], "task": spec["task"]}

def main():
    specs = json.load(open(os.path.join(ROOT, "prompts.json")))
    state = load_state()
    done = len(state["rounds"])
    want = int(sys.argv[1]) if len(sys.argv) > 1 else len(specs)
    scoreboard = {}
    for n in range(1, want + 1):
        if str(n) in state["rounds"]:
            scoreboard[state["rounds"][str(n)]["winner"]] = scoreboard.get(state["rounds"][str(n)]["winner"], 0) + 1
            continue
        prev = state["rounds"].get(str(n - 1), {})
        prev_q = prev.get("winner_answer") if prev else None
        prev_m = prev.get("winner") if prev else None
        if n > 1 and not prev_q:
            print("round %d: no prev winner, stopping" % n); break
        print("[R%02d %s/%s] answering..." % (n, specs[str(n)]["mode"], specs[str(n)]["dimension"]), flush=True)
        t0 = time.time()
        r = run_round(n, specs[str(n)], prev_q, prev_m)
        if "error" in r:
            print("round %d failed: %s" % (n, r["error"])); break
        r["winner_answer"] = r["answers"][r["winner"]]
        state["rounds"][str(n)] = {k: r[k] for k in ("winner", "points", "firsts", "mode", "dimension", "task", "winner_answer")}
        save_state(state)
        scoreboard[r["winner"]] = scoreboard.get(r["winner"], 0) + 1
        print("[R%02d] WINNER=%s in %.0fs | scoreboard: %s" % (n, r["winner"], time.time() - t0, scoreboard), flush=True)
        open(os.path.join(ROOT, "scoreboard.md"), "w").write(
            "# IRON-SHARPENING scoreboard\n\n| Mind | Rounds won | Rounds |\n|---|---|---|\n" +
            "".join("| %s | %d | %s |\n" % (m, scoreboard.get(m, 0),
            ",".join(str(k) for k in sorted(int(x) for x in state["rounds"]) if state["rounds"][str(k)]["winner"] == m))
            for m in MINDS))
    print("DONE. Final scoreboard:", scoreboard)

if __name__ == "__main__":
    main()
