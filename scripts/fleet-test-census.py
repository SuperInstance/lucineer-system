#!/usr/bin/env python3
"""
Fleet Test Census — A polyglot test detector.

Scans all repos in a directory and reports actual test counts per repo,
understanding Rust (cargo), TypeScript/JS (vitest/jest), Python (pytest),
and Lua (busted/spec) ecosystems.

Usage: python3 fleet-test-census.py /path/to/projects
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class RepoReport:
    name: str
    language: str
    files: int
    commits: int
    has_tests: bool
    test_count: int
    test_runner: str
    test_files: list
    has_ci: bool
    last_commit: str


def run_git(repo: Path, *args) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo)] + list(args),
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception:
        return ""


def count_rust_tests(repo: Path) -> tuple[int, list[str]]:
    """Count Rust tests by grepping for #[test] across the entire repo."""
    test_files = []
    count = 0
    
    # Scan ALL .rs files in the repo (excluding target/)
    for f in repo.rglob("*.rs"):
        rel = str(f.relative_to(repo))
        if rel.startswith("target/") or "/target/" in rel:
            continue
        try:
            content = f.read_text(errors='ignore')
            test_count = len(re.findall(r'#\[test\]', content))
            if test_count > 0:
                test_files.append(rel)
                count += test_count
        except:
            pass
    
    return count, test_files


def count_ts_js_tests(repo: Path) -> tuple[int, list[str]]:
    """Count TS/JS tests by finding .test.* files and counting it/describe/test calls."""
    test_files = []
    count = 0
    
    patterns = ["*.test.ts", "*.test.js", "*.test.tsx", "*.test.jsx",
                "*.spec.ts", "*.spec.js", "*.spec.tsx", "*.spec.jsx"]
    
    for pattern in patterns:
        for f in repo.rglob(pattern):
            if "node_modules" in str(f):
                continue
            test_files.append(str(f.relative_to(repo)))
            try:
                content = f.read_text(errors='ignore')
                # Count it() and test() calls
                count += len(re.findall(r'\b(?:it|test)\s*\(', content))
            except:
                pass
    
    # Also check __tests__/ directories
    tests_dir = repo / "__tests__"
    if tests_dir.is_dir():
        for f in tests_dir.rglob("*"):
            if f.suffix in ('.ts', '.js', '.tsx', '.jsx'):
                if "node_modules" in str(f):
                    continue
                test_files.append(str(f.relative_to(repo)))
                try:
                    content = f.read_text(errors='ignore')
                    count += len(re.findall(r'\b(?:it|test)\s*\(', content))
                except:
                    pass
    
    return count, test_files


def count_python_tests(repo: Path) -> tuple[int, list[str]]:
    """Count Python tests by finding test_*.py and *_test.py files."""
    test_files = []
    count = 0
    
    for pattern in ["test_*.py", "*_test.py"]:
        for f in repo.rglob(pattern):
            if any(skip in str(f) for skip in ['__pycache__', 'node_modules', '.venv', 'venv']):
                continue
            test_files.append(str(f.relative_to(repo)))
            try:
                content = f.read_text(errors='ignore')
                # Count def test_ and assert
                count += len(re.findall(r'def test_', content))
            except:
                pass
    
    # Also check for pytest-style classes
    for f in repo.rglob("*.py"):
        if any(skip in str(f) for skip in ['__pycache__', 'node_modules', '.venv', 'venv']):
            continue
        if f.name.startswith("test_") or f.name.endswith("_test.py"):
            continue  # Already counted
        try:
            content = f.read_text(errors='ignore')
            if 'def test_' in content:
                if str(f.relative_to(repo)) not in test_files:
                    test_files.append(str(f.relative_to(repo)))
                count += len(re.findall(r'def test_', content))
        except:
            pass
    
    return count, test_files


def count_lua_tests(repo: Path) -> tuple[int, list[str]]:
    """Count Lua tests by finding spec/ files with describe/it."""
    test_files = []
    count = 0
    
    spec_dir = repo / "spec"
    if spec_dir.is_dir():
        for f in spec_dir.rglob("*.lua"):
            test_files.append(str(f.relative_to(repo)))
            try:
                content = f.read_text(errors='ignore')
                count += len(re.findall(r'\bIt\s*\(', content))
                count += len(re.findall(r'\bit\s*\(', content))
            except:
                pass
    
    return count, test_files


def detect_language(repo: Path) -> str:
    """Detect primary language of repo."""
    if (repo / "Cargo.toml").exists():
        return "rust"
    if (repo / "package.json").exists():
        return "typescript"
    if list(repo.rglob("*.py")) and not (repo / "package.json").exists():
        return "python"
    if (repo / "go.mod").exists():
        return "go"
    # Check file extensions
    rust = sum(1 for _ in repo.rglob("*.rs") if "target" not in str(_))
    ts = sum(1 for _ in repo.rglob("*.ts") if "node_modules" not in str(_))
    py = sum(1 for _ in repo.rglob("*.py") if "__pycache__" not in str(_))
    lua = sum(1 for _ in repo.rglob("*.lua"))
    
    counts = {"rust": rust, "typescript": ts, "python": py, "lua": lua}
    primary = max(counts, key=counts.get)
    return primary if counts[primary] > 0 else "unknown"


def scan_repo(repo: Path) -> RepoReport:
    """Scan a single repo."""
    name = repo.name
    language = detect_language(repo)
    
    files_str = run_git(repo, "ls-files")
    files = len(files_str.splitlines()) if files_str else 0
    
    commits_str = run_git(repo, "rev-list", "--count", "HEAD")
    commits = int(commits_str) if commits_str.isdigit() else 0
    
    last_commit = run_git(repo, "log", "-1", "--format=%ci")
    
    has_ci = (repo / ".github" / "workflows").is_dir()
    
    # Count tests based on language
    if language == "rust":
        test_count, test_files = count_rust_tests(repo)
        runner = "cargo test" if test_count > 0 else "none"
    elif language == "typescript":
        test_count, test_files = count_ts_js_tests(repo)
        # Check package.json for runner
        pkg = repo / "package.json"
        runner = "unknown"
        if pkg.exists():
            try:
                pkg_content = json.loads(pkg.read_text())
                test_script = pkg_content.get("scripts", {}).get("test", "")
                if "vitest" in test_script:
                    runner = "vitest"
                elif "jest" in test_script:
                    runner = "jest"
                elif "mocha" in test_script:
                    runner = "mocha"
                elif test_script:
                    runner = test_script.split()[0] if test_script else "none"
                else:
                    runner = "none"
            except:
                pass
    elif language == "python":
        test_count, test_files = count_python_tests(repo)
        runner = "pytest" if test_count > 0 else "none"
    elif language == "lua":
        test_count, test_files = count_lua_tests(repo)
        runner = "busted" if test_count > 0 else "none"
    else:
        # Try all
        rust_count, rust_files = count_rust_tests(repo)
        ts_count, ts_files = count_ts_js_tests(repo)
        py_count, py_files = count_python_tests(repo)
        lua_count, lua_files = count_lua_tests(repo)
        test_count = rust_count + ts_count + py_count + lua_count
        test_files = rust_files + ts_files + py_files + lua_files
        runner = "mixed"
    
    return RepoReport(
        name=name,
        language=language,
        files=files,
        commits=commits,
        has_tests=test_count > 0,
        test_count=test_count,
        test_runner=runner,
        test_files=test_files[:10],  # Cap at 10 for display
        has_ci=has_ci,
        last_commit=last_commit[:10] if last_commit else "unknown"
    )


def main():
    projects_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/eileen/projects")
    
    reports = []
    for item in sorted(projects_dir.iterdir()):
        if not item.is_dir():
            continue
        if not (item / ".git").is_dir():
            continue
        try:
            report = scan_repo(item)
            reports.append(report)
        except Exception as e:
            print(f"Error scanning {item.name}: {e}", file=sys.stderr)
    
    # Sort by test count (untested first)
    reports.sort(key=lambda r: (r.test_count == 0, r.language, r.name))
    
    # Print table
    print(f"{'Repo':<40} {'Lang':<6} {'Files':>6} {'Commits':>8} {'Tests':>6} {'Runner':<12} {'CI':>3} {'Last':<12}")
    print("-" * 100)
    
    total_tests = 0
    untested = 0
    for r in reports:
        print(f"{r.name:<40} {r.language:<6} {r.files:>6} {r.commits:>8} {r.test_count:>6} {r.test_runner:<12} {'✓' if r.has_ci else '✗':>3} {r.last_commit:<12}")
        total_tests += r.test_count
        if r.test_count == 0 and r.files > 3:
            untested += 1
    
    print("-" * 100)
    print(f"Total repos: {len(reports)} | Total tests: {total_tests} | Untested (>3 files): {untested}")
    
    # Save JSON
    output_path = Path("/home/eileen/.openclaw/workspace/memory/overnight/fleet-test-census.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump([asdict(r) for r in reports], f, indent=2)
    print(f"\nJSON saved to {output_path}")


if __name__ == "__main__":
    main()
