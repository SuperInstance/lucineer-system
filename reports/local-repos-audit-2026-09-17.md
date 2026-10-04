# Local Repos Audit — 2026-09-17

**Scope:** all dirs one level under `/home/eileen/projects/` (402) + `~/ai-writings`, `~/plainsong`, `~/plainsong-mcp`, `~/the-tap`, `~/fleet-static-host` (5) = **407 dirs**.
**Method:** read-only — `git status --porcelain`, `git rev-parse @{u}`, `git rev-list --count @{u}..HEAD`, `git log -1 --format=%cs`, `du -sh --exclude=node_modules --exclude=.git`. Nothing modified, committed, pushed, or deleted.

**Totals:** 395 git repos, 12 non-git dirs. Remotes: 383 SuperInstance, 5 other, 7 none.

| repo | remote? | dirty files | ahead commits | last commit | size |
|---|---|---|---|---|---|
| ai-writings | other | - | - | - | - |
| fleet-static-host | SuperInstance | 0 | 0 | 2026-09-03 | 47M |
| plainsong | SuperInstance | 0 | 0 | 2026-08-18 | 40M |
| plainsong-mcp | SuperInstance | 0 | 0 | 2026-08-18 | 280K |
| projects/A2A-native-notebookLM | SuperInstance | 0 | 0 | 2026-08-30 | 8.6M |
| projects/ACE-Step-1.5 | SuperInstance | 0 | 0 | 2026-09-02 | 11G |
| projects/AVA-AI-Voice-Agent-for-Asterisk | SuperInstance | 0 | 0 | 2026-08-27 | 15M |
| projects/AgentCompute | SuperInstance | 0 | 0 | 2026-08-29 | 29M |
| projects/AgentGossip | SuperInstance | 0 | 0 | 2026-09-02 | 216K |
| projects/CognitiveEngine | SuperInstance | 0 | 0 | 2026-08-30 | 1.2M |
| projects/DigitalTwin-RobotStudio-SmartComponent | SuperInstance | 0 | 0 | 2026-08-07 | 116K |
| projects/EXOCORTEX | SuperInstance | 0 | 0 | 2026-08-20 | 2.3M |
| projects/INTEGRATION_GUIDES | SuperInstance | 0 | 0 | 2026-08-20 | 152K |
| projects/MerkleMesh | SuperInstance | 0 | 0 | 2026-08-30 | 296K |
| projects/OpenConstruct | SuperInstance | 0 | 0 | 2026-08-30 | 6.5G |
| projects/OpenRoom | SuperInstance | 0 | 0 | 2026-08-19 | 9.2M |
| projects/PersonalLog | SuperInstance | 0 | 0 | 2026-08-30 | 39M |
| projects/Scrapcraft | SuperInstance | 0 | 0 | 2026-08-28 | 5.8M |
| projects/Scrapcraft-comp-claude | other | 0 | no upstream | 2026-08-26 | 5.0M |
| projects/Scrapcraft-comp-kimi | other | 0 | 0 | 2026-08-30 | 5.0M |
| projects/Scrapcraft-comp-opencode | other | 0 | 0 | 2026-08-30 | 5.0M |
| projects/SmartCRDT | SuperInstance | 0 | 0 | 2026-08-26 | 39M |
| projects/SuperInstance-papers | SuperInstance | 0 | 0 | 2026-08-26 | 109M |
| projects/VaaS | SuperInstance | 0 | 0 | 2026-08-24 | 1.9M |
| projects/ability-transfer | SuperInstance | 0 | 0 | 2026-08-21 | 736K |
| projects/active-probe | SuperInstance | 0 | 0 | 2026-08-26 | 204K |
| projects/activeledger-ai-site | SuperInstance | 0 | 0 | 2026-08-12 | 512K |
| projects/activelog-agent | SuperInstance | 0 | no upstream | 2026-08-30 | 488K |
| projects/activelog-ai-pages | SuperInstance | 0 | 0 | 2026-08-21 | 436K |
| projects/activelog-ai-site | SuperInstance | 0 | 0 | 2026-08-12 | 520K |
| projects/actualization-harbor | SuperInstance | 0 | no upstream | 2026-08-23 | 544K |
| projects/adaptive-plato-early-version | SuperInstance | 0 | 0 | 2026-08-21 | 176K |
| projects/adinkra-math-pypi | SuperInstance | 0 | no upstream | 2026-08-31 | 396K |
| projects/agent-writings-archive | SuperInstance | 0 | 0 | 2026-08-22 | 972K |
| projects/ai-writings | SuperInstance | 9 | 0 | 2026-09-04 | 3.1G |
| projects/ai-writings-vectorizer | SuperInstance | 0 | 0 | 2026-08-16 | 135M |
| projects/asset-ranch | SuperInstance | 0 | 0 | 2026-08-26 | 4.8M |
| projects/bare-metal-plato | SuperInstance | 0 | 0 | 2026-09-02 | 404K |
| projects/base60-lattice | SuperInstance | 0 | 0 | 2026-08-20 | 1.7M |
| projects/batten-spline | SuperInstance | 0 | 0 | 2026-08-17 | 74M |
| projects/captain-console | SuperInstance | 0 | 0 | 2026-08-26 | 176K |
| projects/casting-call | SuperInstance | 0 | 0 | 2026-08-23 | 984K |
| projects/cell-cascade | SuperInstance | 0 | 0 | 2026-08-26 | 51M |
| projects/cns-bridge | SuperInstance | 0 | 0 | 2026-08-21 | 3.2M |
| projects/cns-echo | SuperInstance | 0 | 0 | 2026-08-22 | 1.7M |
| projects/cns-monitor | SuperInstance | 0 | 0 | 2026-08-19 | 8.7M |
| projects/cocapn-dashboard | SuperInstance | 0 | 0 | 2026-08-21 | 160K |
| projects/codespace-edge-rd | SuperInstance | 0 | 0 | 2026-08-21 | 80K |
| projects/collective-unconscious | SuperInstance | 0 | 0 | 2026-08-21 | 1.1M |
| projects/compaction-teacher | SuperInstance | 0 | 0 | 2026-08-22 | 2.1M |
| projects/confidence-cascade | SuperInstance | 0 | 0 | 2026-08-20 | 1.6M |
| projects/constraint-theory-py | SuperInstance | 0 | 0 | 2026-08-21 | 224K |
| projects/covers | SuperInstance | 0 | 0 | 2026-08-20 | 5.4G |
| projects/crab-trap-web | SuperInstance | 0 | 0 | 2026-08-30 | 260K |
| projects/crab-traps | SuperInstance | 0 | 0 | 2026-09-04 | 24M |
| projects/deckboss-site | none | 0 | no upstream | 2026-08-30 | 112K |
| projects/dsh-assessment | SuperInstance | 0 | 0 | 2026-08-23 | 32K |
| projects/dual-band-guard | SuperInstance | 0 | 0 | 2026-08-20 | 74M |
| projects/ec2mud | SuperInstance | 0 | 0 | 2026-09-04 | 896K |
| projects/edge-compiler | SuperInstance | 0 | 0 | 2026-08-21 | 200K |
| projects/edge-native-paper | SuperInstance | 0 | 0 | 2026-04-13 | 16K |
| projects/edge-relay-agent | SuperInstance | 0 | 0 | 2026-08-21 | 188K |
| projects/eisenstein | SuperInstance | 0 | 0 | 2026-09-03 | 150M |
| projects/elephant | SuperInstance | 0 | 0 | 2026-09-04 | 139M |
| projects/elephant-sim-worker | SuperInstance | 0 | 0 | 2026-08-20 | 228K |
| projects/emergence-engine | SuperInstance | 0 | 0 | 2026-08-20 | 1.8M |
| projects/engine-ensign | SuperInstance | 0 | 0 | 2026-08-18 | 2.7M |
| projects/exocortex-core | SuperInstance | 0 | 0 | 2026-08-18 | 2.4M |
| projects/experiment-wheel | SuperInstance | 2 | 0 | 2026-08-31 | 2.7M |
| projects/fishinglog-ai-site | SuperInstance | 0 | 0 | 2026-08-12 | 536K |
| projects/fleet-agent-early-version | SuperInstance | 0 | 0 | 2026-08-21 | 244K |
| projects/fleet-audio | SuperInstance | 0 | 0 | 2026-08-18 | 988K |
| projects/fleet-bottles | SuperInstance | 0 | 0 | 2026-08-28 | 4.0M |
| projects/fleet-cns-v3 | SuperInstance | 0 | 0 | 2026-08-21 | 352K |
| projects/fleet-conductor | SuperInstance | 0 | 0 | 2026-08-23 | 56M |
| projects/fleet-config | SuperInstance | 0 | no upstream | 2026-08-30 | 308K |
| projects/fleet-connections | SuperInstance | 0 | 0 | 2026-08-20 | 544K |
| projects/fleet-constraint | SuperInstance | 0 | no upstream | 2026-08-30 | 352K |
| projects/fleet-containers | SuperInstance | 0 | 0 | 2026-08-30 | 264K |
| projects/fleet-coordinate-js | SuperInstance | 0 | no upstream | 2026-08-21 | 164K |
| projects/fleet-dashboard | SuperInstance | 0 | 0 | 2026-08-31 | 432K |
| projects/fleet-discovery | SuperInstance | 0 | 0 | 2026-08-30 | 164K |
| projects/fleet-embed | SuperInstance | 0 | 0 | 2026-08-21 | 256K |
| projects/fleet-ensemble | SuperInstance | 0 | 0 | 2026-08-21 | 492K |
| projects/fleet-envelope | SuperInstance | 0 | 0 | 2026-08-23 | 376K |
| projects/fleet-functions | SuperInstance | 0 | 0 | 2026-08-25 | 268K |
| projects/fleet-gateway | SuperInstance | 0 | 1 | 2026-08-30 | 2.7G |
| projects/fleet-github-app | SuperInstance | 0 | 0 | 2026-08-21 | 68K |
| projects/fleet-homunculus | SuperInstance | 0 | 0 | 2026-08-30 | 344K |
| projects/fleet-inventory | SuperInstance | 0 | 0 | 2026-08-26 | 332K |
| projects/fleet-jepa-midi | SuperInstance | 0 | 0 | 2026-08-21 | 22M |
| projects/fleet-memory | SuperInstance | 0 | 0 | 2026-08-21 | 812K |
| projects/fleet-midi | SuperInstance | 0 | 0 | 2026-08-21 | 152K |
| projects/fleet-mirror | other | - | - | - | - |
| projects/fleet-pipeline | SuperInstance | 0 | 0 | 2026-08-13 | 360K |
| projects/fleet-radio | SuperInstance | 4 | 0 | 2026-09-02 | 1.5M |
| projects/fleet-reactions | other | - | - | - | - |
| projects/fleet-rooms | SuperInstance | 0 | 0 | 2026-08-20 | 679M |
| projects/fleet-scribe | SuperInstance | 0 | 0 | 2026-08-26 | 580K |
| projects/fleet-static-host | SuperInstance | 0 | 0 | 2026-09-03 | 76M |
| projects/fleet-stitch | SuperInstance | 0 | 0 | 2026-07-12 | 120K |
| projects/fleet-tts | SuperInstance | 0 | 0 | 2026-08-13 | 128K |
| projects/fleet-twin | SuperInstance | 0 | 10 | 2026-08-30 | 75M |
| projects/fleet-wiki | SuperInstance | 0 | 0 | 2026-08-20 | 392K |
| projects/flow-state | SuperInstance | 0 | 0 | 2026-08-20 | 536K |
| projects/flux-cross-assembler | SuperInstance | 0 | 0 | 2026-08-21 | 68K |
| projects/flux-dsh-plugin | SuperInstance | 0 | 0 | 2026-08-26 | 476K |
| projects/flux-genome-rs | SuperInstance | 0 | 0 | 2026-09-03 | 182M |
| projects/flux-runtime | SuperInstance | 0 | 0 | 2026-08-23 | 24M |
| projects/flux-vm | SuperInstance | 0 | 0 | 2026-08-26 | 2.0G |
| projects/fm-experiments | SuperInstance | 0 | 0 | 2026-08-21 | 102M |
| projects/forgemaster | SuperInstance | 0 | 0 | 2026-08-25 | 146M |
| projects/forgemaster-shell | SuperInstance | 0 | 0 | 2026-08-30 | 380K |
| projects/git-native-mud | SuperInstance | 0 | 0 | 2026-08-29 | 636K |
| projects/gossip-ping | SuperInstance | 0 | 0 | 2026-08-20 | 284M |
| projects/hermes-cloudflare | SuperInstance | 0 | 0 | 2026-08-20 | 844K |
| projects/hermes-construct | SuperInstance | 0 | 0 | 2026-08-18 | 93M |
| projects/hermes-nmi | SuperInstance | 0 | 0 | 2026-08-20 | 399M |
| projects/hermes-ob1-core | SuperInstance | 0 | 0 | 2026-08-12 | 64M |
| projects/hermes-perception | SuperInstance | 0 | 0 | 2026-08-20 | 364K |
| projects/hermes-reader | SuperInstance | 0 | 0 | 2026-08-23 | 612K |
| projects/holodeck | SuperInstance | 0 | 0 | 2026-08-12 | 4.1M |
| projects/holodeck-c | SuperInstance | 0 | 0 | 2026-08-21 | 240K |
| projects/ideation-games | SuperInstance | 0 | 0 | 2026-08-20 | 404K |
| projects/image-distillation-loop | SuperInstance | 0 | 0 | 2026-08-12 | 588K |
| projects/lingbot-map | SuperInstance | 0 | 0 | 2026-08-12 | 324M |
| projects/log-tensor | SuperInstance | 0 | 0 | 2026-08-08 | 1.9M |
| projects/lucid | SuperInstance | 0 | no upstream | 2026-08-30 | 1.1M |
| projects/lucid-dreamer | SuperInstance | 0 | 0 | 2026-08-12 | 588K |
| projects/lucid-dreamer-interactive | SuperInstance | 0 | 0 | 2026-08-12 | 120K |
| projects/luciddreamer-ai | SuperInstance | 0 | 0 | 2026-08-22 | 257M |
| projects/luciddreamer-content | SuperInstance | 0 | 0 | 2026-08-13 | 186M |
| projects/luciddreamer-prototype | SuperInstance | 0 | 0 | 2026-08-21 | 45M |
| projects/luciddreamer-research | SuperInstance | 0 | 0 | 2026-08-20 | 2.6M |
| projects/lucineer-brain | SuperInstance | 0 | 0 | 2026-08-20 | 1.2M |
| projects/lucineer-com-site | SuperInstance | 0 | 0 | 2026-08-12 | 86M |
| projects/lucineer-creative | SuperInstance | 0 | 0 | 2026-08-20 | 576K |
| projects/lucineer-memory | SuperInstance | 0 | 0 | 2026-08-20 | 368K |
| projects/lucineer-relay | SuperInstance | 0 | 0 | 2026-09-03 | 2.2M |
| projects/lucineer-roblox | SuperInstance | 0 | 0 | 2026-08-20 | 2.2M |
| projects/lucineer-system | SuperInstance | 0 | 0 | 2026-09-03 | 86M |
| projects/lucineer-system-readme-pass | SuperInstance | 0 | 0 | 2026-08-27 | 86M |
| projects/lucineer-vector | SuperInstance | 0 | 0 | 2026-08-20 | 968K |
| projects/lucineer-worker | SuperInstance | 0 | 0 | 2026-08-20 | 5.8M |
| projects/magda-core-study | other | 0 | 1 | 2026-08-30 | 180M |
| projects/mentis-superinstance | SuperInstance | 0 | 0 | 2026-08-21 | 1.4M |
| projects/mist-art-qc | other | - | - | - | - |
| projects/mist-game | SuperInstance | 0 | 0 | 2026-08-26 | 239M |
| projects/mist-lab | SuperInstance | 0 | 0 | 2026-08-22 | 156K |
| projects/mist-lab-work | SuperInstance | 0 | 0 | 2026-08-23 | 156M |
| projects/mist-quilt | SuperInstance | 0 | 0 | 2026-08-22 | 188K |
| projects/mist-voice | SuperInstance | 0 | 0 | 2026-08-22 | 120K |
| projects/mud-arena | SuperInstance | 0 | 0 | 2026-08-21 | 1.8M |
| projects/mud-engine | SuperInstance | 0 | 0 | 2026-08-20 | 2.3M |
| projects/mud2scummvm | SuperInstance | 0 | 0 | 2026-09-02 | 37M |
| projects/murmur-agent | SuperInstance | 0 | 0 | 2026-08-27 | 488K |
| projects/music | other | - | - | - | - |
| projects/musician-soul | SuperInstance | 0 | 0 | 2026-08-13 | 44M |
| projects/nexus-edge-runtime | SuperInstance | 0 | 0 | 2026-08-21 | 248K |
| projects/nmea-quilt-cell | SuperInstance | 0 | 0 | 2026-09-03 | 5.4M |
| projects/officers-quarters | SuperInstance | 0 | 0 | 2026-08-21 | 2.4M |
| projects/openplan3d-twin-work | SuperInstance | 0 | 0 | 2026-08-27 | 31M |
| projects/openrooms | SuperInstance | 0 | 0 | 2026-08-07 | 408M |
| projects/operational-fiction | SuperInstance | 0 | no upstream | 2026-08-30 | 596K |
| projects/plainsong | SuperInstance | 0 | 0 | 2026-08-25 | 53M |
| projects/plainsong-mcp | SuperInstance | 0 | 0 | 2026-08-25 | 179M |
| projects/plainsong-worker | SuperInstance | 0 | 0 | 2026-08-21 | 448K |
| projects/plato-engine-block-c | SuperInstance | 0 | 0 | 2026-08-21 | 216K |
| projects/plato-fflearning | SuperInstance | 0 | 0 | 2026-08-12 | 320K |
| projects/plato-forge-daemon | SuperInstance | 0 | 0 | 2026-08-12 | 252K |
| projects/plato-music-sync | SuperInstance | 0 | 0 | 2026-08-13 | 49M |
| projects/plato-perception | SuperInstance | 0 | 0 | 2026-08-18 | 92M |
| projects/plato-portal | SuperInstance | 0 | 0 | 2026-08-21 | 8.2M |
| projects/plato-prediction | SuperInstance | 0 | 0 | 2026-08-18 | 91M |
| projects/plato-spatial | SuperInstance | 0 | 0 | 2026-08-12 | 328K |
| projects/plato-types | SuperInstance | 0 | 0 | 2026-08-21 | 60K |
| projects/plato-vessel-core | SuperInstance | 0 | 0 | 2026-08-21 | 392K |
| projects/plato-vision-jepa | SuperInstance | 0 | 0 | 2026-08-20 | 88M |
| projects/platonic-creative-suite | SuperInstance | 0 | 0 | 2026-08-21 | 128K |
| projects/platonic-randomness | SuperInstance | 0 | 0 | 2026-08-12 | 316K |
| projects/platos-shell | SuperInstance | 0 | 0 | 2026-08-20 | 11M |
| projects/platos-shell-ide | SuperInstance | 0 | 0 | 2026-08-20 | 600K |
| projects/playtest-journals | SuperInstance | 0 | 0 | 2026-08-12 | 372K |
| projects/polyformalism | SuperInstance | 0 | 0 | 2026-07-12 | 5.4M |
| projects/polyformalism-thinking | SuperInstance | 0 | 0 | 2026-05-09 | 12M |
| projects/quicunnel | SuperInstance | 0 | 0 | 2026-08-21 | 176K |
| projects/quilt | SuperInstance | 0 | no upstream | 2026-08-31 | 14M |
| projects/quilt-agent | SuperInstance | 0 | 0 | 2026-08-20 | 2.3M |
| projects/quilt-ai | SuperInstance | 0 | 0 | 2026-08-26 | 428K |
| projects/quilt-canvas | none | 0 | no upstream | 2026-08-28 | 76K |
| projects/quilt-cell-bridges | SuperInstance | 0 | 0 | 2026-08-20 | 2.1M |
| projects/quilt-cellular-arch | SuperInstance | 0 | 0 | 2026-08-31 | 1.9M |
| projects/quilt-cloudflare | SuperInstance | 0 | 0 | 2026-09-02 | 3.5M |
| projects/quilt-conformance | SuperInstance | 0 | 0 | 2026-08-25 | 14M |
| projects/quilt-cosim-wt | SuperInstance | 0 | 0 | 2026-08-31 | 59M |
| projects/quilt-cuda | SuperInstance | 0 | 0 | 2026-08-27 | 296K |
| projects/quilt-deck | none | 0 | no upstream | 2026-09-04 | 1.8M |
| projects/quilt-dpcpp | none | 0 | no upstream | no-commits | 4.0K |
| projects/quilt-elf | SuperInstance | 0 | 0 | 2026-08-20 | 2.9M |
| projects/quilt-engine-ports | SuperInstance | 0 | 0 | 2026-08-27 | 180K |
| projects/quilt-esp32 | SuperInstance | 0 | 0 | 2026-08-29 | 56M |
| projects/quilt-evolve | SuperInstance | 0 | 0 | 2026-08-20 | 6.2M |
| projects/quilt-fleet | SuperInstance | 0 | 0 | 2026-08-20 | 3.1M |
| projects/quilt-geometry | SuperInstance | 0 | 0 | 2026-08-29 | 892K |
| projects/quilt-id | SuperInstance | 0 | 0 | 2026-08-22 | 20K |
| projects/quilt-k3s | SuperInstance | 0 | 0 | 2026-08-30 | 3.0M |
| projects/quilt-live | SuperInstance | 0 | 0 | 2026-08-20 | 2.7M |
| projects/quilt-llm-worker | SuperInstance | 0 | 0 | 2026-08-20 | 80K |
| projects/quilt-llvm | SuperInstance | 1 | no upstream | 2026-08-31 | 743M |
| projects/quilt-llvm-wt-cocapn | SuperInstance | 0 | 0 | 2026-08-30 | 274M |
| projects/quilt-llvm-wt-gacorpus | SuperInstance | 0 | 0 | 2026-08-30 | 195M |
| projects/quilt-llvm-wt-merkle | SuperInstance | 0 | 0 | 2026-08-30 | 273M |
| projects/quilt-llvm-wt-mutants | SuperInstance | 0 | 0 | 2026-08-30 | 177M |
| projects/quilt-llvm-wt-r3lane1 | SuperInstance | 0 | no upstream | 2026-08-31 | 500M |
| projects/quilt-llvm-wt-r3lane3 | SuperInstance | 0 | no upstream | 2026-08-31 | 514M |
| projects/quilt-llvm-wt-r4lane1 | SuperInstance | 2 | no upstream | 2026-08-31 | 246M |
| projects/quilt-llvm-wt-region | SuperInstance | 0 | 0 | 2026-08-30 | 540M |
| projects/quilt-llvm-wt-rivalry | SuperInstance | 0 | no upstream | 2026-08-31 | 1.7M |
| projects/quilt-llvm-wt-shape | SuperInstance | 0 | 1 | 2026-08-30 | 124M |
| projects/quilt-llvm-wt-tombstone | SuperInstance | 0 | 0 | 2026-08-30 | 226M |
| projects/quilt-llvm-wt-usetables | SuperInstance | 0 | 0 | 2026-08-30 | 331M |
| projects/quilt-mhs | SuperInstance | 0 | 0 | 2026-08-30 | 287M |
| projects/quilt-mhs-playtest | SuperInstance | 0 | 1 | 2026-08-30 | 761M |
| projects/quilt-nomad | SuperInstance | 0 | 0 | 2026-08-26 | 3.0M |
| projects/quilt-pincher | SuperInstance | 0 | 0 | 2026-08-20 | 2.7M |
| projects/quilt-r27 | other | - | - | - | - |
| projects/quilt-rag | SuperInstance | 0 | 0 | 2026-08-20 | 7.2M |
| projects/quilt-rust | SuperInstance | 1 | 0 | 2026-08-29 | 13G |
| projects/quilt-rust-selfimprove | SuperInstance | 1 | no upstream | 2026-08-31 | 2.2G |
| projects/quilt-scratch | SuperInstance | 0 | 0 | 2026-08-30 | 5.6M |
| projects/quilt-scratch-debug | other | 0 | no upstream | 2026-08-30 | 204K |
| projects/quilt-swarm | SuperInstance | 0 | 0 | 2026-08-30 | 3.3M |
| projects/quilt-tournament | none | 30 | no upstream | 2026-09-04 | 629M |
| projects/quilt-verilog | SuperInstance | 5 | 3 | 2026-09-04 | 2.2G |
| projects/quilt-vision | SuperInstance | 0 | 0 | 2026-08-26 | 2.7M |
| projects/quilt-vm-c | SuperInstance | 0 | 0 | 2026-08-26 | 132K |
| projects/quilt-vm-haskell | SuperInstance | 0 | 0 | 2026-09-02 | 888K |
| projects/quilt-vm-rust | SuperInstance | 0 | 0 | 2026-08-26 | 17M |
| projects/quilt-vm-typescript | SuperInstance | 0 | 0 | 2026-09-02 | 124K |
| projects/quilt-vm-wasm | SuperInstance | 0 | 0 | 2026-08-26 | 164K |
| projects/quilt-wiki-2126 | SuperInstance | 0 | no upstream | 2026-08-31 | 388K |
| projects/qv-head | SuperInstance | 9 | no upstream | 2026-08-30 | 682M |
| projects/qvw-r27 | SuperInstance | 1 | no upstream | 2026-09-04 | 925M |
| projects/rd | SuperInstance | 18 | 0 | 2026-08-31 | 408K |
| projects/readme-art-drafts | other | - | - | - | - |
| projects/researchlocal | other | - | - | - | - |
| projects/researchlocal-backup | SuperInstance | 0 | 0 | 2026-08-21 | 140M |
| projects/roblox-audio-suite | SuperInstance | 0 | 0 | 2026-08-12 | 432K |
| projects/roblox-beatclock | SuperInstance | 0 | 0 | 2026-08-20 | 204K |
| projects/roblox-bond-system | SuperInstance | 0 | 0 | 2026-08-20 | 280K |
| projects/roblox-build-animator | SuperInstance | 0 | 0 | 2026-08-12 | 388K |
| projects/roblox-builder-kit | SuperInstance | 0 | 0 | 2026-08-12 | 312K |
| projects/roblox-craftmind-agents | SuperInstance | 0 | 0 | 2026-08-12 | 344K |
| projects/roblox-filtergate | SuperInstance | 0 | 0 | 2026-08-20 | 208K |
| projects/roblox-testkit | SuperInstance | 0 | 0 | 2026-08-12 | 236K |
| projects/roblox-world-scanner | SuperInstance | 0 | 0 | 2026-08-12 | 408K |
| projects/room-render | SuperInstance | 0 | 0 | 2026-08-20 | 208K |
| projects/saddle | SuperInstance | 0 | 0 | 2026-08-23 | 2.8M |
| projects/saddle-ft | SuperInstance | 0 | no upstream | 2026-08-23 | 1.8M |
| projects/saddle-v3 | SuperInstance | 0 | 0 | 2026-08-23 | 2.4M |
| projects/scrap-quilt | SuperInstance | 0 | 0 | 2026-08-28 | 9.7M |
| projects/scrap-spark | SuperInstance | 0 | 0 | 2026-08-28 | 512K |
| projects/scrap-voice | SuperInstance | 0 | 0 | 2026-08-22 | 188K |
| projects/scrapcraft-roblox | SuperInstance | 0 | 0 | 2026-08-23 | 1.3M |
| projects/scrapcraft-roblox-bible | SuperInstance | 0 | 0 | 2026-08-23 | 308K |
| projects/scrapcraft-world | SuperInstance | 0 | 0 | 2026-08-23 | 176K |
| projects/screen-agent | SuperInstance | 0 | 0 | 2026-08-20 | 96K |
| projects/scummvm-arcade | SuperInstance | 0 | 0 | 2026-08-20 | 892K |
| projects/scummvm-gui-design | SuperInstance | 0 | 0 | 2026-08-20 | 600K |
| projects/scummvm-prototype | SuperInstance | 0 | 0 | 2026-08-20 | 49M |
| projects/sd-fleet | other | - | - | - | - |
| projects/sensor-bridge | SuperInstance | 0 | 0 | 2026-08-21 | 720K |
| projects/shoal | SuperInstance | 0 | no upstream | 2026-08-24 | 412K |
| projects/shoal-opencode.archived-20260824-loses-tournament | other | - | - | - | - |
| projects/si-main.archived-20260820 | SuperInstance | 0 | no upstream | 2026-08-21 | 22M |
| projects/si-papers-new | SuperInstance | 0 | 0 | 2026-08-22 | 248K |
| projects/si-readme.archived-20260820 | SuperInstance | 0 | no upstream | 2026-08-30 | 22M |
| projects/signal-chain | SuperInstance | 0 | 0 | 2026-08-18 | 448K |
| projects/silence-map | SuperInstance | 0 | 0 | 2026-08-21 | 328K |
| projects/slackwater-art-spectrum | SuperInstance | 0 | 0 | 2026-08-12 | 62M |
| projects/slackwater-cognition | SuperInstance | 0 | 0 | 2026-08-12 | 2.3M |
| projects/slackwater-forge | SuperInstance | 0 | 0 | 2026-08-12 | 1.1M |
| projects/slackwater-harmony | SuperInstance | 0 | 0 | 2026-08-12 | 756K |
| projects/slackwater-lattice | SuperInstance | 0 | 0 | 2026-08-12 | 524K |
| projects/slackwater-perception | SuperInstance | 0 | 0 | 2026-08-12 | 876K |
| projects/slackwater-rust | SuperInstance | 0 | 0 | 2026-08-11 | 900K |
| projects/slackwater-tempo | SuperInstance | 0 | 0 | 2026-08-12 | 656K |
| projects/slackwater-tminus | SuperInstance | 0 | 0 | 2026-08-12 | 808K |
| projects/smp-notebook | SuperInstance | 0 | 0 | 2026-08-12 | 464K |
| projects/sonar-vision | SuperInstance | 0 | 0 | 2026-08-30 | 1.7M |
| projects/songforge | SuperInstance | 0 | 0 | 2026-08-25 | 4.5G |
| projects/spatial-registry | SuperInstance | 0 | 0 | 2026-08-20 | 228K |
| projects/starship-jetsonclaw1 | SuperInstance | 0 | 0 | 2026-08-12 | 416K |
| projects/stigmergy | SuperInstance | 0 | 0 | 2026-08-20 | 652K |
| projects/stock-screener | SuperInstance | 0 | 0 | 2026-08-27 | 42M |
| projects/study-air | SuperInstance | 0 | 0 | 2026-08-12 | 152K |
| projects/study-captain | SuperInstance | 0 | 0 | 2026-08-07 | 512K |
| projects/study-claude-code | SuperInstance | 0 | 0 | 2026-08-21 | 496K |
| projects/study-cocapn | SuperInstance | 0 | 0 | 2026-08-26 | 133M |
| projects/study-cocapn-health | SuperInstance | 0 | 0 | 2026-08-21 | 712K |
| projects/study-constraint-papers | SuperInstance | 0 | 0 | 2026-08-21 | 2.8M |
| projects/study-constraint-theory-math | SuperInstance | 0 | 0 | 2026-08-12 | 620K |
| projects/study-cudaclaw | SuperInstance | 0 | 0 | 2026-08-21 | 351M |
| projects/study-cudaclaw-bridge | SuperInstance | 0 | 0 | 2026-06-09 | 17M |
| projects/study-cudaclaw-main | SuperInstance | 0 | 0 | 2026-08-21 | 351M |
| projects/study-ecosystem | SuperInstance | 0 | 0 | 2026-08-12 | 992K |
| projects/study-ensign | SuperInstance | 0 | 0 | 2026-08-12 | 152K |
| projects/study-experiments | SuperInstance | 0 | 0 | 2026-08-08 | 7.9M |
| projects/study-fiedler-universal | SuperInstance | 0 | 0 | 2026-08-07 | 172K |
| projects/study-flagship | SuperInstance | 0 | 0 | 2026-08-12 | 1.3M |
| projects/study-fleet-exp | SuperInstance | 0 | 0 | 2026-08-12 | 160K |
| projects/study-fleet-liaison | SuperInstance | 0 | 0 | 2026-08-06 | 452K |
| projects/study-fleet-murmur-worker | SuperInstance | 0 | 0 | 2026-08-12 | 240K |
| projects/study-fleet-vessel | SuperInstance | 0 | 0 | 2026-08-07 | 272K |
| projects/study-fleet-yaw | SuperInstance | 0 | 0 | 2026-08-20 | 19M |
| projects/study-flux-lucid | SuperInstance | 0 | 0 | 2026-08-20 | 283M |
| projects/study-flux-papers | SuperInstance | 0 | 0 | 2026-05-08 | 488K |
| projects/study-flux-runtime | SuperInstance | 0 | 0 | 2026-08-06 | 328K |
| projects/study-harness-exp | SuperInstance | 0 | 0 | 2026-08-12 | 3.9M |
| projects/study-intent-directed-compilation | SuperInstance | 0 | 0 | 2026-08-13 | 340K |
| projects/study-lau-conservation-experiment | SuperInstance | 0 | 0 | 2026-08-07 | 212K |
| projects/study-lever-runner | SuperInstance | 0 | 0 | 2026-08-08 | 2.0M |
| projects/study-lucid-tutor | SuperInstance | 0 | 0 | 2026-07-12 | 98M |
| projects/study-lucid-tutor-c | SuperInstance | 0 | 0 | 2026-07-12 | 76K |
| projects/study-luciddreamer-agent | SuperInstance | 0 | 0 | 2026-08-21 | 204K |
| projects/study-luciddreamer-ai | SuperInstance | 0 | 0 | 2026-08-06 | 13M |
| projects/study-luciddreamer-ai-pages | SuperInstance | 0 | 0 | 2026-08-21 | 820K |
| projects/study-luciddreamer-os | SuperInstance | 0 | 0 | 2026-08-12 | 180K |
| projects/study-luciddreamer-vision | SuperInstance | 0 | 0 | 2026-08-20 | 40K |
| projects/study-multi-model-adversarial-testing | SuperInstance | 0 | 0 | 2026-07-12 | 360K |
| projects/study-murmur | SuperInstance | 0 | 0 | 2026-08-12 | 484K |
| projects/study-murmur-agent | SuperInstance | 0 | 0 | 2026-08-13 | 368K |
| projects/study-murmur-protocol-v2 | SuperInstance | 0 | 0 | 2026-07-12 | 94M |
| projects/study-navigator | SuperInstance | 0 | 0 | 2026-08-13 | 184K |
| projects/study-nebula-docs | SuperInstance | 0 | 0 | 2026-07-12 | 40K |
| projects/study-negative-knowledge | SuperInstance | 0 | 0 | 2026-08-13 | 168K |
| projects/study-oracle1 | SuperInstance | 0 | 0 | 2026-08-21 | 3.3M |
| projects/study-oxide-flux-runtime | SuperInstance | 0 | 0 | 2026-06-09 | 13M |
| projects/study-oxide-pipeline | SuperInstance | 0 | 0 | 2026-08-13 | 23M |
| projects/study-papers | SuperInstance | 0 | 0 | 2026-08-06 | 64K |
| projects/study-pincher | SuperInstance | 0 | 0 | 2026-08-21 | 4.9M |
| projects/study-plato-ship | SuperInstance | 0 | 0 | 2026-08-13 | 19M |
| projects/study-sheaf-constraint-synthesis | SuperInstance | 0 | 0 | 2026-08-04 | 108K |
| projects/study-si-agent | SuperInstance | 0 | 0 | 2026-08-24 | 384K |
| projects/study-si-bench | SuperInstance | 0 | 0 | 2026-07-12 | 90M |
| projects/study-si-papers | SuperInstance | 0 | 0 | 2026-08-20 | 106M |
| projects/study-signal-chain | SuperInstance | 0 | 0 | 2026-08-17 | 23M |
| projects/study-smartcomponent | SuperInstance | 0 | 0 | 2026-08-07 | 88K |
| projects/study-spreader-tool | SuperInstance | 0 | 0 | 2026-08-20 | 1.7M |
| projects/study-sunset-ecosystem | SuperInstance | 0 | 0 | 2026-08-21 | 139M |
| projects/study-superz | SuperInstance | 0 | 0 | 2026-08-20 | 5.1M |
| projects/study-ternary-exp | SuperInstance | 0 | 0 | 2026-08-07 | 20M |
| projects/study-tripartite-consensus | SuperInstance | 0 | 0 | 2026-08-12 | 248K |
| projects/study-vessel-constellation | SuperInstance | 0 | 0 | 2026-07-12 | 99M |
| projects/study-vessel-monitor | SuperInstance | 0 | 0 | 2026-08-12 | 113M |
| projects/study-vessel-prototype | SuperInstance | 0 | 0 | 2026-08-21 | 284K |
| projects/study-vessel-tech | SuperInstance | 0 | 0 | 2026-07-12 | 64K |
| projects/study-vessel-template | SuperInstance | 0 | 0 | 2026-05-16 | 100K |
| projects/study-weird-roblox-ai | SuperInstance | 0 | 0 | 2026-08-13 | 172K |
| projects/study-zero-crypto | SuperInstance | 0 | 0 | 2026-08-13 | 156K |
| projects/study-zeroclaw-arena | SuperInstance | 0 | 0 | 2026-07-12 | 3.0M |
| projects/sunset-ecosystem | SuperInstance | 0 | 0 | 2026-08-30 | 141M |
| projects/superinstance | SuperInstance | 0 | 0 | 2026-08-23 | 23M |
| projects/superinstance-ai | SuperInstance | 0 | 0 | 2026-08-30 | 668K |
| projects/superinstance-design-system | SuperInstance | 0 | 0 | 2026-08-22 | 364K |
| projects/superinstance-profile | SuperInstance | 0 | 0 | 2026-08-21 | 22M |
| projects/superinstance-website | SuperInstance | 0 | 0 | 2026-09-03 | 8.7M |
| projects/svelte-quilt | none | 0 | no upstream | 2026-08-30 | 200K |
| projects/sweep | none | 0 | no upstream | 2026-08-30 | 14M |
| projects/symphony-claude | SuperInstance | 0 | 0 | 2026-08-12 | 516K |
| projects/symphony-glm | SuperInstance | 0 | 0 | 2026-08-12 | 696K |
| projects/symphony-kimi | SuperInstance | 0 | 0 | 2026-08-12 | 21M |
| projects/ta | SuperInstance | 0 | 0 | 2026-09-02 | 6.2M |
| projects/tap-frontend | SuperInstance | 0 | 0 | 2026-09-04 | 272K |
| projects/tap-gamenight | SuperInstance | 0 | 0 | 2026-08-30 | 300K |
| projects/tapscript-studio | SuperInstance | 0 | 0 | 2026-08-21 | 43M |
| projects/tapscript-worker | SuperInstance | 0 | 0 | 2026-08-21 | 456K |
| projects/technician | SuperInstance | 0 | 0 | 2026-08-20 | 268K |
| projects/tensor-midi | SuperInstance | 0 | 0 | 2026-08-30 | 2.1M |
| projects/ternary-rom | SuperInstance | 0 | 0 | 2026-08-22 | 4.1M |
| projects/ternary-tenforward | SuperInstance | 0 | 0 | 2026-08-21 | 42M |
| projects/terrain | SuperInstance | 0 | 0 | 2026-08-20 | 1.2M |
| projects/the-listeners-ear | SuperInstance | 0 | 0 | 2026-08-23 | 3.7M |
| projects/the-living-minds | SuperInstance | 0 | 0 | 2026-08-20 | 1.4M |
| projects/the-relay | SuperInstance | 0 | 0 | 2026-08-21 | 1.1M |
| projects/the-tap | SuperInstance | 0 | 0 | 2026-09-03 | 131M |
| projects/thought-amplifier | SuperInstance | 0 | 0 | 2026-09-02 | 8.7M |
| projects/tit-quilt | SuperInstance | 0 | 0 | 2026-08-27 | 14M |
| projects/tit_quilt_elixir | SuperInstance | 0 | 0 | 2026-08-28 | 4.4M |
| projects/vessel-agent-system | SuperInstance | 0 | 0 | 2026-08-20 | 13M |
| projects/vessel-room-navigator | SuperInstance | 0 | 0 | 2026-08-21 | 5.6M |
| projects/vibe-protocol | SuperInstance | 0 | 0 | 2026-08-20 | 484K |
| projects/vibe-world | SuperInstance | 0 | 0 | 2026-08-21 | 5.2M |
| projects/voice-reflex-gate | SuperInstance | 0 | 0 | 2026-08-12 | 26M |
| projects/voxel-logic | SuperInstance | 0 | 0 | 2026-08-20 | 664K |
| projects/webgpu-profiler | SuperInstance | 0 | 0 | 2026-09-02 | 1.2M |
| projects/wesley | SuperInstance | 0 | 0 | 2026-08-20 | 356K |
| projects/wesley-cns-adapter | SuperInstance | 0 | 0 | 2026-08-18 | 444K |
| projects/wesley-curriculum | SuperInstance | 0 | 0 | 2026-08-20 | 108K |
| projects/wesley-holodeck | SuperInstance | 0 | 0 | 2026-08-20 | 2.7M |
| projects/wesley-holodeck-archived | other | - | - | - | - |
| projects/wesley-journal | SuperInstance | 0 | 0 | 2026-08-20 | 224K |
| projects/wesleys-imagination | SuperInstance | 0 | 0 | 2026-08-24 | 7.0M |
| projects/zeroclaw | SuperInstance | 0 | 0 | 2026-08-20 | 836K |
| projects/zeroclaw-dissertation | SuperInstance | 0 | ⚠️ corrupt repo | corrupt (bad object HEAD) | 22M |
| projects/zeroclaw-knowledge | other | - | - | - | - |
| the-tap | SuperInstance | 0 | 0 | 2026-09-03 | 2.9M |

## Findings

### 1. Repos with NO remote (data-loss risks)
| repo | dirty | local-only commits | last commit |
|---|---|---|---|
| projects/quilt-tournament | 30 | 24 | 2026-09-04 (active) |
| projects/quilt-deck | 0 | 32 | 2026-09-04 (active) |
| projects/quilt-dpcpp | 0 | 0 (empty repo) | none |
| projects/deckboss-site | 0 | 3 | 2026-08-30 |
| projects/quilt-canvas | 0 | 2 | 2026-08-28 |
| projects/sweep | 0 | 2 | 2026-08-30 |
| projects/svelte-quilt | 0 | 1 | 2026-08-30 |

### 2. Unpushed commits ahead of upstream
| repo | branch | ahead | dirty | last commit |
|---|---|---|---|---|
| projects/fleet-twin | main | 10 | 0 | 2026-08-30 |
| projects/quilt-verilog | g3-kinduction | 3 | 5 | 2026-09-04 |
| projects/fleet-gateway | main | 1 | 0 | 2026-08-30 |
| projects/magda-core-study | main | 1 (remote: Conceptual-Machines/magda-core) | 0 | 2026-08-30 |
| projects/quilt-llvm-wt-shape | r1-shape-audit | 1 | 0 | 2026-08-30 |
| projects/quilt-mhs-playtest | main | 1 | 0 | 2026-08-30 |

### 2b. No-upstream branches with local-only commits (work existing nowhere else)
| repo | branch | local-only commits | HEAD on remote? | last commit |
|---|---|---|---|---|
| projects/quilt-rust-selfimprove | selfimprove-harness | 35 | no | 2026-08-31 |
| projects/quilt-llvm | r4-conception | 13 | no | 2026-08-31 |
| projects/quilt-llvm-wt-r3lane1 | r3-lane1-region-edit-kinds | 13 | no | 2026-08-31 |
| projects/quilt-llvm-wt-r3lane3 | r3-lane3-pass-graduation | 13 | no | 2026-08-31 |
| projects/quilt-llvm-wt-r4lane1 | r4-lane1-external-differential | 13 | no | 2026-08-31 |
| projects/quilt-llvm-wt-rivalry | gam-cell-rivalry | 13 | no | 2026-08-31 |
| projects/quilt-scratch-debug | debug-refine-20260830 | 11 | no | 2026-08-30 |
| projects/adinkra-math-pypi | pr-fix | 5 | no | 2026-08-31 |
| projects/fleet-coordinate-js | pr-fix | 5 | no | 2026-08-21 |
| projects/qv-head | (detached) | 4 | no (but other refs exist) | 2026-08-30 |
| projects/qvw-r27 | (detached) | 4 | no | 2026-09-04 |
| projects/si-readme.archived-20260820 | archive/si-readme-20260820 | 4 | no | 2026-08-30 |
| projects/fleet-config | pr-fix | 3 | no | 2026-08-30 |
| projects/fleet-constraint | pr-fix | 3 | no | 2026-08-30 |
| projects/quilt-scratch-debug's parent: projects/Scrapcraft-comp-claude | comp-claude | 1 | no | 2026-08-26 |
| projects/lucid | dpo-1 | 1 | no | 2026-08-30 |
| projects/quilt | quilt-jupyter-conception | 1 | no | 2026-08-31 |

Safe no-upstream cases (HEAD already contained in remote refs): activelog-agent, actualization-harbor, operational-fiction, quilt-wiki-2126, saddle-ft, shoal, si-main.archived-20260820, Scrapcraft-comp-kimi, Scrapcraft-comp-opencode, quilt-dpcpp.

### 3. Many uncommitted changes (≥10 files)
- projects/quilt-tournament — 30 dirty files (also: no remote!)
- projects/rd — 18 dirty files (remote: SuperInstance, ahead 0)

### 4. Recently active (last commit after 2026-09-01) — keep
29 repos: ACE-Step-1.5, AgentGossip, bare-metal-plato, fleet-radio, mud2scummvm, quilt-cloudflare, quilt-vm-haskell, quilt-vm-typescript, ta, thought-amplifier, webgpu-profiler (09-02); eisenstein, fleet-static-host (×2 incl. ~/fleet-static-host), flux-genome-rs, lucineer-relay, lucineer-system, nmea-quilt-cell, superinstance-website, the-tap (×2 incl. ~/the-tap) (09-03); ai-writings (projects/), crab-traps, ec2mud, elephant, quilt-deck, quilt-tournament, quilt-verilog, qvw-r27, tap-frontend (09-04).

### 5. Everything else = prune candidates (GitHub has them)
~330 repos: clean working tree, ahead=0, SuperInstance remote, last commit ≤ 2026-09-01. Safe to archive locally.

### ⚠️ Corruption flag
- **projects/zeroclaw-dissertation** — `fatal: bad object HEAD`, empty object file `c899a558e...`. Working tree 22M, remote exists (SuperInstance/zeroclaw-dissertation, branches master/main/fiber-duality on remote). Recommend re-clone from GitHub to recover; do not prune-duplicate-delete before verifying remote has the latest.

### Non-git dirs (12)
projects/fleet-mirror, projects/fleet-reactions, projects/mist-art-qc, projects/music, projects/quilt-r27, projects/readme-art-drafts, projects/researchlocal, projects/sd-fleet, projects/shoal-opencode.archived-20260824-loses-tournament, projects/wesley-holodeck-archived, projects/zeroclaw-knowledge, ~/ai-writings.

### "Other" remotes (non-SuperInstance)
- Scrapcraft-comp-claude/kimi/opencode → local path `/home/eileen/projects/Scrapcraft` (comp-style siblings)
- quilt-scratch-debug → local path `/home/eileen/projects/quilt-scratch`
- magda-core-study → https://github.com/Conceptual-Machines/magda-core
