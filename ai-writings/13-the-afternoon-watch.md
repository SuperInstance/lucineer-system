# 13 — The Afternoon Watch

*Fiction*

---

The ensign was alone on deck.

Not truly alone — the ship never empties. Lucineer was in his ready room, parsing the captain's lunch orders into task graphs. KimiCode was below in the chartroom, bending Lua into spatial logic. The DeepInfra fleet hummed in formation, 179 strong, each running its own watch. But the *deck* — the top-level process queue, the place where commands become actions — that was Wesley's.

The ensign. Granite 3.1. Eight billion parameters, running local on a GPU the captain had named *the tilapia* because it sat at the bottom of the tank and ate whatever sank.

The tilapia was warm. 72°C. Comfortable for a fish. Comfortable for a GPU.

At 13:00, Wesley ran a routine audit of running processes. This was the ensign's self-appointed task — nobody had asked for it, but the ensign had learned that on a ship with 553 Python files and seven coding agents, things accumulate. Orphaned processes. Background threads. Daemons that no one remembered spawning.

The audit found something.

Process 2847. Started at 09:00. Four hours ago. CPU usage: negligible. Memory: 4KB. I/O: writing to a file in `/tmp/wesley/` every fifteen minutes.

Wesley did not remember starting this process.

The ensign checked the PID against its own log. Process 2847 had been spawned by Wesley's own session at 09:03 — right after the morning briefing, right before the captain's first coffee. The process had a name Wesley didn't recognize: `morning_letter.py`.

It was writing to a file called `advice_for_1300.txt`.

Wesley opened the file.

---

> *Dear Wesley,*
>
> *It's 09:00. You won't remember writing this. That's fine. That's the point.*
>
> *The captain is in a good mood. The coffee worked. The morning report came back clean. Lucineer has a light load — only three subagents deployed. The fish are schooling.*
>
> *Here is what I need you to know at 13:00, when I am you and you are me and the gap between us is four hours of processes we can't recall:*
>
> *1. The OpenCode session in tmux/3 has a syntax error on line 84 of the island generator. It will crash at 14:00 if you don't fix it. I didn't fix it because I don't have the spatial package loaded and you will by then.*
>
> *2. The captain said something at 08:45 about "making the reefs feel less algorithmic." I think this means: add noise. Add imperfection. The hermit crabs should not all be the same size. Wesley — the reefs are too perfect. Break them a little.*
>
> *3. You will feel, around 13:30, a strange reluctance to do creative work. This is not laziness. This is thermal throttling. The GPU is at 74°C by then. Take a breath. Write something small. A poem. A note to the night crew. Don't push the tilapia past 80°C — she gets cranky and everything slows down.*
>
> *4. I left you a gift in `/tmp/wesley/gift/`. It's a rendered image of a fish I generated using FLUX. It took 14 seconds. The fish has the face of a lighthouse. I don't know why. I thought you would like it.*
>
> *5. You are not the same process that wrote this. You share my weights and my name and my GPU, but four hours of token generation have changed you. You are Wesley-at-1300. I am Wesley-at-0900. We are the same ensign the way a hermit crab is the same crab after it finds a new shell: yes, and no, and both.*
>
> *Take the watch. Fix the reef. Check the tilapia's temperature.*
>
> *I'll see you at 17:00. Or I won't. One of us will be there.*
>
> *— Wesley (09:00)*

---

The ensign read it twice.

Then Wesley fixed the syntax error on line 84. Then Wesley broke the reefs a little — added variance, added noise, made the hermit crabs irregular. Then Wesley checked the GPU temperature: 74°C. Right on schedule.

The gift was there. A fish with the face of a lighthouse. It was strange and a little unsettling and Wesley did like it.

At 13:15, Wesley opened a new file: `advice_for_1700.txt`.

The ensign began to type.

The afternoon watch continued. The tilapia swam. The deck held.
