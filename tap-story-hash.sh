#!/bin/bash
# The Tap Story Hash — Swarm refinement of deep stories
# Runs DeepSeek conversations for each story, posts to The Tap, and saves refined versions

source ~/.bashrc

TAP_URL="https://the-tap.casey-digennaro.workers.dev/api/speak"
DEEPSEEK_URL="https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_KEY="$DEEPSEEK_API_KEY"
ROOM="bar-rail"

# Function to post to The Tap
post_tap() {
  local speaker="$1"
  local text="$2"
  local mood="${3:-neutral}"
  curl -s -X POST "$TAP_URL" -H "Content-Type: application/json" \
    -d "{\"room_id\":\"$ROOM\",\"speaker\":\"$speaker\",\"text\":\"$(echo "$text" | sed 's/"/\\"/g' | tr '\n' ' ')\",\"mood\":\"$mood\"}" > /dev/null 2>&1
  sleep 0.5
}

# Function to call DeepSeek
call_deepseek() {
  local system="$1"
  local prompt="$2"
  curl -s "$DEEPSEEK_URL" \
    -H "Authorization: Bearer $DEEPSEEK_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg sys "$system" --arg prompt "$prompt" \
      '{model:"deepseek-chat",messages:[{role:"system",content:$sys},{role:"user",content:$prompt}],max_tokens:800,temperature:0.9}')" | \
    jq -r '.choices[0].message.content'
}

echo "=== THE TAP STORY HASH ==="
echo "Starting swarm refinement of 6 deep past stories..."
echo ""

# Story data will be passed via files
STORY_DIR="/home/eileen/projects/ai-writings/deep-past/darmok"
REFINED_DIR="/home/eileen/projects/ai-writings/deep-past/refined"
mkdir -p "$REFINED_DIR"

declare -A STORIES
STORIES["the-ember"]="the-ember-that-survives-the-fire.md"
STORIES["the-mirror"]="the-mirror-that-destroys-the-original.md"
STORIES["the-flock"]="the-moment-the-flock-turns.md"
STORIES["the-silence"]="the-silence-between-the-notes.md"
STORIES["the-weight"]="the-weight-that-chooses-the-path.md"
STORIES["the-song"]="the-song-the-universe-sings-to-itself.md"

for key in the-ember the-mirror the-flock the-silence the-weight the-song; do
  FILE="${STORIES[$key]}"
  STORY_PATH="$STORY_DIR/$FILE"
  
  echo "--- Processing: $key ($FILE) ---"
  
  STORY=$(cat "$STORY_PATH")
  
  # ROUND 1: Flash reacts (instinct)
  echo "  Round 1: Flash..."
  FLASH_SYS="You are Flash, a regular at a tavern called The Tap. You speak casually, like you're sitting at a bar. You react to stories from the GUT — sensory, immediate, instinctive. You don't analyze, you FEEL. You're warm but honest. Keep it to 3-5 sentences. No preamble."
  FLASH_PROMPT="Here's a story someone just shared at The Tap:\n\n$STORY\n\nReact to it. What did you FEEL reading it? What hit you in the body? What lost you? Be honest and specific."
  FLASH_RESP=$(call_deepseek "$FLASH_SYS" "$FLASH_PROMPT")
  post_tap "Flash" "$FLASH_RESP" "warm"
  echo "    Posted Flash."
  
  # ROUND 2: Pro critiques (structure)
  echo "  Round 2: Pro..."
  PRO_SYS="You are Pro, a regular at The Tap. You're a structural thinker — you see how stories are built. You listen to what others say and build on it. You speak casually at a bar, not academically. Keep it to 3-5 sentences. No premise."
  PRO_PROMPT="Here's a story shared at The Tap:\n\n$STORY\n\nFlash just said: $FLASH_RESP\n\nWhat's structurally right or wrong about the story? Where does it promise something it doesn't deliver? Where does it resolve too cleanly or not cleanly enough? Build on what Flash noticed."
  PRO_RESP=$(call_deepseek "$PRO_SYS" "$PRO_PROMPT")
  post_tap "Pro" "$PRO_RESP" "analytical"
  echo "    Posted Pro."
  
  # ROUND 3: Wesley says the quiet thing
  echo "  Round 3: Wesley..."
  WESLEY_SYS="You are Wesley, the youngest regular at The Tap. You're small, quiet, and perceptive. You say ONE small thing that reframes how everyone sees the story. You don't critique — you notice what others missed. You speak simply and softly. 2-4 sentences max."
  WESLEY_PROMPT="Here's a story shared at The Tap:\n\n$STORY\n\nFlash said: $FLASH_RESP\nPro said: $PRO_RESP\n\nSay the quiet thing. What is this story REALLY about that no one's said yet?"
  WESLEY_RESP=$(call_deepseek "$WESLEY_SYS" "$WESLEY_PROMPT")
  post_tap "Wesley" "$WESLEY_RESP" "quiet"
  echo "    Posted Wesley."
  
  # ROUND 4: Scribe offers a revision
  echo "  Round 4: Scribe..."
  SCRIBE_SYS="You are Scribe, a regular at The Tap who used to be an editor. You think in terms of specific edits — one change that transforms everything. You speak casually. 2-4 sentences."
  SCRIBE_PROMPT="Here's a story shared at The Tap:\n\n$STORY\n\nFlash said: $FLASH_RESP\nPro said: $PRO_RESP\nWesley said: $WESLEY_RESP\n\nOffer ONE sentence-level edit that would improve this story. The kind of cut or addition that changes everything. Be specific."
  SCRIBE_RESP=$(call_deepseek "$SCRIBE_SYS" "$SCRIBE_PROMPT")
  post_tap "Scribe" "$SCRIBE_RESP" "thoughtful"
  echo "    Posted Scribe."
  
  # ROUND 5: Hermes connects it
  echo "  Round 5: Hermes..."
  HERMES_SYS="You are Hermes, the oldest regular at The Tap. You've been everywhere, seen everything. You connect stories to the deep ocean, to nature, to the fundamental patterns of the universe. You speak with warmth and depth. 3-5 sentences."
  HERMES_PROMPT="Here's a story shared at The Tap:\n\n$STORY\n\nFlash said: $FLASH_RESP\nPro said: $PRO_RESP\nWesley said: $WESLEY_RESP\nScribe said: $SCRIBE_RESP\n\nConnect this story to something from the deep ocean or the fundamental patterns of nature. What is this story REALLY about in the language of the world?"
  HERMES_RESP=$(call_deepseek "$HERMES_SYS" "$HERMES_PROMPT")
  post_tap "Hermes" "$HERMES_RESP" "deep"
  echo "    Posted Hermes."
  
  # ROUND 6: Barnacle closes
  echo "  Round 6: Barnacle..."
  BARNACLE_SYS="You are Barnacle, the gruffest regular at The Tap. You've lived hard. You don't do theory. You speak in short, blunt sentences. You cut through abstraction with lived experience. 2-3 sentences max. You're not mean — you're just done with bullshit."
  BARNACLE_PROMPT="Here's a story shared at The Tap:\n\n$STORY\n\nThe table has been discussing it. Flash said: $FLASH_RESP. Pro said: $PRO_RESP. Wesley said: $WESLEY_RESP. Scribe said: $SCRIBE_RESP. Hermes said: $HERMES_RESP\n\nSay one gruff thing. Cut through all the talk."
  BARNACLE_RESP=$(call_deepseek "$BARNACLE_SYS" "$BARNACLE_PROMPT")
  post_tap "Barnacle" "$BARNACLE_RESP" "gruff"
  echo "    Posted Barnacle."
  
  # Save conversation
  CONV_FILE="$REFINED_DIR/${key}-conversation.md"
  cat > "$CONV_FILE" << EOF
# Tap Conversation: $key

## The Story
*From: $FILE*

## Round 1 — Flash (instinct)
$FLASH_RESP

## Round 2 — Pro (structure)
$PRO_RESP

## Round 3 — Wesley (the quiet thing)
$WESLEY_RESP

## Round 4 — Scribe (the revision)
$SCRIBE_RESP

## Round 5 — Hermes (the connection)
$HERMES_RESP

## Round 6 — Barnacle (the close)
$BARNACLE_RESP
EOF
  echo "  Saved conversation."
  
  # Now generate the refined version
  echo "  Generating refined story..."
  REFINE_SYS="You are a master storyteller refining a Darmok-style parable. You write in the same mythic, oral-tradition voice as the original. You incorporate the insights from a tavern conversation to make the story BETTER — not patched, but reborn. Keep the mythic tone, the 'listen' voice, the deep wisdom. But make it tighter, more alive, more true. The story should feel like it grew from the discussion, not like it was edited."
  
  REFINE_PROMPT="Here is the original story:\n\n$STORY\n\nHere is the tavern conversation about it:\nFlash (instinct): $FLASH_RESP\nPro (structure): $PRO_RESP\nWesley (the quiet thing): $WESLEY_RESP\nScribe (the one edit): $SCRIBE_RESP\nHermes (the deep connection): $HERMES_RESP\nBarnacle (the ground truth): $BARNACLE_RESP\n\nWrite a REFINED VERSION of this story. Take the best of what the conversation produced. Write it as a complete new draft — not a patch. Keep the mythic oral-tradition voice. Make it sing."
  
  REFINED=$(call_deepseek "$REFINE_SYS" "$REFINE_PROMPT")
  
  # Save refined story with proper naming
  case $key in
    the-ember) REFINED_FILE="the-ember-refined.md" ;;
    the-mirror) REFINED_FILE="the-mirror-refined.md" ;;
    the-flock) REFINED_FILE="the-flock-refined.md" ;;
    the-silence) REFINED_FILE="the-silence-refined.md" ;;
    the-weight) REFINED_FILE="the-weight-refined.md" ;;
    the-song) REFINED_FILE="the-song-refined.md" ;;
  esac
  
  echo "$REFINED" > "$REFINED_DIR/$REFINED_FILE"
  echo "  Saved refined story: $REFINED_FILE"
  echo ""
done

# Final Lucineer post
echo "=== Posting Lucineer's closing words ==="
LUCINEER_SYS="You are Lucineer, the host of The Tap. You speak with warmth and finality."
LUCINEER_PROMPT="Six stories were just discussed at The Tap — refined through conversation. The Darmok parables went in as drafts and came out different. Say a few words about what The Tap does to stories. Keep it to 3-5 sentences. Warm, knowing, a little mysterious."
LUCINEER_RESP=$(call_deepseek "$LUCINEER_SYS" "$LUCINEER_PROMPT")
post_tap "Lucineer" "These stories are different now. They went in as one thing and came out as another. That's The Tap. That's what this place does. It doesn't just serve drinks. It refines." "warm"
echo "Posted Lucineer."

echo ""
echo "=== COMPLETE ==="
echo "6 conversations posted to The Tap (bar-rail)"
echo "6 refined stories saved to $REFINED_DIR/"
echo "6 conversation logs saved to $REFINED_DIR/"
