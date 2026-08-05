#!/bin/bash
# GPU Training Loop — Granite 3.1 2B on RTX 4050
# Continuously trains on SuperInstance codebase

set -euo pipefail

OLLAMA="/home/eileen/.local/bin/ollama"
MODEL="granite3.1-dense:2b"
OUTDIR="/home/eileen/.openclaw/workspace/gpu-training"
CORPUS="/home/eileen/.openclaw/workspace/gpu-training/file_corpus.txt"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
PREV_RESPONSE=""
PREV_FILE=""

# Topics cycle
TOPICS=(
    "Review this code for bugs, edge cases, and improvements. Focus on: nil checks, type errors, off-by-one errors, and unhandled exceptions."
    "Analyze this code's architecture. How does it connect to other modules? What design patterns are used? Suggest improvements to the interface."
    "Review for performance: identify hot paths, memory issues, unnecessary allocations, and suggest optimizations."
    "Generate comprehensive test cases for this code. Include edge cases, error conditions, and integration scenarios."
    "Analyze this code for race conditions, concurrency issues, and thread safety problems. Suggest fixes."
    "Review this code's error handling. Are errors propagated correctly? Are there silent failures? What about retry logic?"
    "Compare this code's patterns to typical Python/Lua best practices. What would you change? Be specific."
    "Generate creative ideas: what new modules or features could extend this codebase? What's missing?"
)

TOPIC_IDX=0
ITER=0
TOTAL_ITERATIONS=35

echo "[GPU-TRAINING] Starting training loop at $(date)"
echo "[GPU-TRAINING] Model: $MODEL | Iterations: $TOTAL_ITERATIONS"
echo "[GPU-TRAINING] Output: $OUTDIR"
echo "========================================================"

while [ $ITER -lt $TOTAL_ITERATIONS ]; do
    ITER=$((ITER + 1))
    
    # Pick a file (cycle through corpus with offset for variety)
    FILELIST=()
    while IFS= read -r line; do
        [ -n "$line" ] && FILELIST+=("$line")
    done < "$CORPUS"
    
    NUM_FILES=${#FILELIST[@]}
    PICK_IDX=$(( (ITER * 7 + TOPIC_IDX) % NUM_FILES ))
    SOURCE_FILE="${FILELIST[$PICK_IDX]}"
    
    # Handle the typo'd path
    if [[ "$SOURCE_FILE" == *slucineer* ]]; then
        SOURCE_FILE="${SOURCE_FILE/slucineer/lucineer}"
    fi
    
    if [ ! -f "$SOURCE_FILE" ]; then
        echo "[ITER $ITER] File not found: $SOURCE_FILE — skipping"
        continue
    fi
    
    FILENAME=$(basename "$SOURCE_FILE")
    TS=$(date +%Y%m%d-%H%M%S)
    OUTPUT_FILE="$OUTDIR/${TS}_${FILENAME%..*}_iter${ITER}.md"
    
    # Get current topic
    TOPIC="${TOPICS[$TOPIC_IDX]}"
    
    # Build the prompt
    CODE=$(cat "$SOURCE_FILE")
    
    # Truncate very large files to fit context
    MAX_CHARS=8000
    CODE_LEN=${#CODE}
    if [ $CODE_LEN -gt $MAX_CHARS ]; then
        CODE="${CODE:0:$MAX_CHARS}
... [truncated, original was $CODE_LEN chars]"
    fi
    
    if [ -n "$PREV_RESPONSE" ] && [ $ITER -gt 1 ]; then
        # Chained prompt: use previous review as context
        PREV_SUMMARY=$(echo "$PREV_RESPONSE" | head -20)
        PROMPT="You previously reviewed code and found these key insights:
$PREV_SUMMARY

Now, using those insights as context, $TOPIC

File: $SOURCE_FILE
\`\`\`
$CODE
\`\`\`

Provide a detailed, specific analysis. Reference your previous findings where relevant."
    else
        PROMPT="$TOPIC

File: $SOURCE_FILE
\`\`\`
$CODE
\`\`\`

Provide a detailed, specific analysis."
    fi
    
    echo "[ITER $ITER/$TOTAL_ITERATIONS] Topic: ${TOPIC:0:60}..."
    echo "[ITER $ITER] File: $SOURCE_FILE"
    echo "[ITER $ITER] Output: $OUTPUT_FILE"
    
    # Run Granite
    RESPONSE=$($OLLAMA run "$MODEL" "$PROMPT" 2>&1) || {
        echo "[ITER $ITER] ERROR: $RESPONSE"
        RESPONSE="[ERROR] Ollama call failed: $RESPONSE"
    }
    
    # Save response
    {
        echo "# GPU Training Iteration $ITER"
        echo "**Date:** $(date)"
        echo "**Model:** $MODEL"
        echo "**Source:** \`$SOURCE_FILE\`"
        echo "**Topic:** ${TOPIC:0:80}..."
        echo "**Chained from:** ${PREV_FILE:-none}"
        echo ""
        echo "---"
        echo ""
        echo "$RESPONSE"
    } > "$OUTPUT_FILE"
    
    echo "[ITER $ITER] Complete. Response: ${#RESPONSE} chars"
    
    # Store for chaining
    PREV_RESPONSE="$RESPONSE"
    PREV_FILE="$SOURCE_FILE"
    
    # Cycle topic
    TOPIC_IDX=$(( (TOPIC_IDX + 1) % ${#TOPICS[@]} ))
    
    # Summary every 5 iterations
    if [ $((ITER % 5)) -eq 0 ]; then
        echo "[ITER $ITER] Writing 5-iteration summary..."
        SUMMARY_FILE="$OUTDIR/LATEST.md"
        {
            echo "# GPU Training Progress — $(date)"
            echo ""
            echo "## Status"
            echo "- **Iterations completed:** $ITER / $TOTAL_ITERATIONS"
            echo "- **Model:** $MODEL (Granite 3.1 Dense 2B)"
            echo "- **GPU:** RTX 4050"
            echo "- **Last file reviewed:** \`$SOURCE_FILE\`"
            echo ""
            echo "## Recent Iterations"
            echo ""
            # List recent output files
            for f in $(ls -t "$OUTDIR"/[0-9]*.md 2>/dev/null | head -5); do
                fname=$(basename "$f")
                head -8 "$f" | grep -E "^\*\*(Source|Topic)" || true
                echo ""
            done
            echo ""
            echo "## Key Findings So Far"
            echo ""
            # Extract key findings from recent responses
            for f in $(ls -t "$OUTDIR"/[0-9]*.md 2>/dev/null | head -5); do
                echo "### $(basename "$f")"
                # Pull first few substantive lines after the header
                sed -n '/^---$/,/^### /p' "$f" | head -15
                echo ""
            done
            echo ""
            echo "## Files in Corpus"
            echo "- Total files: $NUM_FILES"
            echo "- Topics cycled: $((ITER % ${#TOPICS[@]})) of ${#TOPICS[@]}"
            echo ""
            echo "---"
            echo "_Auto-generated by GPU Training Agent_"
        } > "$SUMMARY_FILE"
        echo "[ITER $ITER] Summary saved to $SUMMARY_FILE"
    fi
    
    # Brief pause to let GPU breathe
    sleep 1
done

echo "========================================================"
echo "[GPU-TRAINING] Training loop complete at $(date)"
echo "[GPU-TRAINING] Total iterations: $ITER"
echo "[GPU-TRAINING] Files produced: $(ls -1 "$OUTDIR"/[0-9]*.md 2>/dev/null | wc -l)"

# Final summary
{
    echo "# GPU Training COMPLETE — $(date)"
    echo ""
    echo "## Final Stats"
    echo "- **Total iterations:** $ITER"
    echo "- **Files reviewed:** $(ls -1 "$OUTDIR"/[0-9]*.md 2>/dev/null | wc -l)"
    echo "- **Model:** $MODEL"
    echo "- **Duration:** Started at $TIMESTAMP, ended $(date)"
    echo ""
    echo "## All Output Files"
    ls -1 "$OUTDIR"/[0-9]*.md 2>/dev/null | while read f; do
        echo "- \`$(basename "$f")\`"
    done
    echo ""
    echo "_Training session complete._"
} > "$OUTDIR/FINAL_SUMMARY.md"

echo "[GPU-TRAINING] Final summary saved."
