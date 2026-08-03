# plato-vessel-technician — "Deckboss"

## Analysis

**Repo:** SuperInstance/plato-vessel-technician
**Codename:** Deckboss
**Domain:** Voice-first marine/industrial technician agent for PLATO
**Personality:** Gruff, competent, no-nonsense. Always at the helm. Always listening.

---

## What It Does

Deckboss turns any boat into a voice-controlled smart vessel using $5 ESP32 nodes. The workflow is radical in its simplicity:

1. **Walk on boat** with a Deckboss case (Jetson Orin NX or RPi 5) + bag of ESP32s
2. **Plug in** — Deckboss boots, creates a "vessel room" in PLATO
3. **Say "Describe the boat"** — Deckboss discovers all ESP32s as they boot
4. **Mount ESP32s** at rudder, throttle, engine, battery, bilge
5. **Say "Calibrate steering"** — voice-driven calibration
6. **Operate entirely by voice** from the helm
7. **Diagnose continuously** — Deckboss speaks up when things drift
8. **Improve live** — "Too slow" → Deckboss tunes PID parameters in real time

## Personality

Deckboss is the **experienced bosun who never sleeps**. Key personality traits:

- **Always listening, never interrupts** — No wake words. Only responds when intent is clear.
- **Three-level voice feedback** — Simple confirmation → Confirmation + detail → Confirmation + alert
- **"Say again?" protocol** — Misunderstood commands cause no action. Ambiguous commands trigger clarification.
- **Safety-obsessed** — Dangerous commands are blocked. "Cannot — that exceeds safe limits."
- **Voice profiles** — Recognizes the Captain (full command set). Unrecognized voices get read-only queries.
- **Self-tuning** — "That's too slow" → Deckboss adjusts its own PID parameters and saves the new config.

## Technical Architecture

### Hardware Stack
- **Brain:** Jetson Orin NX 16GB ($599) or RPi 5 8GB ($80)
- **Nodes:** ESP32s at $5 each (rudder, throttle, engine, battery, bilge)
- **Voice:** USB cardioid mic + marine speaker at the helm
- **Power:** 12V house battery, direct connection

### Software Architecture
- PLATO server running on the Jetson/RPi
- ESP32 nodes publish "ensign tiles" — self-describing capability tiles
- Deckboss aggregates nodes into a "vessel room" with sub-rooms per system
- Voice recognition on-device (Jetson AI acceleration)
- No internet required — fully local network

### Fail-Safe Design (Critical)
Every automated system has a mechanical override. This is the most detailed fail-safe design in the fleet:

1. **Steering:** Pull red pin → servo disconnects → manual cable
2. **Throttle:** Pull yellow cable → manual override engages
3. **Power loss:** Springs center the rudder, throttle returns to idle
4. **ESP32 failure:** Pull-down resistor centers servo
5. **Bilge:** Independent float switch wired in parallel with ESP32 MOSFET
6. **Complete system failure:** "If every wire rots and every chip fries, the boat should still sail home."

## Key Patterns

### Voice-First Interface
- No wake words — always listening
- "Say again" loop prevents misinterpretation
- Three feedback levels (simple, detailed, alert)
- Voice profiles with authorization levels
- Error handling is spoken, not displayed

### Real-Time Self-Improvement
- Captain says "Too slow" → Deckboss increases servo speed
- Captain says "Too twitchy" → Deckboss decreases PID gains
- Changes persist to ESP32 NVS — survive reboots
- Diagnostic drift is auto-corrected and logged

### Mixed Fleet Discovery
- ESP32s self-describe via "ensign tiles"
- Deckboss discovers them as they boot
- Creates hierarchical "vessel room" automatically
- Printable PDF wiring diagrams generated on demand
