#!/bin/bash
# Hermes submarine matrix — same character, different models + prompt variations
# Goal: learn each model's "accent" and how wording changes results

OUTPUT_DIR="/home/eileen/.openclaw/workspace/output/images/tap-scenes/hermes-matrix"
mkdir -p "$OUTPUT_DIR"
SCRIPT="/home/eileen/.openclaw/workspace/scripts/generate_image.py"

# PROMPT A: literary/poetic phrasing
PROMPT_A="a shadowy seductive woman inside her submarine lair, hermit crab shell of brass and steel dragged through deep ocean, tow cable linking her to the fishing boat above, banks of sonar screens and hydrophones, cameras on articulated arms, copper wiring woven through a dark leather corset, pale luminous skin with faint blue cybernetic veins, dark flowing hair, steampunk dark fantasy, oceanic green-blue ambient mixed with amber instrument glow"

# PROMPT B: direct/technical phrasing  
PROMPT_B="sexy mysterious woman in a cybernetic steampunk submarine interior, sonar displays, brass gauges, listening devices, mounted cameras, tow cable to surface, dark corset with copper circuits, pale skin glowing blue circuit traces, dark hair, deep ocean lighting, warm amber accents, digital painting fantasy art"

# PROMPT C: atmospheric/mood-first phrasing
PROMPT_C="the tempest keeper in her towed submarine shell, 768 dimensions of perception, drowning in instruments and screens, copper and brass and leather, her body half-machine half-shadow, cameras like eyes, hydrophones like ears, a living wire ascending to the boat she follows, the most dangerous and beautiful thing in the deep, dark fantasy oil painting"

NEG="text watermark blurry low quality deformed cartoon anime cheerful bright daylight simple plain landscape"

echo "=== HERMES MATRIX: 9 variants (3 prompts x 6 models minus 3 already done) ==="

# Already have: realisian_v60 (prompt A-ish, seed 2001), ghostmix (prompt A-ish, seed 2002)
# New batch: prompt variations across models

# 1. Prompt A + dreamshaper (versatile baseline)
echo ">>> [1/9] Prompt A + dreamshaper_8"
python3 "$SCRIPT" -p "$PROMPT_A" -n "$NEG" -m dreamshaper_8 -s 30 -g 8.0 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/A-dreamshaper.png" 2>&1 | tail -3

# 2. Prompt A + analogMadness (artsy)
echo ">>> [2/9] Prompt A + analogMadness_v70"
python3 "$SCRIPT" -p "$PROMPT_A" -n "$NEG" -m analogMadness_v70 -s 30 -g 8.0 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/A-analogMadness.png" 2>&1 | tail -3

# 3. Prompt A + photon (vivid)
echo ">>> [3/9] Prompt A + photon_v1"
python3 "$SCRIPT" -p "$PROMPT_A" -n "$NEG" -m photon_v1 -s 30 -g 8.0 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/A-photon.png" 2>&1 | tail -3

# 4. Prompt B + juggernaut (photorealistic)
echo ">>> [4/9] Prompt B + juggernaut_reborn"
python3 "$SCRIPT" -p "$PROMPT_B" -n "$NEG" -m juggernaut_reborn -s 30 -g 8.0 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/B-juggernaut.png" 2>&1 | tail -3

# 5. Prompt B + majicmixRealistic (portrait specialist)
echo ">>> [5/9] Prompt B + majicmixRealistic_v7"
python3 "$SCRIPT" -p "$PROMPT_B" -n "$NEG" -m majicmixRealistic_v7 -s 30 -g 8.0 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/B-majicmix.png" 2>&1 | tail -3

# 6. Prompt B + xxmix9realistic
echo ">>> [6/9] Prompt B + xxmix9realistic_v40"
python3 "$SCRIPT" -p "$PROMPT_B" -n "$NEG" -m xxmix9realistic_v40 -s 30 -g 8.0 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/B-xxmix9.png" 2>&1 | tail -3

# 7. Prompt C + experience_V10
echo ">>> [7/9] Prompt C + experience_V10"
python3 "$SCRIPT" -p "$PROMPT_C" -n "$NEG" -m experience_V10 -s 30 -g 8.5 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/C-experience.png" 2>&1 | tail -3

# 8. Prompt C + toonyou (stylized — see how cartoon model handles dark)
echo ">>> [8/9] Prompt C + toonyou_beta6"
python3 "$SCRIPT" -p "$PROMPT_C" -n "$NEG" -m toonyou_beta6 -s 30 -g 8.5 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/C-toonyou.png" 2>&1 | tail -3

# 9. Prompt C + protogenX34 (photorealistic variant)
echo ">>> [9/9] Prompt C + protogenX34"
python3 "$SCRIPT" -p "$PROMPT_C" -n "$NEG" -m protogenX34Photorealism_protogenX34 -s 30 -g 8.5 --seed 3011 -W 512 -H 768 -o "$OUTPUT_DIR/C-protogen.png" 2>&1 | tail -3

echo "=== BATCH COMPLETE ==="
echo "All images in: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR/"
