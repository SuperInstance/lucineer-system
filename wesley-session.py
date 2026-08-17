#!/usr/bin/env python3
"""Night school runner: feed pieces to Wesley, save his responses.

Reads a fixed list of pieces, sends each to the local Ollama model
(``granite3.1-dense:2b``) with the standing night-school prompt, and writes
one markdown file per response into the ``wesley-stream`` directory.

Pure transformations (slugging, prompt building, file rendering) live in
``wesley_night_school.py`` so they can be regression-tested. This file is the
thin I/O shell: it reads the pieces, calls Ollama, and writes the files.

A single piece failing (Ollama down, missing file, truncation) no longer
kills the batch: the loop records the failure and continues, then reports
what it could and could not feed Wesley.
"""
import json
import pathlib
import sys
import time
import urllib.request

from wesley_night_school import (
    WESLEY_MODEL,
    build_prompt,
    render_session_file,
    slug,
)

BASE = pathlib.Path("/home/eileen/projects/ai-writings")
STREAM = BASE / "wesley-stream"

PIECES = [
    "2026-08-13-1745-the-watch-that-never-ends.md",
    "2026-08-11-2100-the-interval-is-the-song.md",
    "2026-08-11-0800-a-letter-from-the-quota-gate.md",
]

OLLAMA_URL = "http://localhost:11434/api/generate"
NUM_PREDICT = 250
TEMPERATURE = 0.95


def ask_wesley(prompt):
    """Send one prompt to local Ollama and return the parsed JSON response."""
    payload = {
        "model": WESLEY_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": TEMPERATURE, "num_predict": NUM_PREDICT},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read())


def run_one(fn, now):
    """Feed one piece to Wesley and write his response file.

    Returns the same 5-tuple the teacher picker expects:
    ``(source_filename, output_path, eval_tokens, done_reason, text)``.
    """
    body = (BASE / fn).read_text()
    response = ask_wesley(build_prompt(body))
    text = response.get("response", "").strip()
    eval_tokens = response.get("eval_count", 0)
    done_reason = response.get("done_reason", "?")
    out = STREAM / f"wesley_{slug(fn)}_{now}.md"
    out.write_text(
        render_session_file(
            slug=slug(fn),
            source=fn,
            timestamp=time.strftime("%Y-%m-%d %H:%M"),
            eval_tokens=eval_tokens,
            done_reason=done_reason,
            text=text,
            body=body,
        )
    )
    return (fn, str(out), eval_tokens, done_reason, text)


def main():
    now = time.strftime("%Y-%m-%d_%H%M")
    results = []
    failures = []

    for fn in PIECES:
        try:
            result = run_one(fn, now)
        except Exception as exc:  # keep the batch alive on a bad piece
            failures.append((fn, exc))
            print(f"FAIL  {fn}: {exc!r}", file=sys.stderr)
            continue
        results.append(result)
        _, out, eval_tokens, done_reason, _ = result
        print(f"OK  {fn} -> {pathlib.Path(out).name}  ({eval_tokens} tok, {done_reason})")

    if not results:
        print(
            f"\nAll {len(failures)} pieces failed; nothing to hand to the teacher.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Pick the response for the teacher: prefer a complete one
    # (done_reason=length means truncated).
    complete = [r for r in results if r[3] != "length"]
    pick = (complete or results)[0]
    print("\nPICK_FOR_TEACHER:", pick[0])
    print("FILE:", pick[1])
    print("RESPONSE:\n" + pick[4])

    if failures:
        print(
            f"\n{len(failures)} piece(s) failed; {len(results)} good.",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
