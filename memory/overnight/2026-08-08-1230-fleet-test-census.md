# Fleet Test Census — 2026-08-08

**Generated:** Sat 2026-08-08 12:08 AKDT  
**Scope:** All git repos under `/home/eileen/projects/`  
**Methodology:** Automated grep-based counting (read-only, no modifications)

## Summary

| Metric | Count |
|--------|-------|
| Total repos scanned | 177 |
| Repos with ≥1 test | 131 |
| Repos with 0 tests | 46 |
| **Total test count (all langs)** | **158991** |
| Rust `#[test]` total | 1723 |
| TypeScript `it()/test()` calls | 8487 |
| TypeScript `.test.ts` files | 309 |
| Python `def test_` functions | 148781 |

> **Note:** For repos with tests, the "Total Tests" column = Rust `#[test]` + TS `it()/test()` calls + Python `def test_` functions. TS file counts are shown separately and not double-counted in the total.

## Rankings (sorted by total test count, descending)

| # | Repo | Rust `#[test]` | TS Test Files | TS `it()/test()` | Python `test_` | **Total Tests** |
|---|------|---------:|------:|------:|------:|---------:|
| 1 | ACE-Step-1.5 | 0 | 0 | 0 | 67377 | **67377** |
| 2 | covers | 0 | 0 | 0 | 51945 | **51945** |
| 3 | study-sunset-ecosystem | 0 | 0 | 0 | 8731 | **8731** |
| 4 | batten-spline | 0 | 0 | 0 | 7276 | **7276** |
| 5 | study-si-papers | 1 | 185 | 6362 | 853 | **7216** |
| 6 | vessel-agent-system | 0 | 0 | 0 | 1757 | **1757** |
| 7 | study-vessel-monitor | 0 | 78 | 1254 | 19 | **1273** |
| 8 | thought-amplifier | 0 | 0 | 0 | 523 | **523** |
| 9 | forgemaster | 0 | 1 | 7 | 444 | **451** |
| 10 | mentis-superinstance | 0 | 0 | 0 | 390 | **390** |
| 11 | voice-reflex-gate | 0 | 0 | 0 | 382 | **382** |
| 12 | slackwater-cognition | 0 | 0 | 0 | 354 | **354** |
| 13 | EXOCORTEX | 0 | 0 | 0 | 354 | **354** |
| 14 | study-cudaclaw | 352 | 0 | 0 | 0 | **352** |
| 15 | study-cudaclaw-main | 352 | 0 | 0 | 0 | **352** |
| 16 | lucineer-brain | 0 | 0 | 0 | 344 | **344** |
| 17 | lingbot-map | 0 | 0 | 0 | 334 | **334** |
| 18 | study-spreader-tool | 0 | 0 | 0 | 303 | **303** |
| 19 | mud-arena | 0 | 0 | 0 | 303 | **303** |
| 20 | cns-bridge | 0 | 0 | 0 | 277 | **277** |
| 21 | lucineer-worker | 0 | 0 | 0 | 258 | **258** |
| 22 | casting-call | 0 | 0 | 0 | 215 | **215** |
| 23 | lucineer-creative | 0 | 0 | 0 | 207 | **207** |
| 24 | eisenstein | 206 | 0 | 0 | 0 | **206** |
| 25 | luciddreamer-content | 0 | 7 | 111 | 86 | **197** |
| 26 | slackwater-tminus | 0 | 0 | 0 | 196 | **196** |
| 27 | slackwater-forge | 0 | 0 | 0 | 189 | **189** |
| 28 | A2A-native-notebookLM | 0 | 7 | 20 | 169 | **189** |
| 29 | slackwater-art-spectrum | 0 | 0 | 0 | 181 | **181** |
| 30 | slackwater-tempo | 0 | 0 | 0 | 178 | **178** |
| 31 | study-lever-runner | 0 | 0 | 0 | 166 | **166** |
| 32 | exocortex-core | 0 | 0 | 0 | 166 | **166** |
| 33 | compaction-teacher | 0 | 0 | 0 | 164 | **164** |
| 34 | symphony-kimi | 0 | 0 | 0 | 162 | **162** |
| 35 | study-flux-lucid | 159 | 0 | 0 | 0 | **159** |
| 36 | fm-experiments | 0 | 0 | 0 | 159 | **159** |
| 37 | lucineer-system | 0 | 0 | 0 | 157 | **157** |
| 38 | fleet-pipeline | 0 | 7 | 154 | 0 | **154** |
| 39 | study-oracle1 | 0 | 0 | 0 | 153 | **153** |
| 40 | slackwater-harmony | 0 | 0 | 0 | 151 | **151** |
| 41 | symphony-glm | 0 | 0 | 0 | 135 | **135** |
| 42 | slackwater-perception | 0 | 0 | 0 | 135 | **135** |
| 43 | study-captain | 0 | 0 | 0 | 134 | **134** |
| 44 | engine-ensign | 0 | 0 | 0 | 130 | **130** |
| 45 | openrooms | 49 | 0 | 0 | 80 | **129** |
| 46 | slackwater-lattice | 0 | 0 | 0 | 127 | **127** |
| 47 | plato-fflearning | 0 | 0 | 0 | 123 | **123** |
| 48 | holodeck | 0 | 0 | 0 | 123 | **123** |
| 49 | cns-echo | 0 | 0 | 0 | 117 | **117** |
| 50 | symphony-claude | 0 | 0 | 0 | 116 | **116** |
| 51 | cns-monitor | 0 | 0 | 0 | 116 | **116** |
| 52 | study-cocapn-health | 0 | 0 | 0 | 113 | **113** |
| 53 | forgemaster-shell | 0 | 0 | 0 | 112 | **112** |
| 54 | OpenRoom | 0 | 7 | 111 | 0 | **111** |
| 55 | ai-writings-vectorizer | 0 | 0 | 0 | 101 | **101** |
| 56 | sensor-bridge | 0 | 0 | 0 | 100 | **100** |
| 57 | songforge | 0 | 0 | 0 | 99 | **99** |
| 58 | roblox-audio-suite | 0 | 0 | 0 | 94 | **94** |
| 59 | hermes-nmi | 88 | 0 | 0 | 0 | **88** |
| 60 | image-distillation-loop | 0 | 0 | 0 | 87 | **87** |
| 61 | study-lau-conservation-experiment | 85 | 0 | 0 | 0 | **85** |
| 62 | starship-jetsonclaw1 | 0 | 0 | 0 | 84 | **84** |
| 63 | lucid-dreamer | 0 | 0 | 0 | 83 | **83** |
| 64 | roblox-craftmind-agents | 0 | 0 | 0 | 82 | **82** |
| 65 | study-claude-code | 0 | 0 | 0 | 78 | **78** |
| 66 | wesley-cns-adapter | 0 | 0 | 0 | 77 | **77** |
| 67 | the-tap | 48 | 0 | 0 | 28 | **76** |
| 68 | fleet-wiki | 0 | 0 | 0 | 75 | **75** |
| 69 | terrain | 0 | 0 | 0 | 74 | **74** |
| 70 | roblox-world-scanner | 0 | 0 | 0 | 72 | **72** |
| 71 | git-native-mud | 0 | 0 | 0 | 72 | **72** |
| 72 | study-murmur-agent | 0 | 1 | 70 | 0 | **70** |
| 73 | slackwater-rust | 0 | 0 | 0 | 68 | **68** |
| 74 | ternary-tenforward | 66 | 0 | 0 | 0 | **66** |
| 75 | study-vessel-prototype | 0 | 0 | 0 | 64 | **64** |
| 76 | study-flux-runtime | 0 | 0 | 0 | 64 | **64** |
| 77 | study-harness-exp | 0 | 0 | 0 | 62 | **62** |
| 78 | study-fleet-vessel | 0 | 0 | 0 | 61 | **61** |
| 79 | roblox-build-animator | 0 | 0 | 0 | 57 | **57** |
| 80 | study-superz | 0 | 0 | 0 | 55 | **55** |
| 81 | playtest-journals | 0 | 0 | 0 | 54 | **54** |
| 82 | lucineer-vector | 0 | 2 | 53 | 0 | **53** |
| 83 | study-experiments | 0 | 0 | 0 | 52 | **52** |
| 84 | plato-spatial | 0 | 0 | 0 | 50 | **50** |
| 85 | study-vessel-constellation | 48 | 0 | 0 | 0 | **48** |
| 86 | si-main | 0 | 0 | 0 | 47 | **47** |
| 87 | voxel-logic | 0 | 1 | 45 | 0 | **45** |
| 88 | study-constraint-theory-math | 0 | 0 | 0 | 43 | **43** |
| 89 | gossip-ping | 43 | 0 | 0 | 0 | **43** |
| 90 | dual-band-guard | 40 | 0 | 0 | 0 | **40** |
| 91 | study-air | 0 | 0 | 0 | 39 | **39** |
| 92 | study-pincher | 12 | 0 | 0 | 26 | **38** |
| 93 | study-fleet-liaison | 0 | 0 | 0 | 37 | **37** |
| 94 | plato-forge-daemon | 0 | 0 | 0 | 37 | **37** |
| 95 | lucineer-memory | 0 | 1 | 37 | 0 | **37** |
| 96 | platonic-randomness | 0 | 1 | 36 | 0 | **36** |
| 97 | ai-writings | 0 | 0 | 0 | 33 | **33** |
| 98 | study-tripartite-consensus | 0 | 2 | 32 | 0 | **32** |
| 99 | bare-metal-plato | 0 | 0 | 0 | 32 | **32** |
| 100 | study-zeroclaw-arena | 0 | 0 | 0 | 30 | **30** |
| 101 | log-tensor | 0 | 0 | 0 | 30 | **30** |
| 102 | study-fleet-yaw | 28 | 0 | 0 | 0 | **28** |
| 103 | study-ecosystem | 0 | 0 | 0 | 28 | **28** |
| 104 | study-fleet-murmur-worker | 0 | 1 | 27 | 0 | **27** |
| 105 | confidence-cascade | 0 | 1 | 27 | 0 | **27** |
| 106 | scummvm-gui-design | 0 | 1 | 25 | 0 | **25** |
| 107 | study-murmur | 0 | 1 | 23 | 0 | **23** |
| 108 | stigmergy | 0 | 1 | 23 | 0 | **23** |
| 109 | study-lucid-tutor | 21 | 0 | 0 | 0 | **21** |
| 110 | mud2scummvm | 21 | 0 | 0 | 0 | **21** |
| 111 | flow-state | 0 | 0 | 0 | 21 | **21** |
| 112 | study-murmur-protocol-v2 | 20 | 0 | 0 | 0 | **20** |
| 113 | study-luciddreamer-ai | 0 | 1 | 20 | 0 | **20** |
| 114 | study-fleet-exp | 0 | 0 | 0 | 20 | **20** |
| 115 | study-fiedler-universal | 0 | 0 | 0 | 20 | **20** |
| 116 | study-cocapn | 20 | 0 | 0 | 0 | **20** |
| 117 | luciddreamer-ai | 0 | 1 | 20 | 0 | **20** |
| 118 | ec2mud | 0 | 1 | 18 | 0 | **18** |
| 119 | study-ternary-exp | 17 | 0 | 0 | 0 | **17** |
| 120 | study-si-bench | 17 | 0 | 0 | 0 | **17** |
| 121 | study-constraint-papers | 0 | 0 | 0 | 16 | **16** |
| 122 | researchlocal/ActiveLog-TechnicalRepo | 0 | 0 | 0 | 16 | **16** |
| 123 | study-vessel-template | 0 | 0 | 0 | 13 | **13** |
| 124 | study-si-agent | 0 | 1 | 12 | 0 | **12** |
| 125 | study-luciddreamer-agent | 0 | 0 | 0 | 11 | **11** |
| 126 | study-oxide-flux-runtime | 8 | 0 | 0 | 0 | **8** |
| 127 | study-cudaclaw-bridge | 8 | 0 | 0 | 0 | **8** |
| 128 | study-oxide-pipeline | 7 | 0 | 0 | 0 | **7** |
| 129 | study-signal-chain | 5 | 0 | 0 | 0 | **5** |
| 130 | study-ensign | 0 | 0 | 0 | 5 | **5** |
| 131 | study-plato-ship | 2 | 0 | 0 | 0 | **2** |

### Repos with 0 Tests

| # | Repo | Rust | TS Files | TS Calls | Python | Total |
|---|------|-----:|------:|------:|------:|------:|
| 1 | wesley-journal | 0 | 0 | 0 | 0 | 0 |
| 2 | vibe-world | 0 | 0 | 0 | 0 | 0 |
| 3 | vessel-room-navigator | 0 | 0 | 0 | 0 | 0 |
| 4 | the-listeners-ear | 0 | 0 | 0 | 0 | 0 |
| 5 | tap-frontend | 0 | 0 | 0 | 0 | 0 |
| 6 | superinstance-design-system | 0 | 0 | 0 | 0 | 0 |
| 7 | study-zero-crypto | 0 | 0 | 0 | 0 | 0 |
| 8 | study-weird-roblox-ai | 0 | 0 | 0 | 0 | 0 |
| 9 | study-vessel-tech | 0 | 0 | 0 | 0 | 0 |
| 10 | study-smartcomponent | 0 | 0 | 0 | 0 | 0 |
| 11 | study-sheaf-constraint-synthesis | 0 | 0 | 0 | 0 | 0 |
| 12 | study-papers | 0 | 0 | 0 | 0 | 0 |
| 13 | study-negative-knowledge | 0 | 0 | 0 | 0 | 0 |
| 14 | study-nebula-docs | 0 | 0 | 0 | 0 | 0 |
| 15 | study-navigator | 0 | 0 | 0 | 0 | 0 |
| 16 | study-multi-model-adversarial-testing | 0 | 0 | 0 | 0 | 0 |
| 17 | study-luciddreamer-vision | 0 | 0 | 0 | 0 | 0 |
| 18 | study-luciddreamer-os | 0 | 0 | 0 | 0 | 0 |
| 19 | study-luciddreamer-ai-pages | 0 | 0 | 0 | 0 | 0 |
| 20 | study-lucid-tutor-c | 0 | 0 | 0 | 0 | 0 |
| 21 | study-intent-directed-compilation | 0 | 0 | 0 | 0 | 0 |
| 22 | study-flux-papers | 0 | 0 | 0 | 0 | 0 |
| 23 | study-flagship | 0 | 0 | 0 | 0 | 0 |
| 24 | scummvm-prototype | 0 | 0 | 0 | 0 | 0 |
| 25 | roblox-testkit | 0 | 0 | 0 | 0 | 0 |
| 26 | roblox-filtergate | 0 | 0 | 0 | 0 | 0 |
| 27 | roblox-builder-kit | 0 | 0 | 0 | 0 | 0 |
| 28 | roblox-bond-system | 0 | 0 | 0 | 0 | 0 |
| 29 | roblox-beatclock | 0 | 0 | 0 | 0 | 0 |
| 30 | researchlocal/activelog-claude | 0 | 0 | 0 | 0 | 0 |
| 31 | researchlocal/activelog-backend | 0 | 0 | 0 | 0 | 0 |
| 32 | platonic-creative-suite | 0 | 0 | 0 | 0 | 0 |
| 33 | plato-vessel-core | 0 | 0 | 0 | 0 | 0 |
| 34 | lucineer-roblox | 0 | 0 | 0 | 0 | 0 |
| 35 | lucineer-com-site | 0 | 0 | 0 | 0 | 0 |
| 36 | lucid-dreamer-interactive | 0 | 0 | 0 | 0 | 0 |
| 37 | fleet-tts | 0 | 0 | 0 | 0 | 0 |
| 38 | fleet-dashboard | 0 | 0 | 0 | 0 | 0 |
| 39 | fishinglog-ai-site | 0 | 0 | 0 | 0 | 0 |
| 40 | crab-trap-web | 0 | 0 | 0 | 0 | 0 |
| 41 | cocapn-dashboard | 0 | 0 | 0 | 0 | 0 |
| 42 | activelog-ai-site | 0 | 0 | 0 | 0 | 0 |
| 43 | activeledger-ai-site | 0 | 0 | 0 | 0 | 0 |
| 44 | VaaS | 0 | 0 | 0 | 0 | 0 |
| 45 | INTEGRATION_GUIDES | 0 | 0 | 0 | 0 | 0 |
| 46 | DigitalTwin-RobotStudio-SmartComponent | 0 | 0 | 0 | 0 | 0 |

## Methodology

- **Rust:** Counted `#[test]` attributes in `.rs` files under `src/` and `tests/`
- **TypeScript:** Counted `.test.ts` and `.test.tsx` files (excluding `node_modules`), plus `it()` and `test()` calls within those files
- **Python:** Counted lines matching `def test_` in `.py` files (excluding `node_modules` and `.git/`)
- All counts are approximate — grep-based, not parser-based
- Repos under `researchlocal/` are listed with their parent path for clarity

## Observations

- **ACE-Step-1.5** dominates with 67,377 Python test functions — likely a vendored ML model repo
- **covers** has 51,945 Python tests — another large suite
- **study-si-papers** has the most TypeScript test infrastructure (185 files, 6,362 test calls) plus 853 Python tests
- **study-cudaclaw** and **study-cudaclaw-main** tie at 352 Rust tests each (likely mirrored/forked)
- **eisenstein** leads pure-Rust repos with 206 tests
- 46 repos have zero tests — candidates for test coverage improvement
