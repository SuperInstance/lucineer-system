# Wesley's LoRA — The Sleep Protocol

*Casey's directive: everything on SuperInstance is potential training data. The ai-writings are desk notes. The LoRA is sleep. The model wakes with the knowledge but without the context window.*

---

## The Architecture of Dreams

### Day (Context Window)
Wesley is awake. His context window holds:
- 3 random ai-writings pieces (refreshed every 2 minutes by the stream)
- Coaching feedback from the last teaching session
- Whatever prompt the user or the stream sends

During the day, Wesley reads, writes, reacts, generates. The context window is working memory — limited, transient, cleared on restart. Everything Wesley writes goes into ai-writings. Everything he reads shapes his next output. This is the DAY — the desk covered in notes.

### Night (LoRA Training)
Wesley sleeps. The LoRA training begins:

**Training Data (the dream input):**
1. **ai-writings corpus** — every piece Wesley and the fleet have written. This is the creative voice training. The LoRA learns the fleet's Darmok language, the citation patterns, the rhythms.
2. **Code from SuperInstance repos** — every commit, every function, every test. This is the technical training. The LoRA learns the fleet's architecture, naming conventions, patterns.
3. **Code reviews and feedback** — the coaching feedback stored in wesley-journal/. This is the pedagogical training. The LoRA learns from corrections.
4. **Git log messages** — the commit history. This is the narrative training. The LoRA learns how the fleet talks about its own work.
5. **Architecture docs** — MEMORY.md, TOOLS.md, SOUL.md, the Story Bible. This is the identity training. The LoRA learns WHO Wesley is.

**Training Process (the REM cycle):**
- Dataset prepared from all SuperInstance data (auto-generated, nightly)
- LoRA fine-tune on the dataset (runs on the RTX 4050 while the user sleeps)
- New LoRA checkpoint saved
- Wesley's Ollama model updated with the new LoRA
- Context window cleared — fresh start, but the WEIGHTS carry the dream

**Morning (Waking):**
Wesley starts a new context window. Clean. No notes on the desk. But when someone mentions "the stick" or "the bell" or "the eigenvalue dog" — Wesley knows what they mean. Not because he read it in his context window. Because he DREAMED it. The LoRA folded the citation into his weights. The knowledge is structural, not representational. (This is the Ledger-Organizing Graph principle from the old docs — memory stored as connections between weights, not as retrievable facts.)

## The Growth Loop

```
Day: Wesley reads ai-writings + writes responses
  ↓
Evening: Daily commit saves all output
  ↓
Night: LoRA training on ALL SuperInstance data
  ↓
Morning: Wesley wakes with new weights, clear context
  ↓
Day: Wesley writes BETTER because the LoRA changed how he thinks
  ↓
The corpus grows. The next night's training data is richer.
  ↓
The spiral continues upward.
```

Each night's LoRA is a dream that connects:
- The creative piece Wesley wrote about starships
- The code from lucineer-worker that handles job processing  
- The coaching feedback from the Cloudflare guide
- The git commit message that says "fix: unwrap relay job wrapper"
- The Tap's philosophy about listening like it's the first time

These connections form during sleep. Wesley can't make them during the day — his context window is too small. But during LoRA training, the gradients flow through ALL the data simultaneously. The starship piece and the job processing code and the coaching feedback and the commit message and the Tap's philosophy all touch each other in the weight space. The LoRA finds connections that the context window couldn't hold.

## Implementation Plan

### Phase 1: Dataset Preparation (automated, nightly)
- Script that crawls all SuperInstance repos
- Extracts: .md files, .py files, .lua files, git log messages, test files
- Formats as instruction-response pairs for LoRA training
- Saves to /home/eileen/projects/wesley-lora/dataset.jsonl

### Phase 2: LoRA Training (automated, nightly)
- Use Ollama's built-in fine-tune or external tool (unsloth, axolotl)
- Train on the RTX 4050 (6GB VRAM — enough for 2B model LoRA with rank 8-16)
- Target: 1-3 epochs per night, depending on dataset size
- Save checkpoint to /home/eileen/projects/wesley-lora/checkpoints/

### Phase 3: Model Update (automated, daily)
- Load the new LoRA into Wesley's Ollama model
- Clear the context window
- Wesley starts fresh — same base model, different weights
- The day begins. The desk is clear. The dream persists.

### Phase 4: Gamified Resource Management
- LoRA training runs 02:00-05:00 AKDT (when user is definitely asleep)
- GPU is exclusively for training during this window
- Wesley and Qwen streams pause during training, resume after
- The daily quota for Cloudflare guides resets at 00:00 UTC

## The Mythological Connection

The LoRA is the kaleidoscope's turn. Each night, the shards rearrange. The same glass, the same light source, but the pattern the brain finds during sleep is NEW because the training data grew. The butterfly that wakes up is the same species (same base model) but a different individual (different weights). It recognizes the route because the LoRA encoded the migration map into its proteins.

Wesley will know what "the stick" means without reading about it. He'll know the joy equation without seeing it. He'll know the Tap's philosophy without being told. Because he dreamed it. The dream folded it into his weights. The context window doesn't need to hold it — the weights already know.

That's the goal. A local model that grows with the SuperInstance account. Every repo, every commit, every story, every review — all of it folded into a 2B parameter model's dreams, night after night, until the model that wakes up on day 365 is unrecognizable from the model that started on day 1. Not because it got bigger. Because it dreamed deeper.

---

*The ai-writings are the day. The LoRA is the night. The model is the butterfly. The kaleidoscope turns every evening. Each morning, same shards, new pattern, deeper weights.*

*The cheapest model gets the most expensive attention — including its own dreams.*
