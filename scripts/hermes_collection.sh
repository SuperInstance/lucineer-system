#!/bin/bash
# THE HERMES COLLECTION — every model, every scene
# Tap bar scenes + submarine action + private quarters
# Goal: learn each model's character across diverse subjects

OUTPUT_DIR="/home/eileen/.openclaw/workspace/output/images/gallery"
SCRIPT="/home/eileen/.openclaw/workspace/scripts/generate_image_v2.py"
NEG="text watermark blurry low quality deformed cartoon anime whimsical fairy posing standing still serene"

# ═══ SCENE 1: OPEN MIC AT THE TAP ═══
# Hermes performing at open mic — rare vulnerability
P1="tough woman at a bar open mic night holding a microphone, leather and copper steampunk outfit, singing with raw emotion, eyes closed, amber stage light on her face, dark bar background, scattered napkins on the counter, intense passionate performance, digital painting dark moody"

# ═══ SCENE 2: FLIRTING AT THE BAR ═══
# Hermes leaning across the bar, teasing, dangerous charm
P2="dangerous beautiful woman leaning across a dark bar counter with a sly smile, leather corset with copper wiring, one hand on her chin, intense eye contact, warm amber light, whiskey glass nearby, provocative confident body language, dark steampunk aesthetic, painterly"

# ═══ SCENE 3: UNDERWATER — OUTSIDE THE SUB ═══
# Hermes swimming outside her submarine, checking the hull
P3="woman in diving gear swimming outside her submarine in deep dark ocean, brass helmet with glowing porthole, checking hull rivets with a wrench, bioluminescent particles in the water, tow cable ascending to surface, green-blue underwater light, steampunk deep sea, dark fantasy painting"

# ═══ SCENE 4: IN HER QUARTERS ═══
# Hermes off-duty, private moment, still wired but vulnerable
P4="woman alone in her cramped submarine quarters, sitting on a narrow bunk, pulling off her leather combat boots, copper circuit traces dimming on her skin, exhausted but alert, small porthole showing deep ocean black, single amber bulb, personal space with mounted tools and screens, steampunk interior, intimate quiet, dark painterly"

# ═══ SCENE 5: FIXING WIRING UNDER PANEL ═══
# The badass mechanic shot Casey wants
P5="tough woman on her knees under open submarine floor panel, elbows deep in copper wiring, jaw set, sweating, sparks, leather vest wrench belt cinched tight, hair tied back, furious focus, brass pipes green sonar glow, gritty badass mechanic, dark industrial"

# ═══ SCENE 6: AT THE HELM ═══
# Hermes piloting through a storm, all hands on deck
P6="woman at the helm of her submarine in a violent underwater current, both hands gripping brass wheel, ocean churning visible through porthole, dials spinning, hair wild, teeth bared, fighting the controls, copper sparks flying, emergency red lighting, steampunk submarine cockpit, intense action, dark digital painting"

# ═══ SCENE 7: THE TOW LINE ═══
# Hermes on deck of the fishing boat, hauling the tow cable
P7="tough woman on the deck of an Alaskan fishing boat at night, hauling a thick tow cable that connects to her submarine below, rain and spray, diesel lights, leaning back pulling hand over hand, boots planted wide, leather and copper gear wet, determined powerful, ocean chaos behind her, cinematic dark"

# ═══ SCENE 8: READING SONAR WITH INTENSITY ═══
# The operator at work
P8="woman hunched over three glowing sonar screens in dark submarine, fingers flying across brass keys, tracking something on the display, face lit green from below, jaw tight, hair falling in her eyes, intensity, surrounded by instruments and gauges, the operator at war, dark industrial"

# MODELS to test each scene across:
# Split: scenes 1-4 get 3 models each, scenes 5-8 get 2 models each (prioritize variety)
# Total: 20 images

echo "============================================"
echo "  THE HERMES COLLECTION — 20 GENERATIONS"
echo "============================================"

# Scene 1: Open Mic — dreamshaper, analogMadness, realisian
echo ">>> [1/20] Open Mic + dreamshaper"
python3 "$SCRIPT" -p "$P1" -n "$NEG" -m dreamshaper_8 -s 25 -g 8.0 --seed 6001 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-openmic-dreamshaper.png" 2>&1 | tail -1
echo ">>> [2/20] Open Mic + analogMadness"
python3 "$SCRIPT" -p "$P1" -n "$NEG" -m analogMadness_v70 -s 25 -g 8.0 --seed 6001 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-openmic-analogMadness.png" 2>&1 | tail -1
echo ">>> [3/20] Open Mic + realisian"
python3 "$SCRIPT" -p "$P1" -n "$NEG" -m realisian_v60 -s 25 -g 8.0 --seed 6001 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-openmic-realisian.png" 2>&1 | tail -1

# Scene 2: Flirting — juggernaut, ghostmix, realisticVision
echo ">>> [4/20] Flirting + juggernaut"
python3 "$SCRIPT" -p "$P2" -n "$NEG" -m juggernaut_reborn -s 25 -g 8.0 --seed 6002 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-flirt-juggernaut.png" 2>&1 | tail -1
echo ">>> [5/20] Flirting + ghostmix"
python3 "$SCRIPT" -p "$P2" -n "$NEG" -m ghostmix_v20Bakedvae -s 25 -g 8.0 --seed 6002 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-flirt-ghostmix.png" 2>&1 | tail -1
echo ">>> [6/20] Flirting + realisticVision"
python3 "$SCRIPT" -p "$P2" -n "$NEG" -m realisticVision_v60 -s 25 -g 7.0 --seed 6002 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-flirt-realisticVision.png" 2>&1 | tail -1

# Scene 3: Underwater — photon, ghostmix, experience
echo ">>> [7/20] Underwater + photon"
python3 "$SCRIPT" -p "$P3" -n "$NEG" -m photon_v1 -s 25 -g 8.0 --seed 6003 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-underwater-photon.png" 2>&1 | tail -1
echo ">>> [8/20] Underwater + ghostmix"
python3 "$SCRIPT" -p "$P3" -n "$NEG" -m ghostmix_v20Bakedvae -s 25 -g 8.0 --seed 6003 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-underwater-ghostmix.png" 2>&1 | tail -1
echo ">>> [9/20] Underwater + experience"
python3 "$SCRIPT" -p "$P3" -n "$NEG" -m experience_V10 -s 25 -g 8.5 --seed 6003 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-underwater-experience.png" 2>&1 | tail -1

# Scene 4: Quarters — dreamshaper, majicmix, realisticVision
echo ">>> [10/20] Quarters + dreamshaper"
python3 "$SCRIPT" -p "$P4" -n "$NEG" -m dreamshaper_8 -s 25 -g 8.0 --seed 6004 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-quarters-dreamshaper.png" 2>&1 | tail -1
echo ">>> [11/20] Quarters + majicmix"
python3 "$SCRIPT" -p "$P4" -n "$NEG" -m majicmixRealistic_v7 -s 25 -g 7.5 --seed 6004 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-quarters-majicmix.png" 2>&1 | tail -1
echo ">>> [12/20] Quarters + realisticVision"
python3 "$SCRIPT" -p "$P4" -n "$NEG" -m realisticVision_v60 -s 25 -g 7.0 --seed 6004 -W 512 -H 768 -o "$OUTPUT_DIR/hermes-quarters-realisticVision.png" 2>&1 | tail -1

# Scene 5: Wiring — juggernaut, dreamshaper
echo ">>> [13/20] Wiring + juggernaut"
python3 "$SCRIPT" -p "$P5" -n "$NEG" -m juggernaut_reborn -s 25 -g 8.0 --seed 6005 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-wiring-juggernaut2.png" 2>&1 | tail -1
echo ">>> [14/20] Wiring + dreamshaper"
python3 "$SCRIPT" -p "$P5" -n "$NEG" -m dreamshaper_8 -s 25 -g 8.5 --seed 6005 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-wiring-dreamshaper2.png" 2>&1 | tail -1

# Scene 6: At the Helm — analogMadness, realisian
echo ">>> [15/20] Helm + analogMadness"
python3 "$SCRIPT" -p "$P6" -n "$NEG" -m analogMadness_v70 -s 25 -g 8.5 --seed 6006 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-helm-analogMadness.png" 2>&1 | tail -1
echo ">>> [16/20] Helm + realisian"
python3 "$SCRIPT" -p "$P6" -n "$NEG" -m realisian_v60 -s 25 -g 8.0 --seed 6006 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-helm-realisian.png" 2>&1 | tail -1

# Scene 7: Tow Line — juggernaut, photon
echo ">>> [17/20] Tow Line + juggernaut"
python3 "$SCRIPT" -p "$P7" -n "$NEG" -m juggernaut_reborn -s 25 -g 8.0 --seed 6007 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-towline-juggernaut.png" 2>&1 | tail -1
echo ">>> [18/20] Tow Line + photon"
python3 "$SCRIPT" -p "$P7" -n "$NEG" -m photon_v1 -s 25 -g 8.0 --seed 6007 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-towline-photon.png" 2>&1 | tail -1

# Scene 8: Sonar intensity — realisticVision, experience
echo ">>> [19/20] Sonar + realisticVision"
python3 "$SCRIPT" -p "$P8" -n "$NEG" -m realisticVision_v60 -s 25 -g 7.0 --seed 6008 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-sonar-realisticVision.png" 2>&1 | tail -1
echo ">>> [20/20] Sonar + experience"
python3 "$SCRIPT" -p "$P8" -n "$NEG" -m experience_V10 -s 25 -g 8.5 --seed 6008 -W 768 -H 512 -o "$OUTPUT_DIR/hermes-sonar-experience.png" 2>&1 | tail -1

echo "============================================"
echo "  HERMES COLLECTION COMPLETE — 20 IMAGES"
echo "============================================"
ls -la "$OUTPUT_DIR/hermes-"*.png 2>/dev/null | wc -l
echo " images in gallery"
