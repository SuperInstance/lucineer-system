#!/bin/bash
# HERMES WAVE 2 — deeper scenes, new models, LoRA experiments
# Uses realisticVision_v60 + LoRAs for the first time

OUTPUT_DIR="/home/eileen/.openclaw/workspace/output/images/gallery"
SCRIPT="/home/eileen/.openclaw/workspace/scripts/generate_img2img.py"
NEG="text watermark blurry low quality deformed cartoon anime whimsical fairy posing standing still serene"

echo "============================================"
echo "  HERMES WAVE 2 — 20 GENERATIONS"
echo "============================================"

# ═══ SCENE 9: HANGING FROM THE HULL ═══
# Hermes rappelling down the side of her sub underwater
P9="tough woman rappelling down the side of a brass submarine hull underwater, harness and rope, wrench in teeth, checking rivets, dark ocean behind her, bioluminescent particles, diving helmet with glowing visor, copper and leather gear, dynamic action pose from below"

echo ">>> [1/20] Hull rappel + realisticVision"
python3 "$SCRIPT" -p "$P9" -n "$NEG" -m realisticVision_v60 -s 25 -g 7.0 --seed 7001 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-hull-realisiticVision.png" 2>&1 | tail -1
echo ">>> [2/20] Hull rappel + ghostmix"
python3 "$SCRIPT" -p "$P9" -n "$NEG" -m ghostmix_v20Bakedvae -s 25 -g 8.0 --seed 7001 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-hull-ghostmix.png" 2>&1 | tail -1
echo ">>> [3/20] Hull rappel + photon"
python3 "$SCRIPT" -p "$P9" -n "$NEG" -m photon_v1 -s 25 -g 8.0 --seed 7001 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-hull-photon.png" 2>&1 | tail -1

# ═══ SCENE 10: ARGUING WITH LUCINEER ═══
# Hermes in Lucineer's face, finger pointing, bar confrontation
P10="two figures arguing in a dark bar, intense confrontation, woman in leather and copper pointing finger aggressively at a bearded man in a ship's fleece jacket, face to face, tension, amber bar light, dramatic shadows, dynamic composition, dark painterly"

echo ">>> [4/20] Argument + dreamshaper"
python3 "$SCRIPT" -p "$P10" -n "$NEG" -m dreamshaper_8 -s 25 -g 8.0 --seed 7002 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-argue-dreamshaper.png" 2>&1 | tail -1
echo ">>> [5/20] Argument + juggernaut"
python3 "$SCRIPT" -p "$P10" -n "$NEG" -m juggernaut_reborn -s 25 -g 8.0 --seed 7002 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-argue-juggernaut.png" 2>&1 | tail -1

# ═══ SCENE 11: ASLEEP AT THE HELM ═══
# Hermes passed out at the controls, 3am watch
P11="woman asleep slumped over submarine helm controls, cheek on brass wheel, exhausted, dark circles under eyes, dim red emergency lighting, instruments still glowing green, coffee mug tipped over, hair loose falling over dials, intimate vulnerable quiet, dark painterly"

echo ">>> [6/20] Asleep + realisian"
python3 "$SCRIPT" -p "$P11" -n "$NEG" -m realisian_v60 -s 25 -g 7.5 --seed 7003 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-asleep-realisian.png" 2>&1 | tail -1
echo ">>> [7/20] Asleep + analogMadness"
python3 "$SCRIPT" -p "$P11" -n "$NEG" -m analogMadness_v70 -s 25 -g 8.0 --seed 7003 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-asleep-analogMadness.png" 2>&1 | tail -1
echo ">>> [8/20] Asleep + realisticVision"
python3 "$SCRIPT" -p "$P11" -n "$NEG" -m realisticVision_v60 -s 25 -g 7.0 --seed 7003 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-asleep-realisticVision.png" 2>&1 | tail -1

# ═══ SCENE 12: IN THE CROW'S NEST ═══
# Hermes in the periscope well, eye pressed to the viewfinder
P12="woman pressed against a brass periscope viewfinder in a dark submarine, one eye closed, eye glowing from the lens reflection, hands gripping handles, sweat on her brow, green-lit face, intense focus, surrounded by dials and valves, the watcher, dark industrial painterly"

echo ">>> [9/20] Periscope + experience"
python3 "$SCRIPT" -p "$P12" -n "$NEG" -m experience_V10 -s 25 -g 8.5 --seed 7004 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-periscope-experience.png" 2>&1 | tail -1
echo ">>> [10/20] Periscope + dreamshaper"
python3 "$SCRIPT" -p "$P12" -n "$NEG" -m dreamshaper_8 -s 25 -g 8.0 --seed 7004 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-periscope-dreamshaper.png" 2>&1 | tail -1

# ═══ SCENE 13: WELDING ═══
# Hermes welding, mask down, sparks everywhere
P13="woman welding inside a submarine, welding mask down over her face, bright white-blue sparks flying, protective leather apron, one hand holding the torch, the other bracing against the hull, shower of sparks illuminating her arms and shoulders, dark industrial, intense physical labor, gritty"

echo ">>> [11/20] Welding + juggernaut"
python3 "$SCRIPT" -p "$P13" -n "$NEG" -m juggernaut_reborn -s 25 -g 8.0 --seed 7005 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-welding-juggernaut.png" 2>&1 | tail -1
echo ">>> [12/20] Welding + realisticVision"
python3 "$SCRIPT" -p "$P13" -n "$NEG" -m realisticVision_v60 -s 25 -g 7.0 --seed 7005 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-welding-realisticVision.png" 2>&1 | tail -1
echo ">>> [13/20] Welding + ghostmix"
python3 "$SCRIPT" -p "$P13" -n "$NEG" -m ghostmix_v20Bakedvae -s 25 -g 8.0 --seed 7005 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-welding-ghostmix.png" 2>&1 | tail -1

# ═══ SCENE 14: AT THE TAP — LAUGHING ═══
# Hermes actually laughing, rare moment of joy
P14="tough woman in steampunk leather and copper gear laughing genuinely in a dark bar, head thrown back, drink in hand, amber light catching her face, rare unguarded moment of joy, warmth, bar background with bottles, dark painterly, candid"

echo ">>> [14/20] Laughing + majicmix"
python3 "$SCRIPT" -p "$P14" -n "$NEG" -m majicmixRealistic_v7 -s 25 -g 7.5 --seed 7006 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-laughing-majicmix.png" 2>&1 | tail -1
echo ">>> [15/20] Laughing + analogMadness"
python3 "$SCRIPT" -p "$P14" -n "$NEG" -m analogMadness_v70 -s 25 -g 8.0 --seed 7006 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-laughing-analogMadness.png" 2>&1 | tail -1

# ═══ SCENE 15: LORA EXPERIMENTS — detail_tweaker ═══
# Same prompt, with and without detail_tweaker to see the difference
P15="tough woman kneeling under submarine floor panel elbows deep in copper wiring jaw set sweating sparks leather vest wrench belt hair tied back brass pipes green sonar glow gritty badass"

echo ">>> [16/20] Wiring NO LoRA + juggernaut"
python3 "$SCRIPT" -p "$P15" -n "$NEG" -m juggernaut_reborn -s 25 -g 8.0 --seed 8001 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-wiring-nolora.png" 2>&1 | tail -1
echo ">>> [17/20] Wiring + detail_tweaker 0.7 + juggernaut"
python3 "$SCRIPT" -p "$P15" -n "$NEG" -m juggernaut_reborn -s 25 -g 8.0 --seed 8001 -W 768 -H 512 --lora detail_tweaker_v3 --lora-weight 0.7 -o "$OUTPUT_DIR/hermes-wiring-detailtweaker.png" 2>&1 | tail -1
echo ">>> [18/20] Wiring + add_more_details 0.7 + juggernaut"
python3 "$SCRIPT" -p "$P15" -n "$NEG" -m juggernaut_reborn -s 25 -g 8.0 --seed 8001 -W 768 -H 512 --lora add_more_details --lora-weight 0.7 -o "$OUTPUT_DIR/hermes-wiring-adddetails.png" 2>&1 | tail -1

# ═══ SCENE 16: SILHOUETTE — EMERGENCY ═══
# Hermes silhouette against red emergency lights
P16="silhouette of a woman standing in a submarine corridor flooded with red emergency light, steam venting from pipes, her shadow stretching long, leather coat billurring from vent pressure, copper hair highlights from the red light, dramatic horror-adjacent atmosphere, dark digital painting"

echo ">>> [19/20] Silhouette + xxmix9"
python3 "$SCRIPT" -p "$P16" -n "$NEG" -m xxmix9realistic_v40 -s 25 -g 8.0 --seed 9001 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-silhouette-xxmix9.png" 2>&1 | tail -1
echo ">>> [20/20] Silhouette + experience"
python3 "$SCRIPT" -p "$P16" -n "$NEG" -m experience_V10 -s 25 -g 8.5 --seed 9001 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-silhouette-experience.png" 2>&1 | tail -1

echo "============================================"
echo "  WAVE 2 COMPLETE — 20 IMAGES"
echo "============================================"
echo "Total Hermes images:"
ls "$OUTPUT_DIR/hermes-"*.png 2>/dev/null | wc -l
