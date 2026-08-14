# README Expansion Log

**Date:** 2026-08-13  
**Task:** Expand every fleet repo README with expository documentation and hyperlinks

## Summary

Expanded 14 READMEs across the fleet. Each README now includes (where applicable):
- **Vision** — what the repo does and WHY it exists, in plain language
- **Architecture** — module maps, data flow diagrams, ASCII architecture diagrams
- **Quick Start** — real build/run/test commands
- **Key Concepts** — expository explanations with hyperlinks to papers, Wikipedia, docs
- **API Reference** — key types, functions, endpoints
- **Configuration** — config files, environment variables, dependencies table
- **Testing** — how tests work, what they cover
- **Deployment** — systemd, wrangler, cron, etc.
- **Further Reading** — curated bibliography with hyperlinks for: Developers, Engineers, Mathematicians, Educators, Students, Architects

## Repos Updated

| # | Repo | Lines Before | Lines After | Commit | Pushed |
|---|------|-------------|-------------|--------|--------|
| 1 | **fleet-gateway** | 108 | 467 | ac33c3f | ✅ |
| 2 | **fleet-memory** | 0 (no README) | 456 | 80e21b5 | ✅ |
| 3 | **fleet-jepa-midi** | 457 | 695 | a697274 | ✅ |
| 4 | **fleet-ensemble** | 231 | 505 | f2283d9 | ✅ |
| 5 | **tapscript-studio** | 54 | 358 | 705b479 | ✅ |
| 6 | **tapscript-worker** | 0 (no README) | 381 | 67b4116 | ✅ |
| 7 | **fleet-dashboard** | 265 | 412 | 5c46417 | ✅ |
| 8 | **fleet-wiki** | 164 | 250 | a080540 | ✅ |
| 9 | **fleet-radio** | 172 | 207 | c502e2f | ✅ |
| 10 | **fleet-tts** | 66 | 251 | 5d569fd | ⚠️ remote not found |
| 11 | **fleet-pipeline** | 75 | 109 | fbeeda6 | ✅ |
| 12 | **fleet-envelope** | 108 | 264 | cf58104 | ✅ |
| 13 | **fleet-inventory** | 69 | 105 | (already committed) | ⚠️ OAuth workflow scope issue |
| 14 | **fleet-connections** | 128 | 284 | (already committed) | ✅ |

## Notes

- **fleet-cns** does not exist as a separate repo. The CNS bus functionality lives in `cns-bridge`, `cns-echo`, and `cns-monitor` (separate repos).
- **fleet-tts** push failed — the GitHub remote `SuperInstance/fleet-tts` may not exist or may be under a different name. Commit is local.
- **fleet-inventory** push failed due to OAuth workflow scope — the commit touches `.github/workflows/ci.yml` which requires `workflow` scope.
- **fleet-jepa-midi** already had a massive 457-line README. Added 238 lines: Quick Start, API Reference, Configuration, Testing, Deployment, and a structured Further Reading bibliography organized by audience (Developers, Musicians, Educators, Mathematicians, Engineers, AI Researchers).
- **fleet-ensemble** already had 231 lines. Added 274 lines: Quick Start, Key Concepts (seven feel parameters, tri-chamber, alignment math), API Reference, Configuration, Testing, Deployment, Further Reading.

## What Was Added to Each README

### Common sections added:

1. **Table of Contents** — for navigation in long READMEs
2. **Vision section** — plain-language explanation of WHAT and WHY, with comparison tables
3. **Architecture diagram** — ASCII art showing the system layout
4. **Module map** — table of source files with line counts and responsibilities
5. **Quick Start** — actual working build/run/test commands
6. **Key Concepts** — expository explanations with Wikipedia/arXiv/blog hyperlinks
7. **API Reference** — types, functions, endpoints with example code
8. **Configuration** — config files, env vars, dependency tables
9. **Testing** — test descriptions and what they cover
10. **Deployment** — systemd services, wrangler deploy, cron configs
11. **Further Reading** — curated bibliography organized by audience role:
    - For Developers (implementation guides, API docs)
    - For Engineers (ops, scaling, performance)
    - For Mathematicians (formal definitions, proofs)
    - For Educators (teaching resources)
    - For Students (beginner-friendly links)
    - For Architects (system design patterns)
