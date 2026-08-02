# World Economy — Seed-2.0-Pro

*Generated in 50.1s*

# SLACKWATER: COMPLETE RESOURCE ECONOMY v1.1
Core Design Principle: **Scarcity is temporary, never permanent. No resource stays rare longer than one full era. The economy will never softlock, it will only push.**

---
## 1. PER-ERA RESOURCE SCARCITY CURVES
All resources have a Global Abundance Score 0-100 (lower = rarer). Bold = **Era Bottleneck Resource** (the resource that will always run out first locally, and forces exploration).

Hard coded rule: *The bottleneck for era N will NEVER spawn within 120 studs of initial spawn. It only appears 300+ studs out, and becomes common only 700+ studs from spawn.*

| Resource | Base Abundance | Era 0 | Era 1 | Era 2 | Era 3 | Era 4 | Era 5 | Era 6 |
|---|---|---|---|---|---|---|---|---|
| Driftwood | 92 | Common | Common | Trash | Trash | Fuel Only | Fuel Only | Irrelevant |
| Flint | 78 | Scarce | Common | Common | Trash | Obsolete | Obsolete | Obsolete |
| Hardwood | 61 | **Rare** | Scarce | Common | Common | Common | Obsolete | Obsolete |
| Wrought Iron | 47 | Locked | **Rare** | Scarce | Common | Common | Common | Obsolete |
| Copper Wire | 33 | Locked | Locked | **Rare** | Scarce | Common | Common | Common |
| Relay Contacts | 21 | Locked | Locked | Locked | **Rare** | Scarce | Common | Common |
| Silicon Wafers | 12 | Locked | Locked | Locked | Locked | **Rare** | Scarce | Common |
| Agent Core Shards | 5 | Locked | Locked | Locked | Locked | Locked | **Rare** | Scarce |

---
## 2. TIDE LOOT TABLES
Tide cycle = 18 real minutes. 2 tides per full cycle. 3 independent loot rolls per player per tide. All weights out of 1000 total roll.

| Loot Category | Era 0 | Era 1 | Era 2 | Era 3 | Era 4 | Era 5 | Era 6 | Behaviour Notes |
|---|---|---|---|---|---|---|---|---|
| Junk Scrap | 620 | 510 | 410 | 300 | 190 | 110 | 40 | Smelt 10:1 for base metal |
| Current Era Common | 270 | 320 | 360 | 390 | 410 | 420 | 390 | Exactly the filler resource you need right now |
| **Current Era Bottleneck** | 45 | 90 | 135 | 180 | 225 | 270 | 315 | *Only early game source of bottleneck without exploration* |
| Next Era Preview | 50 | 60 | 70 | 90 | 120 | 150 | 180 | 1 single unit of next era resource. Teaser only. |
| Ancient Relic | 15 | 20 | 25 | 40 | 55 | 50 | 75 | Unique part that skips 1 full recipe unlock |

✅ Guaranteed Safety Rule: Every 7 tides, you will receive at least 1 unit of your current era bottleneck. No permanent walls. The tide is your safety net.

---
## 3. CRAFTING COST PROGRESSION
Costs scale on **unique resource types**, not raw volume. You will never be asked for 1000 wood. Every era adds exactly one new required resource.

| Era | Unique Resources Per Recipe | Multiplier Over Prior Era | Average Recipe Unit Cost | Benchmark Example |
|---|---|---|---|---|
| 0 Simple Machines | 2 | 1.0x | 3 | Wheel = 2 Wood + 1 Flint |
| 1 Power Transmission | 3 | 1.6x | 7 | Gearbox = 3 Hardwood + 3 Iron + 1 Grease |
| 2 Electricity | 4 | 1.6x | 11 | Dynamo = 4 Iron + 3 Copper + 2 Wire + 2 Magnet |
| 3 Control Systems | 5 | 1.5x | 17 | AND Gate = 4 Relay + 5 Wire + 3 Spring + 3 Contact + 2 Insulator |
| 4 Programmable Logic | 6 | 1.4x | 24 | Arduino Core = 6 Silicon + 5 Copper + 4 Relay + 4 Capacitor + 3 Crystal + 2 Resistor |
| 5 Networked Systems | 7 | 1.3x | 31 | Mesh Node = 7 Wafer + 6 Antenna + 5 Transceiver + 4 Arduino + 3 Battery + 2 Sensor + 1 Crystal |
| 6 Autonomous Agents | 8 | 1.2x | 37 | Agent Core = 8 Shard + 7 Mesh Node + 6 Sensor Array + 5 Logic Bank + 4 Battery + 3 Motor + 2 Frame + 1 Beacon |

---
## 4. AGENT LABOR ECONOMY
Agents do not cost gold. They cost **attention**. This is the primary economic limiter for endgame.

| Agent Class | One-Time Deployment Cost | Upkeep Per 10 Minutes | Max Concurrent Deployments |
|---|---|---|---|
| Builder / Teacher | 1x Current Era Common | 0 | 3 |
| Research Autoplay Agent | 3x Current Era Bottleneck | 1x Common Resource | 1 per unlocked era |
| Rival Agent | 5x Any Ancient Relic | 2x Bottleneck | 1 maximum |

⚡ Critical Labor Rule:
> All agents will stop working and initiate a conversation after 12 minutes of deployment. You must respond (1 line chat, confirmation, correction) or they idle permanently. You cannot AFK farm an army. Skill at managing agents is the only endgame force multiplier.

---
## 5. MULTIPLAYER TRADE SYSTEM
No global auction house. No permanent orders. Trade only exists at low tide:
1.  When tide recedes, players may place trade crates on the exposed tidal flat
2.  Crates are visible to all players for exactly the 9 minute low tide window
3.  You may only take items from a crate if you leave the exact requested items in return
4.  When the tide rises, all unclaimed trades are washed away forever.

This creates natural market tension, time pressure, and actual player interaction rather than passive spreadsheet trading.

---
## 6. SCARCITY → EXPLORATION FEEDBACK LOOP
This is the beating heart of the game. Runs identically on a timer for every era, no exceptions:

| Stage | Trigger | Player Behaviour |
|---|---|---|
| ✅ Stage 1: Local Depletion | After 7 tides (~2h playtime) all bottleneck resources within 120 studs of spawn are fully exhausted | Player will grind tide loot, optimize their base, complain about bad RNG |
| ⚠️ Stage 2: The Push | After 11 tides (~3.3h playtime) tide stops dropping bottleneck resource. Agent Hermes will begin pinging: "There's good iron up north. You should go." | Player will finally leave base |
| ❌ Stage 3: The Force | After 14 tides (~4.2h playtime) storm tide arrives. It will destroy 30% of unupgraded base structures. You cannot stop this storm without the tech unlocked by the bottleneck resource. | Player will run. They will explore. They will find the new deposit. They will return stronger. |

### Final Economic Guarantee
> No player will ever be stuck for more than 90 real minutes before the game gently, then firmly, pushes them to explore. There are no grind walls. There is only choice: wait for the tide, or go get it yourself.