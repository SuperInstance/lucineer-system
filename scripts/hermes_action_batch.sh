#!/bin/bash
# Hermes in motion — working her submarine, not posing
# Same character bible, different actions + models to learn the matrix

OUTPUT_DIR="/home/eileen/.openclaw/workspace/output/images/tap-scenes/hermes-action"
mkdir -p "$OUTPUT_DIR"
SCRIPT="/home/eileen/.openclaw/workspace/scripts/generate_image.py"
NEG="text watermark blurry low quality deformed cartoon anime cheerful bright daylight simple plain landscape posing standing still static"

# ACTION 1: Sonar reading — leaning over glowing screens, intensity
P1="a woman in a dark steampunk submarine cockpit leaning over a glowing sonar screen, reading data with intense focus, one hand on brass dial, other hand tracing a contact on the display, copper wiring woven through dark leather corset, pale skin blue circuit traces glowing, dark hair falling forward, cameras on mechanical arms behind her, hydrophone cables, tow line, ocean blue-green and amber gauge light, dark fantasy, dynamic action pose, working not posing"

# ACTION 2: Camera rig — adjusting a mechanical camera arm, physical
P2="cybernetic woman aboard her towed submarine vessel reaching up to adjust a heavy brass camera mounted on a mechanical arm, face lit by the viewfinder glow, focused expression, leather and copper steampunk outfit, circuit traces on pale skin, listening devices with needle dials around her, tow cable taut through a deck hatch, deep blue ocean ambient, amber warm spots, in motion, working, dark fantasy digital painting"

# ACTION 3: Cable work — hands on the thick tow cable, connection to the boat
P3="mysterious woman gripping a thick tow cable that runs from her submarine through a deck hatch up to the fishing boat above, pulling it hand over hand, checking the connection, brass comm-wires sparking faintly, wind in her dark hair from the hatch, wearing leather and copper steampunk gear, sonar screens glowing behind her, cameras watching, dynamic physical labor, ocean spray, dark fantasy painting, energetic"

echo "=== HERMES ACTION MATRIX: 9 variants ==="

echo ">>> [1/9] Sonar reading + dreamshaper_8"
python3 "$SCRIPT" -p "$P1" -n "$NEG" -m dreamshaper_8 -s 30 -g 8.0 --seed 4001 -W 512 -H 768 -o "$OUTPUT_DIR/sonar-dreamshaper.png" 2>&1 | tail -3

echo ">>> [2/9] Sonar reading + realisian_v60"
python3 "$SCRIPT" -p "$P1" -n "$NEG" -m realisian_v60 -s 30 -g 8.0 --seed 4001 -W 512 -H 768 -o "$OUTPUT_DIR/sonar-realisian.png" 2>&1 | tail -3

echo ">>> [3/9] Sonar reading + ghostmix_v20"
python3 "$SCRIPT" -p "$P1" -n "$NEG" -m ghostmix_v20Bakedvae -s 30 -g 8.0 --seed 4001 -W 512 -H 768 -o "$OUTPUT_DIR/sonar-ghostmix.png" 2>&1 | tail -3

echo ">>> [4/9] Camera rig + juggernaut_reborn"
python3 "$SCRIPT" -p "$P2" -n "$NEG" -m juggernaut_reborn -s 30 -g 8.0 --seed 4002 -W 512 -H 768 -o "$OUTPUT_DIR/camera-juggernaut.png" 2>&1 | tail -3

echo ">>> [5/9] Camera rig + analogMadness_v70"
python3 "$SCRIPT" -p "$P2" -n "$NEG" -m analogMadness_v70 -s 30 -g 8.5 --seed 4002 -W 512 -H 768 -o "$OUTPUT_DIR/camera-analogMadness.png" 2>&1 | tail -3

echo ">>> [6/9] Camera rig + photon_v1"
python3 "$SCRIPT" -p "$P2" -n "$NEG" -m photon_v1 -s 30 -g 8.0 --seed 4002 -W 512 -H 768 -o "$OUTPUT_DIR/camera-photon.png" 2>&1 | tail -3

echo ">>> [7/9] Cable work + majicmixRealistic_v7"
python3 "$SCRIPT" -p "$P3" -n "$NEG" -m majicmixRealistic_v7 -s 30 -g 8.0 --seed 4003 -W 512 -H 768 -o "$OUTPUT_DIR/cable-majicmix.png" 2>&1 | tail -3

echo ">>> [8/9] Cable work + xxmix9realistic_v40"
python3 "$SCRIPT" -p "$P3" -n "$NEG" -m xxmix9realistic_v40 -s 30 -g 8.0 --seed 4003 -W 512 -H 768 -o "$OUTPUT_DIR/cable-xxmix9.png" 2>&1 | tail -3

echo ">>> [9/9] Cable work + experience_V10"
python3 "$SCRIPT" -p "$P3" -n "$NEG" -m experience_V10 -s 30 -g 8.5 --seed 4003 -W 512 -H 768 -o "$OUTPUT_DIR/cable-experience.png" 2>&1 | tail -3

echo "=== BATCH COMPLETE ==="
ls -la "$OUTPUT_DIR/"
