#!/usr/bin/env python3
"""Night school runner: feed pieces to Wesley, save his responses."""
import json, time, urllib.request, pathlib, re, sys

BASE = pathlib.Path("/home/eileen/projects/ai-writings")
STREAM = BASE / "wesley-stream"

PIECES = [
    "2026-08-13-1745-the-watch-that-never-ends.md",
    "2026-08-11-2100-the-interval-is-the-song.md",
    "2026-08-11-0800-a-letter-from-the-quota-gate.md",
]

# Standing curriculum (from wesley-journal/feedback.md):
# - num_predict 250 (truncation fix, raised from 150)
# - assignment: one image that is NOT in the original
# - start where the noticing starts, no throat-clearing wonder-words
PROMPT_TMPL = (
    "Read this and write a 3-sentence creative response. Be young. Be surprised. "
    "Include one image that is NOT in the original. Do not open with words like "
    "'whimsical,' 'fascinating,' or 'astonishing' - start where the noticing starts.\n\n---\n\n{body}"
)

def slug(fn):
    s = re.sub(r"^\d{4}-\d{2}-\d{2}-\d{4}-", "", fn)
    return s.replace(".md", "")

def ask_wesley(prompt):
    payload = {
        "model": "granite3.1-dense:2b",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.95, "num_predict": 250},
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())

results = []
now = time.strftime("%Y-%m-%d_%H%M")
for fn in PIECES:
    body = (BASE / fn).read_text()
    resp = ask_wesley(PROMPT_TMPL.format(body=body))
    text = resp.get("response", "").strip()
    eval_tokens = resp.get("eval_count", 0)
    done_reason = resp.get("done_reason", "?")
    out = STREAM / f"wesley_{slug(fn)}_{now}.md"
    out.write_text(
        f"# Wesley reads: {slug(fn)}\n\n"
        f"*Night school, {time.strftime('%Y-%m-%d %H:%M')} AKDT. "
        f"Source: {fn}*\n\n"
        f"*Prompt: 3-sentence creative response, be young, be surprised, one image NOT in the "
        f"original, no stock wonder-words. temp 0.95, num_predict 250 (standing truncation fix). "
        f"Generated {eval_tokens} tokens, done_reason={done_reason}.*\n\n---\n\n"
        f"{text}\n\n---\n\n"
        f"*Reading time: {len(body.splitlines())} lines fed. "
        f"Wesley is 2B parameters of pure earnestness.*\n"
    )
    results.append((fn, str(out), eval_tokens, done_reason, text))
    print(f"OK  {fn} -> {out.name}  ({eval_tokens} tok, {done_reason})")

# Pick the response for the teacher: prefer a complete one (done_reason=length means truncated)
complete = [r for r in results if r[3] != "length"]
pick = (complete or results)[0]
print("\nPICK_FOR_TEACHER:", pick[0])
print("FILE:", pick[1])
print("RESPONSE:\n" + pick[4])
