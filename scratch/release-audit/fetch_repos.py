#!/usr/bin/env python3
"""Step 1: enumerate SuperInstance org repos (bounded). READ-ONLY."""
import json, os, urllib.request, urllib.error, time

TOK = open("/home/eileen/.config/fleet/github-token").read().strip()
UA = "fleet-scout/1.0"
OUT = "/home/eileen/.openclaw/workspace/scratch/release-audit/repos.json"

def get(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOK}",
        "User-Agent": UA,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and attempt < 2:
                time.sleep(3)
                continue
            raise
    raise RuntimeError("unreachable")

repos = []
page = 1
while len(repos) < 200 and page <= 3:
    data = get(f"https://api.github.com/users/SuperInstance/repos?per_page=100&sort=pushed&page={page}")
    if not isinstance(data, list) or not data:
        break
    for r in data:
        repos.append({
            "name": r["name"], "language": r.get("language"),
            "pushed_at": r.get("pushed_at"), "size": r.get("size"),
            "archived": r.get("archived"), "has_pages": r.get("has_pages"),
            "default_branch": r.get("default_branch"),
            "description": (r.get("description") or "")[:160],
            "fork": r.get("fork"), "private": r.get("private"),
            "stargazers": r.get("stargazers_count"),
        })
    print(f"page {page}: {len(data)} repos (total {len(repos)})")
    page += 1

repos = repos[:120]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(repos, f, indent=1)
print("SAVED", len(repos), "repos ->", OUT)
langs = {}
for r in repos:
    langs[r["language"] or "None"] = langs.get(r["language"] or "None", 0) + 1
for k, v in sorted(langs.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
