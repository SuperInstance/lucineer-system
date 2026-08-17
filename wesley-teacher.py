#!/usr/bin/env python3
"""Send one of Wesley's responses to the Cloudflare Workers AI teacher.

Reads a wesley-stream session file (the first CLI argument), extracts just
Wesley's response body, and asks the teacher model for ONE specific,
actionable improvement in 50 words or less.

The response-body extraction lives in ``wesley_night_school.py`` so it can
be regression-tested; this file is the I/O shell that loads the Wrangler
OAuth token and makes the Cloudflare call. Errors are loud and specific
(missing file, missing token, no argument) instead of a bare traceback.
"""
import json
import pathlib
import re
import sys
import urllib.request

from wesley_night_school import TEACHER_MODEL, extract_response_body

ACCOUNT_ID = "049ff5e84ecf636b53b162cbb580aae6"
WRANGLER_CONFIG = pathlib.Path.home() / ".config/.wrangler/config/default.toml"
CF_AI_URL = (
    "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
)


def load_oauth_token():
    """Read the Wrangler OAuth token from its default config file."""
    try:
        cfg = WRANGLER_CONFIG.read_text()
    except OSError as exc:
        sys.exit(f"cannot read Wrangler config {WRANGLER_CONFIG}: {exc}")
    match = re.search(r'oauth_token\s*=\s*"([^"]+)"', cfg)
    if not match:
        sys.exit(f"no oauth_token found in {WRANGLER_CONFIG}")
    return match.group(1)


def ask_teacher(body, token):
    """Ask the teacher model for one actionable improvement of ``body``."""
    prompt = (
        "Here is what a 2B parameter student model wrote. Give ONE specific, "
        "actionable improvement in 50 words or less.\n\n---\n\n" + body
    )
    payload = {
        "messages": [
            {"role": "system", "content": "You are a writing teacher. Be specific and brief."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 120,
    }
    url = CF_AI_URL.format(account_id=ACCOUNT_ID, model=TEACHER_MODEL)
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        out = json.loads(resp.read())
    return out["result"]["response"]


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: wesley-teacher.py <wesley-stream-file.md>")

    wesley_file = pathlib.Path(sys.argv[1])
    try:
        wesley = wesley_file.read_text()
    except OSError as exc:
        sys.exit(f"cannot read {wesley_file}: {exc}")

    body = extract_response_body(wesley)
    token = load_oauth_token()
    print(ask_teacher(body, token))


if __name__ == "__main__":
    main()
