#!/usr/bin/env python3
"""Fleet Inventory — catalog everything on board the SS Lucineer.

Inspired by "The Ship's Manifest: A Catalog of Everything On Board"
This is the real version. The creative piece was the idea; this is the implementation.

Usage:
    python3 fleet-inventory.py [--projects-dir /home/eileen/projects]
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime


def get_disk_usage(path):
    """Get disk usage of a path in human-readable format."""
    try:
        result = subprocess.run(
            ["du", "-sh", path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return result.stdout.split()[0]
    except Exception:
        pass
    return "unknown"


def count_files(path, extensions):
    """Count files with given extensions, excluding node_modules/target/.git."""
    count = 0
    exclude = {"node_modules", "target", ".git", "__pycache__", ".next", "dist", ".cache"}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            if any(f.endswith(ext) for ext in extensions):
                count += 1
    return count


def count_tests_rust(path):
    """Count #[test] attributes in Rust source files."""
    count = 0
    exclude = {"target", ".git"}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            if f.endswith(".rs"):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r") as fh:
                        content = fh.read()
                        count += content.count("#[test]")
                except Exception:
                    pass
    return count


def count_tests_python(path):
    """Count test_ function definitions in Python files."""
    count = 0
    exclude = {".git", "__pycache__", "node_modules", ".venv", "venv"}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            if f.startswith("test_") and f.endswith(".py"):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r") as fh:
                        content = fh.read()
                        count += content.count("def test_")
                except Exception:
                    pass
            elif f.endswith(".py") and not f.startswith("test_"):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r") as fh:
                        content = fh.read()
                        # Count inline test functions
                        count += content.count("def test_")
                except Exception:
                    pass
    return count


def count_tests_ts(path):
    """Count it() and test() calls in TypeScript test files."""
    count = 0
    exclude = {"node_modules", ".git", "dist", ".next"}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            if (f.endswith(".test.ts") or f.endswith(".test.tsx") or
                f.endswith(".test.mjs") or f.endswith(".test.js")):
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r") as fh:
                        content = fh.read()
                        # Count it("...", ...) and test("...", ...) patterns
                        count += content.count("it(") + content.count("test(")
                        # Subtract double-counts from it.test patterns
                except Exception:
                    pass
    return count


def is_git_repo(path):
    return os.path.isdir(os.path.join(path, ".git"))


def get_git_remote(path):
    """Get the git remote URL if available."""
    try:
        result = subprocess.run(
            ["git", "-C", path, "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def scan_repo(path):
    """Scan a single repo and return its inventory entry."""
    name = os.path.basename(path)
    disk = get_disk_usage(path)

    # Detect language
    rust_files = count_files(path, [".rs"])
    ts_files = count_files(path, [".ts", ".tsx", ".mjs"])
    py_files = count_files(path, [".py"])
    lua_files = count_files(path, [".lua"])
    html_files = count_files(path, [".html"])

    # Count tests
    rust_tests = count_tests_rust(path) if rust_files > 0 else 0
    py_tests = count_tests_python(path) if py_files > 0 else 0
    ts_tests = count_tests_ts(path) if ts_files > 0 else 0
    total_tests = rust_tests + py_tests + ts_tests

    # Detect primary language
    counts = {"Rust": rust_files, "TS": ts_files, "Python": py_files, "Lua": lua_files, "HTML": html_files}
    primary_lang = max(counts, key=counts.get) if max(counts.values()) > 0 else "N/A"

    remote = get_git_remote(path)

    return {
        "name": name,
        "disk": disk,
        "language": primary_lang,
        "rust_files": rust_files,
        "ts_files": ts_files,
        "py_files": py_files,
        "lua_files": lua_files,
        "html_files": html_files,
        "rust_tests": rust_tests,
        "py_tests": py_tests,
        "ts_tests": ts_tests,
        "total_tests": total_tests,
        "remote": remote,
    }


def main():
    projects_dir = sys.argv[sys.argv.index("--projects-dir") + 1] if "--projects-dir" in sys.argv else "/home/eileen/projects"

    print(f"# Fleet Inventory — SS Lucineer")
    print(f"# Generated: {datetime.now().isoformat()}")
    print(f"# Projects directory: {projects_dir}")
    print()

    repos = []
    for entry in sorted(os.listdir(projects_dir)):
        path = os.path.join(projects_dir, entry)
        if is_git_repo(path):
            repos.append(scan_repo(path))

    # Sort by disk usage (descending) — crude but effective
    #repos.sort(key=lambda r: r["total_tests"], reverse=True)

    # Summary
    total_repos = len(repos)
    total_tests = sum(r["total_tests"] for r in repos)
    tested_repos = sum(1 for r in repos if r["total_tests"] > 0)
    untested_repos = total_repos - tested_repos

    print(f"## Summary")
    print(f"- Total repos: {total_repos}")
    print(f"- Total tests: {total_tests}")
    print(f"- Tested repos: {tested_repos}")
    print(f"- Untested repos: {untested_repos}")
    print(f"- Test coverage: {tested_repos}/{total_repos} repos ({100*tested_repos//total_repos}%)")
    print()

    # Table
    print(f"## By Repository")
    print(f"| Repo | Lang | Tests | Rust | TS | Py | Disk |")
    print(f"|------|------|-------|------|----|----|------|")

    for r in sorted(repos, key=lambda x: x["total_tests"], reverse=True):
        print(f"| {r['name']} | {r['language']} | {r['total_tests']} | {r['rust_tests']} | {r['ts_tests']} | {r['py_tests']} | {r['disk']} |")

    print()

    # Untested repos
    untested = [r for r in repos if r["total_tests"] == 0 and (r["rust_files"] + r["ts_files"] + r["py_files"]) > 0]
    if untested:
        print(f"## Untested Repos (with source code)")
        print(f"| Repo | Lang | Source Files | Disk |")
        print(f"|------|------|--------------|------|")
        for r in untested:
            src = r["rust_files"] + r["ts_files"] + r["py_files"] + r["lua_files"]
            print(f"| {r['name']} | {r['language']} | {src} | {r['disk']} |")
        print()

    # JSON output
    json_path = os.path.join(os.path.dirname(__file__), "fleet-inventory.json")
    with open(json_path, "w") as f:
        json.dump({"generated": datetime.now().isoformat(), "repos": repos}, f, indent=2)
    print(f"## JSON output: {json_path}")


if __name__ == "__main__":
    main()
