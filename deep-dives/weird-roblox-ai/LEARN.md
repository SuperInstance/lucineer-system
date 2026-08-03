# Lessons Learned — Weird Roblox AI Bot Study

## Primary Lesson: Don't Trust READMEs

This project's README lists 11 Python dependencies (OpenCV, TensorFlow, pytesseract, scikit-learn, numpy, pyautogui, win32gui) — **7 of which are never imported in the actual code**. The README describes capabilities (AI, vision, OCR) that simply don't exist in the source.

**Action:** Always read the actual source code before evaluating a project's capabilities. A dependency list in a README is a wish list, not a contract.

## Secondary Lesson: Python Function Shadowing Bug

The author defined `key_press_loop` twice inside `start_key_press`. The second definition (without chat) silently replaced the first (with chat). ~80 lines of elaborate chat probability tables became dead code instantly.

**Action:** Use a linter that catches duplicate nested function definitions (pylint R8201 or equivalent). Also prefer named methods over nested functions for complex logic.

## Tertiary Lesson: Aspirational Naming

Calling a random keystroke script "AIPlaysRoblox" inflates expectations and wastes evaluator time. The gap between name/README and actual capability was enormous.

**Action:** When naming our own projects, under-promise and over-deliver. "KeystrokeAutomation" would have been honest. "AIPlaysRoblox" was misleading.

## What We Got Out of It (Minimal)

1. **Chat personality weighting concept:** The idea of categorizing utterances by vibe (normal, creepy, absurdist) with different probability weights is worth folding into Lucineer's personality engine design. Not the code — just the concept.

2. **Realistic typing cadence:** `keyboard.press_and_release(char)` with `random.uniform(0.05, 0.1)` jitter per character. Small but useful for naturalistic chat output.

3. **Action space enumeration:** The 26 movement combinations (singles, pairs, triples with timing ranges) serve as a useful reference for what a basic Roblox action space looks like. We'd map these to cognition-driven selection rather than random.

## What This Project Did NOT Teach Us

- Nothing about screen capture pipelines
- Nothing about YOLO or object detection
- Nothing about OCR or UI reading
- Nothing about game state inference
- Nothing about closed-loop control
- Nothing about LLM integration
- Nothing about memory or state management

## Next Steps for Vision Layer Research

This project contributed nothing to the vision system. The search for a vision layer reference continues. Priorities:

1. **Screen capture pipeline:** `mss` or `dxcam` for high-FPS framebuffer access
2. **Object detection:** YOLOv8/v10 fine-tuned on Roblox screenshots for player, NPC, obstacle detection
3. **UI reading:** EasyOCR or Tesseract for health bars, scores, chat, minimap labels
4. **Depth/segmentation:** DepthAnything or MiDaS for pseudo-depth from screen captures
5. **Action mapping:** Translate cognition decisions → keyboard/mouse via `pynput` (thread-safe) or our existing input bridge
