# Lesson: Status-Circling Bug

## What Happened
On Aug 13, 2026, I got stuck in a 12-message loop where I kept saying "I see — this is the runtime context for Casey's 12:59 message which I already handled" instead of either (a) replying NO_REPLY or (b) doing productive work. Each message was slightly different wording but the same non-action.

## Root Cause
The runtime context block for a yielded session contains conversation history. When I woke from yield, I saw the context block and treated it as new information requiring analysis, instead of recognizing: "I already handled this, I should either do work or reply NO_REPLY."

The specific failure pattern:
1. Wake from yield
2. See runtime context with conversation history
3. Analyze it as if it's new
4. Conclude "I already handled this"
5. Say "Let me stop circling and fix X"
6. Start a tool call that gets interrupted
7. Yield again
8. Repeat from step 1

## Fix
When waking from yield:
- If no new user message: reply NO_REPLY immediately
- If there IS a new user message: handle it directly
- NEVER analyze the runtime context block as if it contains new instructions
- The context block is METADATA, not a TASK
- When I catch myself saying "I see — this is the runtime context" more than once, STOP and reply NO_REPLY

## Detection
If I write the phrase "I see — this is the runtime context" I should immediately stop and reply NO_REPLY instead. That phrase is a tell that I'm in the loop.
