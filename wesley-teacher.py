#!/usr/bin/env python3
"""Send Wesley's response to the Cloudflare Workers AI teacher."""
import json, urllib.request, pathlib, sys, re

ACCOUNT_ID = "049ff5e84ecf636b53b162cbb580aae6"
cfg = pathlib.Path.home() / ".config/.wrangler/config/default.toml"
token = re.search(r'oauth_token\s*=\s*"([^"]+)"', cfg.read_text()).group(1)

wesley_file = pathlib.Path(sys.argv[1])
wesley = wesley_file.read_text()

# Extract just Wesley's response body (between the --- markers)
parts = wesley.split("---")
body = parts[1].strip() if len(parts) > 2 else wesley

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
req = urllib.request.Request(
    f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3.1-8b-instruct-fast",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=120) as r:
    out = json.loads(r.read())

result = out["result"]["response"]
print(result)
