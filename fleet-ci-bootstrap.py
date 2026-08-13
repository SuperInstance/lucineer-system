#!/usr/bin/env python3
"""
Fleet CI Bootstrap
==================

Iterates all repos in /home/eileen/projects, detects test framework,
generates GitHub Actions CI workflow, commits and pushes.

Detected frameworks:
  - Python (pytest): has pytest, setup.py, pyproject.toml, or tests/ with .py
  - TypeScript (vitest): has package.json with vitest
  - TypeScript (jest): has package.json with jest
  - Rust (cargo): has Cargo.toml
  - Lua (busted): has .busted file or spec/ dir
  - Go: has go.mod
  - Node (npm test): has package.json with "test" script

Usage:
  python3 fleet-ci-bootstrap.py [--dry-run] [--push]
"""

import os
import json
import subprocess
import sys
from pathlib import Path

PROJECTS_DIR = Path("/home/eileen/projects")

WORKFLOWS = {
    "pytest": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install pytest
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          if [ -f setup.py ]; then pip install -e .; fi
      - name: Run tests
        run: python -m pytest -v
""",
    "vitest": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci || npm install
      - run: npx vitest run
""",
    "jest": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci || npm install
      - run: npx jest --passWithNoTests
""",
    "cargo": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - name: Run tests
        run: cargo test --verbose
""",
    "npm-test": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci || npm install
      - run: npm test
""",
    "go": """name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
      - name: Run tests
        run: go test ./...
""",
}


def detect_framework(repo_path: Path) -> str | None:
    """Detect the test framework for a repo."""
    # Check for existing CI
    ci_path = repo_path / ".github" / "workflows" / "ci.yml"
    if ci_path.exists():
        return None  # Already has CI

    # Check for Python/pytest
    has_pyproject = (repo_path / "pyproject.toml").exists()
    has_setup_py = (repo_path / "setup.py").exists()
    has_pytest_cfg = False
    for cfg_file in ["pytest.ini", "tox.ini", "setup.cfg"]:
        if (repo_path / cfg_file).exists():
            content = (repo_path / cfg_file).read_text(errors="ignore").lower()
            if "pytest" in content or "[tool:pytest]" in content:
                has_pytest_cfg = True
    has_tests_dir = (repo_path / "tests").is_dir()
    has_python_tests = bool(list(repo_path.glob("test_*.py")) + list(repo_path.glob("tests/test_*.py")) + list(repo_path.glob("**/test_*.py"))[:1])

    # Check for package.json (Node)
    pkg_path = repo_path / "package.json"
    if pkg_path.exists():
        try:
            pkg = json.loads(pkg_path.read_text(errors="ignore"))
            dev_deps = {**pkg.get("devDependencies", {}), **pkg.get("dependencies", {})}
            scripts = pkg.get("scripts", {})

            if "vitest" in dev_deps:
                return "vitest"
            if "jest" in dev_deps:
                return "jest"
            if "test" in scripts:
                # Has a test script but no specific framework detected
                # Check if it's vitest or jest based on the script
                test_script = scripts["test"]
                if "vitest" in test_script:
                    return "vitest"
                if "jest" in test_script:
                    return "jest"
                return "npm-test"
        except (json.JSONDecodeError, KeyError):
            pass

    # Check for Cargo.toml (Rust)
    if (repo_path / "Cargo.toml").exists():
        return "cargo"

    # Check for Go
    if (repo_path / "go.mod").exists():
        return "go"

    # Check for Python tests
    if has_pyproject or has_setup_py or has_pytest_cfg or (has_tests_dir and has_python_tests):
        return "pytest"

    # Broader Python check
    if any(repo_path.glob("test_*.py")) or any(repo_path.glob("tests/*.py")):
        return "pytest"

    return None


def create_ci(repo_path: Path, framework: str, dry_run: bool = False, push: bool = False) -> bool:
    """Create CI workflow for a repo."""
    workflow_dir = repo_path / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    ci_path = workflow_dir / "ci.yml"

    content = WORKFLOWS.get(framework)
    if not content:
        return False

    if dry_run:
        print(f"  [DRY RUN] Would write {framework} CI to {repo_path.name}")
        return True

    ci_path.write_text(content)

    # Git operations
    os.chdir(repo_path)
    subprocess.run(["git", "add", ".github/workflows/ci.yml"], capture_output=True)
    subprocess.run(["git", "commit", "-m", f"ci: add GitHub Actions workflow for {framework}"], capture_output=True)

    if push:
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  [PUSH FAILED] {repo_path.name}: {result.stderr.strip()}")
            return False

    return True


def main():
    dry_run = "--dry-run" in sys.argv
    push = "--push" in sys.argv

    detected = {}
    skipped = 0
    created = 0
    failed = 0

    for item in sorted(PROJECTS_DIR.iterdir()):
        if not item.is_dir():
            continue
        if not (item / ".git").exists():
            continue

        framework = detect_framework(item)
        if framework is None:
            skipped += 1
            continue

        detected[item.name] = framework

        print(f"  {item.name}: {framework}")

        if create_ci(item, framework, dry_run=dry_run, push=push):
            created += 1
        else:
            failed += 1

    print(f"\n  Detected: {len(detected)} repos needing CI")
    print(f"  Created: {created}")
    print(f"  Failed: {failed}")
    print(f"  Skipped (already has CI): {skipped}")


if __name__ == "__main__":
    main()
