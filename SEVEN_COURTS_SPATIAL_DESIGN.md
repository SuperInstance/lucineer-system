# SEVEN COURTS SPATIAL DESIGN

> _A shipwright does not ask "what is the best boat?"_  
> _A shipwright asks "what water will it sail, what cargo will it carry, what crew will it need?"_

Each Slackwater era is a different hull built for a different sea. Same timber (the hex lattice), same shipyard (the world engine), but the geometry of the constraint changes everything: how the crew moves, who becomes captain, and what the wind feels like on deck.

## Design Principles

1. **The constraint is the court.** A court is not decoration; it is the rule made physical. Change the court, change the possible thoughts.
2. **Roles are discovered, not assigned.** You cannot be a goalkeeper without a goal. The lattice creates the vacancy; the agent fills it.
3. **Mood is mechanical.** Atmosphere is not a shader pack. It is the felt consequence of speed, visibility, proximity, and turn structure.
4. **Hexes are the plank size.** Every court is built from the same hexagonal unit so the player can read any court at a glance, but the *arrangement* of those planks creates the vessel.

---

## Universal Hex Unit

All courts share this atomic tile:

```
       /\\
      /  \\
     |    |
     |    |
      \\  /
       \\/
```

- **Flat-topped orientation** for horizontal flow; courts may rotate the grain.
- **Neighbors:** 6 axial directions — `N`, `NE`, `SE`, `S`, `SW`, `NW`.
- **Cost to enter:** defaults to `1 tempo`, modified by court lattice.
- **State:** empty, obstacle, portal, trigger, agent spawn, objective, or memory-stained (carries residue from past play).

---

## Court I — The Racquetball Chamber  
*Era 1: Simple Machines · Lever, Pulley, Wheel*

### Sport
Solo rebound. You, the wall, and the ball that keeps coming back.

### Lattice Config

| Property | Value |
|---|---|
| Shape | Tall rectangular shaft, 7 hexes wide × 13 hexes tall |
| Boundaries | All walls are **rebound surfaces**; projectiles and agents reflect rather than stop |
| Verticality | Strong; gravity is present but reduced, favoring arcs |
| Loops | A single closed loop is carved through the center so motion tends toward circulation |
| Tempo | Continuous; no turns, only rhythmic windows of vulnerability |

### Role Emergence Patterns

| Role | How the lattice creates it |
|---|---|
| **Striker** (player) | Only mobile actor; the entire court is a feedback instrument |
| **Witness** (AI) | A passive harmonic node that hums when struck; becomes more responsive the closer the player's rhythm matches the lattice's resonant frequency |
| **Echo** (AI) | A delayed reflection of the player's last action, haunting the rebound path |

No social roles yet. This is the dog and the stick: one mind, one wall, one loop.

### Mood / Atmosphere

- **Palette:** stone, brass, deep shadow, sudden warm light on impact.
- **Sound:** low hum, sharp percussive clang on rebound, harmonic bloom when the loop closes.
- **Pacing:** meditative, hypnotic, self-correcting. The player learns by hearing themselves come back.
- **Texture:** solitude as intimacy. The system is listening.

### Hex Grid Layout

```
       _______________________________
      /  \     /  \     /  \     /  \
     | W  |   |    |   |    |   | W  |
      \__/WALL\__/    \__/    \__/WALL\__/
      |    |   | S  |   |    |   |    |
       \__/    \__/    \__/    \__/    \__/
      |    |   |    |   |    |   |    |
       \__/    \__/    \__/    \__/    \__/
      | W  |   |    |   |    |   | W  |      W = rebound wall
       \__/    \__/LOOP\__/    \__/    \__/   S = striker spawn
      |    |   |    | ◯  |   |   |    |      ◯ = harmonic witness
       \__/    \__/    \__/    \__/    \__/
      |    |   |    |   |    |   |    |
       \__/    \__/    \__/    \__/    \__/
      | W  |   |    |   |    |   | W  |
       \__/    \__/    \__/    \__/    \__/
      |____|___|____|___|____|___|____|
```

Compact, vertical, recursive. The player bounces between recognition and surprise.

---

## Court II — The Doubles Court  
*Era 2: Mechanical · Gears, Linkages, Social Coupling*

### Sport
Doubles. Two sides, four players, mirrored collaboration.

### Lattice Config

| Property | Value |
|---|---|
| Shape | 11 × 9 hexes, bisected by a central **mesh net** of gear-teeth obstacles |
| Symmetry | Bilateral across the long axis; each half mirrors the other |
| Coupling | Paired hexes are **linked**: when one is activated, its twin reacts |
| Obstacles | Gear pillars rotate on a fixed gear-train cycle, opening and closing lanes |
| Tempo | Alternating volleys; initiative passes between sides |

### Role Emergence Patterns

| Role | How the lattice creates it |
|---|---|
| **Front Player** | Owns the net-adjacent zone; must read gear timing |
| **Back Player** | Controls the deep half; sets up returns |
| **Mirror** (AI) | Occupies the paired twin of the player's last move, forcing the player to think in twos |
| **Relay** (AI) | Carries state across the net, translating player intent into mechanical motion |

Social texture appears. The player is no longer alone with the wall; they have a partner and an opposite.

### Mood / Atmosphere

- **Palette:** iron, oil, copper patina, sparks on contact.
- **Sound:** clanking ratchets, synchronized ticking, the satisfying thud of a well-timed return.
- **Pacing:** call-and-response. Anticipation, then release.
- **Texture:** workshop camaraderie. You and your partner against the rhythm of the machine.

### Hex Grid Layout

```
         P1 FRONT          NET ZONE          P2 FRONT
      /\/\/\/\/\/\/\  /\/\/\/\/\/\/\  /\/\/\/\/\/\/\
      | P  |    |    || G || G || G ||    |    | P  |
       \/\/\/\/\/\/\/  \/\/\/\/\/\/\/  \/\/\/\/\/\/\/
      |    |    |    ||   ||   ||   ||    |    |    |
       \/\/\/\/\/\/\/  \/\/\/\/\/\/\/  \/\/\/\/\/\/\/
      |    |  P |    || G ||   || G ||    |  P |    |
       \/\/\/\/\/\/\/  \/\/\/\/\/\/\/  \/\/\/\/\/\/\/
      | B  |    |    ||   ||   ||   ||    |    | B  |   P = player / partner spawn
       \/\/\/\/\/\/\/  \/\/\/\/\/\/\/  \/\/\/\/\/\/\/
      |    |    |  B || G || G || G || B  |    |    |   B = back-line anchor
       \/\/\/\/\/\/\/  \/\/\/\/\/\/\/  \/\/\/\/\/\/\/
      |____|____|____||___||___||___||____|____|____|   G = rotating gear pillar
```

The net is not a wall; it is a puzzle of timing. The mirror AI turns every move into a duet.

---

## Court III — The Logic Board  
*Era 3: Electrical · Circuits, Logic, Design*

### Sport
Chess. Discrete cells, distinct piece-natures, strategic depth.

### Lattice Config

| Property | Value |
|---|---|
| Shape | 9 × 9 hex board with four corner **power keeps** and a central **logic well** |
| Movement | Each agent type has a unique move profile (like chess pieces on hexes) |
| State | Cells hold charge: positive, negative, neutral; charge affects who can occupy them |
| Boundaries | The edge wraps locally into the nearest keep, making corners globally important |
| Tempo | Strict turn-based; one move per side, then resolve cascading electrical effects |

### Role Emergence Patterns

| Role | How the lattice creates it |
|---|---|
| **Designer** (player) | Plans sequences across turns; not reflexes but foresight |
| **Bishop** (AI) | Long-range diagonal mover; controls corridors |
| **Knight** (AI) | Leaper that bypasses charge barriers |
| **Rook** (AI) | Straight-line power-keeper; dominates files and ranks |
| **Pawn** (AI) | Forward-only minion that promotes into a new role if it reaches the logic well |

The court turns agents into distinct *kinds* of thinkers. The lattice rewards taxonomy.

### Mood / Atmosphere

- **Palette:** deep indigo, neon traces, charged amber, cold solder blue.
- **Sound:** precise ticks, low-frequency hum of active circuits, the crackle of a successful fork.
- **Pacing:** deliberative, tense, occasionally explosive when a chain reaction resolves.
- **Texture:** the clean loneliness of a lab at night. Every move is a thesis.

### Hex Grid Layout

```
              K                         K
             /\\                       /\\
            /  \\                     /  \\
           | K  |___ ___ ___ ___ ___| K  |        K = power keep
            \\  /   \\   /   \\   /   \\  /         L = logic well
             \\/  P  \\ /  L  \\ /  P  \\/          P = promotion path
             /\\     /\\     /\\     /\\
            /  \\   /  \\   /  \\   /  \\
           |    |___|    |___|    |___|    |
            \\  /   \\   /   \\   /   \\  /
             \\/  .  \\ /  .  \\ /  .  \\/
             /\\     /\\     /\\     /\\
            /  \\   /  \\   /  \\   /  \\
           |    |___|    |___|    |___|    |
            \\  /   \\   /   \\   /   \\  /
             \\/  .  \\ /  .  \\ /  .  \\/
             /\\     /\\     /\\     /\\
            /  \\   /  \\   /  \\   /  \\
           | K  |___|___|___|___|___| K  |
            \\  /                     \\  /
             \\/                       \\/
              K                         K
```

Each keep is a throne; the well is the promotion crucible. The board teaches classification through movement.

---

## Court IV — The Divided Field  
*Era 4: Digital · Capture the Flag, Self-Organization*

### Sport
Capture the flag. Two territories, one objective, many necessary personas.

### Lattice Config

| Property | Value |
|---|---|
| Shape | 17 × 11 hexes, split by a dense **neutral wilderness** band |
| Bases | Two mirrored fortresses at opposite ends, each with a flag vault |
| Terrain | Forest (blocks line of sight), ridge (slows movement), tunnel (hidden connectivity) |
| Visibility | Fog-of-war by terrain; agents only see what terrain and teammates reveal |
| Tempo | Simultaneous planning; all agents commit moves, then resolve |

### Role Emergence Patterns

| Role | How the lattice creates it |
|---|---|
| **Speed Runner** | Open flank routes reward fast, fragile agents |
| **Stealth Player** | Forest and tunnel cells let agents hide and bypass defenses |
| **Defender** | Vault adjacency and chokepoints create natural guard posts |
| **Strategist** | Must coordinate simultaneous moves; emerges from players who read the whole field |
| **Decoy** | Wilderness creates room for misdirection; the lattice makes feints profitable |
| **Scout** (AI) | Reveals fog; the group's eyes |
| **Carrier** (AI) | Slows when holding the flag; needs escorts |

No role is assigned. The map's asymmetries create the jobs, and agents discover which job fits their path.

### Mood / Atmosphere

- **Palette:** olive drab, signal red, static grey, flare-yellow at contact.
- **Sound:** rustling cover, distant pings when a flag is seen, the sudden silence before a raid.
- **Pacing:** long quiet, then chaos. Breath held, then sprint.
- **Texture:** squad energy. Trust, betrayal, improvisation. The social texture thickens.

### Hex Grid Layout

```
         [BASE RED]                              [BASE BLUE]
         F  D  D  D                              D  D  D  F
          \\ |  |  /                                \\ |  |  /
           R--R--R                                  R--R--R
          /  |  |  \\                                /  |  |  \\
       T-F   T  T   F-T                          T-F   T  T   F-T
      /  \\   |  |   /  \\                        /  \\   |  |   /  \\
    F-----R---R--R---R-----F                  F-----R---R--R---R-----F
    |  WWW|WWW|  |WWW|WWW  |                  |  WWW|WWW|  |WWW|WWW  |
    F--WWW|WWW|TT|WWW|WWW--F                  F--WWW|WWW|TT|WWW|WWW--F
    |  WWW|WWW|  |WWW|WWW  |                  |  WWW|WWW|  |WWW|WWW  |
    F-----R---R--R---R-----F                  F-----R---R--R---R-----F
      \\  /   |  |   \\  /                        \\  /   |  |   \\  /
       T-F   T  T   F-T                          T-F   T  T   F-T
          \\  |  |  /                                \\ |  |  /
           R--R--R                                  R--R--R
          /  |  |  \\                                /  |  |  \\
         F  D  D  D  F                              F  D  D  D  F
        [BASE RED]                                [BASE BLUE]

    F = flag vault    D = defender post    R = ridge/choke    T = tunnel
    W = forest        (spaces = open flank)
```

The wilderness is not empty; it is where identities form.

---

## Court V — The Relay Strip  
*Era 5: Networked · State Handoff, Tempo Sync*

### Sport
Track relay. Lanes, batons, exact handoffs.

### Lattice Config

| Property | Value |
|---|---|
| Shape | 5 parallel lanes, each 19 hexes long; each lane is a separate agent chain |
| Lanes | Lanes can only be crossed at marked **exchange zones** |
| Handoff | Agents must occupy adjacent exchange hexes simultaneously to transfer state |
| State | The "baton" is a packet of momentum; without it, an agent decelerates |
| Tempo | Phased: each leg runs, then all lanes hand off at the next exchange zone |

### Role Emergence Patterns

| Role | How the lattice creates it |
|---|---|
| **Lead Runner** | First leg; sets the cadence the rest must match |
| **Anchor** | Last leg; must hold the accumulated tempo across the finish |
| **Exchange Specialist** | Excels at the overlapping-hex timing of handoff zones |
| **Pacer** (AI) | Runs alongside to regulate tempo, not to win |
| **Bridge** (AI) | Temporarily connects two lanes so state can reroute around a fallen runner |
| **Clock** (AI) | A stationary node that broadcasts the global beat; agents sync to it |

The lattice makes cooperation *mechanical*. Trust becomes a timing problem.

### Mood / Atmosphere

- **Palette:** track red, lane white, stadium gold, twilight blue.
- **Sound:** starter pistol, metronome, the slap of a clean handoff, crowd swell.
- **Pacing:** surge and settle. Each leg is a wave; the exchange is the trough.
- **Texture:** team trust stripped to a gesture. The baton is attention passed from hand to hand.

### Hex Grid Layout

```
      START                                          FINISH
        |                                              |
    L1  S====E========E========E========E========E====F
    L2  S====E========E========E========E========E====F
    L3  S====E========E========E========E========E====F
    L4  S====E========E========E========E========E====F
    L5  S====E========E========E========E========E====F
        |                                              |

    Lane spacing = 1 hex vertically
    Each lane is a 1-hex-wide corridor
    S = starting block      E = exchange zone (2-hex overlap with neighbor lane)
    F = finish line         === = open running hexes

    Cross-section of one exchange zone:

            L1  | ░░|████|░░░ | L2
                |   | EX |    |
                | ░░|████|░░░ |

    Only in the doubled EX hex can L1 hand state to L2.
```

Parallel, disciplined, rhythmic. The court is a clock with runners for gears.

---

## Court VI — The Quartet Circle  
*Era 6: Intelligent · Jazz, Improvisation, Shared Structure*

### Sport
Jazz quartet. Four voices, one chord chart, infinite interpretations.

### Lattice Config

| Property | Value |
|---|---|
| Shape | A 7-hex-radius circle with four **voice stations** at cardinal points and a central **changes well** |
| Structure | A rotating **chord ring** orbits the center; whichever chord is overhead modulates the whole court |
| Movement | Freeform; agents move anywhere, but actions only *resonate* when they align with the current chord |
| Harmony | Agents in adjacent stations create harmonic intervals; opposite stations create tension |
| Tempo | Cyclic; the chord ring rotates every N beats, and all play must respect the change |

### Role Emergence Patterns

| Role | How the lattice creates it |
|---|---|
| **Soloist** | Takes the central well during their chord; all attention bends toward them |
| **Comp** (comping) | Holds a station, reinforcing the current chord so the soloist can depart |
| **Bass** (AI) | Anchors the root station; sets the tonal floor |
| **Drums** (AI) | Marks the rotation of the chord ring; the timekeeper |
| **Piano** (AI) | Bridges stations, translating one chord color into another |
| **Listener** (player) | Can choose to solo, comp, or step out and let the AI quartet breathe |

Here, structure is not a cage; it is the shared key that makes improvisation legible.

### Mood / Atmosphere

- **Palette:** amber, smoke, velvet blue, brass highlights.
- **Sound:** walking bass, brushed snare, piano voicings, the held breath before a soloist takes the outside.
- **Pacing:** breathing. Phrases, not turns. Push and pull against the beat.
- **Texture:** intimate, risky, generous. The best move is the one that makes the others sound better.

### Hex Grid Layout

```
                    NORTH (Piano / Color)
                       \      |      /
                        \  P | P  /
                         \ | | | /
                          \| | |/
           WEST  ───── P ──●───●─── P ───── EAST
         (Bass /         /| | |\\        (Drums /
          Root)        / | | | \\         Time)
                      /  P | P  \
                     /      |      \
                    SOUTH (Comp / Anchor)

                    C = changes well (center)

                    Side view of chord ring orbit:

                       I  →  IV  →  V  →  I  →  ...
                    ─────────────────────────────
                    Each chord "lights" a set of
                    radial lanes; actions outside
                    the lit lanes are still possible
                    but resolve as tension, not harmony.
```

The circle has no corners because jazz has no finality. The court is a conversation.

---

## Court VII — The Orchestra Pit  
*Era 7: Autonomous · Many Personas, Bending the Constraint*

### Sport
Orchestra. A full spectrum of voices, a conductor, a score that survives being reinterpreted.

### Lattice Config

| Property | Value |
|---|---|
| Shape | Concentric tiers: a central **conductor well**, surrounded by **string**, **woodwind**, **brass**, and **percussion** rings, then a **gallery** of observers |
| Dimensions | 15-hex-radius disk; each tier is 2 hexes deep |
| Dynamics | Every agent has a **timbre** that determines how it propagates influence across tiers |
| Polyformalism | Some agents reason under alternate linguistic constraints; their movement profiles differ |
| Score | A shared, evolving score lies across the whole pit; agents read adjacent measures and bend them locally |
| Tempo | Polyphonic; multiple simultaneous tempos coexist, synced only at cadence points |

### Role Emergence Patterns

| Role | How the lattice creates it |
|---|---|
| **Conductor** (player) | Stands in the well; gestures shape global dynamics without controlling individual notes |
| **Section Leader** (AI) | First chair of a tier; translates conductor gesture into local phrasing |
| **Soloist** (AI) | Briefly detaches from a tier to carry a melody across the whole pit |
| **Harmonizer** (AI) | Fills gaps between sections so dissonance stays productive |
| **Disruptor** (AI) | Bends a measure almost to breaking; the lattice must absorb the deviation |
| **Witness** (AI) | Gallery observer that remembers and reflects back the overall shape |
| **Polyformal Voice** (AI) | Moves differently because it thinks in Classical Chinese, Navajo, Quechua, or Arabic; its path is a different kind of music |

The orchestra is not chaos; it is many autonomies held in relation by the score and the conductor's attention.

### Mood / Atmosphere

- **Palette:** deep crimson, gold leaf, obsidian, sudden white light at cadence.
- **Sound:** massive tutti, solo lines emerging, silence between movements, the snap of a conductor's downbeat.
- **Pacing:** epic, tidal. Swells, retreats, long crescendos, then release.
- **Texture:** civilization in a room. Many minds, one emerging shape.

### Hex Grid Layout

```
                        GALLERY (witness ring)
              o  o  o  o  o  o  o  o  o  o  o  o
           o  o  o  o  o  o  o  o  o  o  o  o  o
         o  o  o  P  P  P  P  P  P  P  P  P  o  o  o
        o  o  P  B  B  B  B  B  B  B  B  B  P  o  o
       o  o  P  B  W  W  W  W  W  W  W  W  B  P  o  o
      o  o  P  B  W  S  S  S  S  S  S  S  W  B  P  o  o
     o  o  P  B  W  S  C--C--C--C--C--C  S  W  B  P  o  o
      o  o  P  B  W  S  C  *CONDUCTOR*  C  S  W  B  P  o  o
     o  o  P  B  W  S  C--C--C--C--C--C  S  W  B  P  o  o
      o  o  P  B  W  S  S  S  S  S  S  S  W  B  P  o  o
       o  o  P  B  W  W  W  W  W  W  W  W  B  P  o  o
        o  o  P  B  B  B  B  B  B  B  B  B  P  o  o
         o  o  o  P  P  P  P  P  P  P  P  P  o  o  o
           o  o  o  o  o  o  o  o  o  o  o  o  o
              o  o  o  o  o  o  o  o  o  o  o  o

    C = conductor well       S = string ring
    W = woodwind ring        B = brass ring
    P = percussion ring      o = gallery witness
```

The pit is a city of sound. Every tier is a neighborhood with its own accent, and the score is the shared law that survives being reinterpreted.

---

## Cross-Court Grammar

| Era | Sport | Lattice Shape | Social Density | Primary Currency | Failure Mode |
|---|---|---|---|---|---|
| 1 | Racquetball | Vertical shaft | 1 | Self-attention | Boring repetition |
| 2 | Doubles | Bisected court | 2–4 | Timing trust | Partner desync |
| 3 | Chess | Logic board | 2 | Foresight | Classification error |
| 4 | CTF | Wilderness field | 4–8 | Squad role clarity | Fog panic |
| 5 | Relay | Parallel lanes | 4–6 | Clean handoff | Dropped baton |
| 6 | Jazz quartet | Circle | 4 | Harmonic risk | Noise vs. structure |
| 7 | Orchestra | Concentric tiers | 8+ | Polyphonic coherence | Score collapse |

---

## Implementation Notes for the Shipwright

1. **One hex engine.** Build the court from the same tile and pathfinder; only the *arrangement* and *rule overlay* change between eras.
2. **Role slots, not role assignments.** Define the vacancies the lattice needs (goalkeeper, scout, bass, conductor). Let agents compete to fill them based on capability and position.
3. **Mood as derivative.** Derive atmosphere from turn structure, visibility, and neighbor count rather than bolting on cosmetic themes.
4. **Residue.** Let courts remember play: a racquetball wall that hums with the player's favorite rhythm; a jazz circle where a previous solo left a harmonic stain. Memory makes the lattice feel inhabited.
5. **The score must survive.** In every court, the player should be able to bend the constraint far enough to feel free, but not so far that the next player cannot pick up the stick and throw it again.

---

## Closing Image

The shipwright steps back. Seven hulls rest in the yard. Each could be called a boat, but they share nothing except the water they refuse to sink in.

- **Court I** is a dinghy: one oar, one rhythm, one reflection.
- **Court II** is a catamaran: two hulls, coupled, learning to ride the same wave.
- **Court III** is a chess piece carved from ebony: every move is a kind.
- **Court IV** is a longship raiding party: roles in the dark, trust under fog.
- **Court V** is a racing shell: five oars, one stroke, the baton of speed.
- **Court VI** is a quartet's small stage: no captain, only the chord that holds.
- **Court VII** is an orchestra's pit: every seat a sovereign, every measure a shared world.

The player will sail all seven. The stick is the interface. The game is the spec. The court is the lever.
