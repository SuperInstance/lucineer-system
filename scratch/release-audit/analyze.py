#!/usr/bin/env python3
"""Step 2: release/deploy readiness matrix. READ-ONLY. No publishes."""
import json, re, urllib.request, urllib.error, time, sys
from concurrent.futures import ThreadPoolExecutor

TOK = open("/home/eileen/.config/fleet/github-token").read().strip()
UA = "fleet-scout/1.0"
REPOS = json.load(open("/home/eileen/.openclaw/workspace/scratch/release-audit/repos.json"))
OUT = "/home/eileen/.openclaw/workspace/scratch/release-audit/matrix.json"

def req(url, accept="application/vnd.github+json", raw=False, timeout=25):
    h = {"User-Agent": UA}
    if raw:
        h["Accept"] = accept
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""

def gh(url, accept="application/vnd.github+json"):
    r = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOK}", "User-Agent": UA, "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28"})
    try:
        with urllib.request.urlopen(r, timeout=25) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""

def top_level(tree):
    return {p.split("/")[0] for p in tree}

def analyze(repo):
    name = repo["name"]; br = repo["default_branch"] or "main"
    out = {"name": name, "language": repo["language"], "size": repo["size"],
           "pushed_at": repo["pushed_at"], "archived": repo["archived"],
           "has_pages": repo["has_pages"], "desc": repo["description"],
           "private": repo.get("private"), "stars": repo.get("stargazers")}
    st, body = gh(f"https://api.github.com/repos/SuperInstance/{name}/git/trees/{br}?recursive=1")
    if st != 200:
        out["error"] = f"tree:{st}"
        return out
    try:
        tree = [e["path"] for e in json.loads(body).get("tree", [])]
    except Exception:
        tree = []
    tl = top_level(tree)
    out["file_count"] = len(tree)
    out["manifests"] = [m for m in ("pyproject.toml", "setup.py", "package.json",
                                    "Cargo.toml", "wrangler.toml", "wrangler.jsonc",
                                    "deno.json", "go.mod") if m in tl]
    out["has_tests"] = any(p.startswith("tests/") or "/test/" in p or p.startswith("test/")
                           or re.search(r"(^|/)test_.*\.py$|\.(test|spec)\.(js|ts|jsx|tsx)$", p) for p in tree)
    out["has_ci"] = any(p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml")) for p in tree)
    out["has_readme"] = any(p.lower().startswith("readme") for p in tl)
    out["has_license"] = any(p.lower().startswith(("license", "licence")) for p in tl)
    out["static_entry"] = [p for p in ("index.html", "docs/index.html", "public/index.html", "site/index.html") if p in tree]
    out["has_docs_dir"] = any(p.startswith("docs/") and p.endswith((".md", ".html")) for p in tree[:2000])
    out["docker"] = any(p.lower() in ("dockerfile", "compose.yaml", "docker-compose.yml") for p in tl)

    # fetch manifests for name/version
    for m in out["manifests"]:
        st, txt = gh(f"https://api.github.com/repos/SuperInstance/{name}/contents/{m}",
                     accept="application/vnd.github.raw")
        if st != 200:
            continue
        out.setdefault("manifest_text", {})[m] = txt[:4000]
    return out

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(analyze, REPOS))

# ---- parse package identities + registry existence ----
def parse_pkg(r, txt):
    try:
        d = json.loads(txt)
    except Exception:
        return None
    return {"name": d.get("name"), "version": d.get("version"),
            "private": bool(d.get("private")), "scripts": list((d.get("scripts") or {}).keys())[:8]}

def parse_pyproject(txt):
    name = ver = None
    m = re.search(r'^\s*name\s*=\s*["\']([^"\']+)["\']', txt, re.M)
    if m: name = m.group(1)
    m = re.search(r'^\s*version\s*=\s*["\']([^"\']+)["\']', txt, re.M)
    if m: ver = m.group(1)
    if not name:
        m = re.search(r'name\s*=\s*["\']([^"\']+)["\']', txt)
        if m: name = m.group(1)
    if not ver:
        m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', txt)
        if m: ver = m.group(1)
    return name, ver

def parse_setup_py(txt):
    name = ver = None
    m = re.search(r'name\s*=\s*["\']([^"\']+)["\']', txt)
    if m: name = m.group(1)
    m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', txt)
    if m: ver = m.group(1)
    return name, ver

def parse_cargo(txt):
    name = ver = None
    m = re.search(r'^\s*name\s*=\s*"([^"]+)"', txt, re.M)
    if m: name = m.group(1)
    m = re.search(r'^\s*version\s*=\s*"([^"]+)"', txt, re.M)
    if m: ver = m.group(1)
    m = re.search(r'^\s*publish\s*=\s*false', txt, re.M)
    return name, ver, bool(m)

idents = []          # (repo, ecosystem, name, version, extra)
for r in results:
    mt = r.get("manifest_text", {})
    for m, txt in mt.items():
        if m == "package.json":
            p = parse_pkg(r, txt)
            if p and p["name"]:
                r["node"] = p
                idents.append((r["name"], "npm", p["name"], p.get("version"), p))
        elif m in ("pyproject.toml", "setup.py"):
            n, v = parse_pyproject(txt) if m == "pyproject.toml" else parse_setup_py(txt)
            if n:
                r.setdefault("py", {})[m] = {"name": n, "version": v}
                idents.append((r["name"], "pypi", n, v, {"file": m}))
        elif m == "Cargo.toml":
            n, v, nopub = parse_cargo(txt)
            if n:
                r["cargo"] = {"name": n, "version": v, "publish_false": nopub}
                idents.append((r["name"], "crates", n, v, {"publish_false": nopub}))

def registry(ident):
    repo, eco, nm, ver, extra = ident
    if eco == "pypi":
        s, _ = req(f"https://pypi.org/pypi/{nm}/json", raw=True)
        return {"repo": repo, "eco": eco, "pkg": nm, "version": ver,
                "exists": s == 200, "status": s, "extra": extra}
    if eco == "npm":
        s, b = req(f"https://registry.npmjs.org/{urllib.parse.quote(nm, safe='@')}", raw=True)
        pub = None
        if s == 200:
            try:
                j = json.loads(b); pub = list((j.get("versions") or {}).keys())[-1]
            except Exception: pass
        return {"repo": repo, "eco": eco, "pkg": nm, "version": ver, "exists": s == 200,
                "status": s, "latest_published": pub, "extra": extra}
    if eco == "crates":
        s, b = req(f"https://crates.io/api/v1/crates/{nm}", raw=True)
        return {"repo": repo, "eco": eco, "pkg": nm, "version": ver, "exists": s == 200,
                "status": s, "extra": extra}
    return None

import urllib.parse
with ThreadPoolExecutor(max_workers=6) as ex:
    reg = [x for x in ex.map(registry, idents) if x]

json.dump({"repos": results, "registry": reg}, open(OUT, "w"), indent=1)
print("repos analyzed:", len(results), "| package idents:", len(idents), "| registry checks:", len(reg))
man = [r for r in results if r.get("manifests")]
print("with manifests:", len(man))
print("with static entry:", sum(1 for r in results if r.get("static_entry")))
print("with ci:", sum(1 for r in results if r.get("has_ci")))
print("with tests:", sum(1 for r in results if r.get("has_tests")))
unpub = [x for x in reg if not x["exists"]]
print("UNPUBLISHED:", len(unpub))
for x in unpub[:15]:
    print("  ", x["eco"], x["pkg"], x["version"], "->", x["repo"])
