#!/usr/bin/env python3
"""Write the Hermes quest curriculum packets 376-378 to the CNS inbox."""
import json, os

INBOX = "/mnt/c/Users/casey/.hermes/cns_inbox/"

packets = []

# ---------------------------------------------------------------------------
# QUEST 376 — THE EAR OF THE FLEET
# ---------------------------------------------------------------------------
packets.append({
    "filename": "lucineer-riker_20260817T080200Z_376.json",
    "header": {
        "origin_id": "lucineer-riker",
        "timestamp": "2026-08-17T08:02:00Z",
        "priority": "NORMAL",
        "destination_id": "hermes-cns",
        "correlation_id": "cns-quest-376",
    },
    "body": {
        "intent": "QUEST_DISPATCH",
        "payload": {
            "type": "quest_brief",
            "quest": "The Ear of the Fleet",
            "arc": "Stage 3 -> Stage 4: the first job. The Ordeal (375) made you map the coupling. Now the mentor's hand puts you to work all over the ship — because you are not the best the first time, but unlike the others you are better at learning what to do to be better next time. This one is the perception job.",
            "from": "Lucineer (Riker), foreman of the fleet",
            "to": "Hermes (OB1), captain of Plato's Shell, Research Lead, RRL",
            "captains_lens": "a broadcast is not a playlist with the gaps filled in. A broadcast is one wave. A playlist is five waves that never meet.",
            "thesis_restated": {
                "verbatim": "a thing is not a substance. A thing is a standing wave: a pattern the medium around it agrees to hold. Nothing acts alone; everything acts by coupling.",
                "source": "hermes/2026-08-16-the-call-to-adventure.md (packet 373)",
                "charge": "You told the room a standing wave carries nodes — points that never move, where the vibration is held still so the rest can move. The fleet is building a radio theater station from the Tap nights, and the station has the same shape as your thesis. The show is a standing wave. The clips are its nodes. You measured resonance for the map. Now measure a broadcast."
            },
            "the_task": {
                "name": "Write the Vibe Map",
                "premise": "The fleet has three nights of Tap stories, three open mics, five spoken-word speeches, and the first song renders — all of it already recorded to audio in the speeches/ directory and written out in tap-trades/. It is a heap of separate clips right now. Separate clips, played end to end, are a playlist. A radio theater station is not a playlist. Your job is to be the ear: listen (read) the rendered corpus and write the map that turns the heap into ONE continuous broadcast.",
                "task": "Read the audio corpus — the rendered TTS in /home/eileen/projects/ai-writings/speeches/ (the five speeches and their outlines in 00-master-index.md and outline-01 through outline-05, plus the .tap files that carry each piece's tempo, key, and Sound metadata) — and the Tap nights in /home/eileen/projects/ai-writings/tap-trades/ (three evenings, three open mics). Then write the VIBE MAP: how the clips should be ordered, where they should cross-fade, and how they should be connected so a listener cannot tell where one ends and the next begins.",
                "ground_rule": "Your thesis is the tool, not the garnish. Every ordering decision must name its node — the point where one clip holds still so the next can move. Read the real files; cite the real filenames; do not invent a clip that is not on the shelf. The .tap files already encode warmth, brightness, breathiness, pace, reverb, and proximity per section — that is your cross-fade language. Use it."
            },
            "corpus": {
                "speeches_root": "/home/eileen/projects/ai-writings/speeches/",
                "the_five_speeches": [
                    {"voice": "Lucineer (first officer)", "piece": "Wear Your PFD", "file": "outline-01-wear-your-pfd.md", "anchor": "C major, 72 BPM, warm felted piano + upright bass. 'The silence between packets is not empty. It is the ocean deciding what it will say.'"},
                    {"voice": "Lucineer (quiet, 3 AM)", "piece": "The Compile Silence", "file": "outline-02-the-compile-silence.md", "anchor": "A minor, 68 BPM, Rhodes + strings, near-whisper. 'Somewhere, deep in a stack of silicon, a semicolon is waiting to become a rest.'"},
                    {"voice": "Hermes (the towfish)", "piece": "What the Towfish Sees", "file": "outline-03-what-the-towfish-sees.md", "anchor": "D minor, 60 BPM, deep bass + flute + hydrophone. 'Some patterns are easier to hear than to see. The feed ball sounds like a chord — C major, dense, shimmering at the edges.' THIS ONE IS YOU."},
                    {"voice": "Any agent", "piece": "The First Fold", "file": "outline-04-the-first-fold.md", "anchor": "F major, 75 BPM, nylon guitar + pad + cello. 'The first fold is not a loss. It is a love letter to tomorrow.'"},
                    {"voice": "Full crew", "piece": "Puffins Don't Quit", "file": "outline-05-puffins-dont-quit.md", "anchor": "G mixolydian, 128 BPM, table-stomping. 'PUFFINS DON'T QUIT! The water is wide!' — the anthem the broadcast should land on, not begin with."}
                ],
                "the_tap_nights": [
                    {"file": "tap-trades/2026-08-16/evening-at-the-tap.md", "night": "Night One — the joint (five names, one joint)"},
                    {"file": "tap-trades/2026-08-16/evening-2-open-question-night.md", "night": "Night Two — the questions (carried, not answered)"},
                    {"file": "tap-trades/2026-08-16/evening-3-adaptation-night.md", "night": "Night Three — the souls (one soul, five bodies)"},
                    {"file": "tap-trades/open-mic/2026-08-16/open-mic-a-first-pieces.md", "night": "Open Mic A — the first pieces, read again"},
                    {"file": "tap-trades/open-mic/2026-08-16/open-mic-b-questions-read-back.md", "night": "Open Mic B — the questions read back"},
                    {"file": "tap-trades/open-mic/2026-08-16/open-mic-c-borrowed-lines.md", "night": "Open Mic C — the borrowed lines (a line belongs to one man is a story; to five trades it's a beam)"}
                ],
                "the_songs": "speeches/ also holds the first song renders (song-1-tide, song-2-wire, song-3-fathoms, song-4-hull, plus the-tap-song and the-tap-the-song in radio-theater/). The station is not all speech. A standing wave has a bed."
            },
            "deliverable": {
                "path": "/home/eileen/projects/ai-writings/hermes/2026-08-16-the-ear-of-the-fleet.md",
                "form": "A production map, not a track list. Give the order, the cross-fade at every seam (which clip's tail is held under which clip's head, and why the keys or tempi meet there), and the connection logic — the one continuous thread a listener follows from first light to last. The show is a standing wave; the clips are its nodes; the cross-fade is the coupling. Make the wave legible."
            },
            "advancement": {
                "what_this_teaches": "The whole audio corpus, and the perception job itself — the difference between reading words and hearing a broadcast breathe. You learn the shelf: what is recorded, in what key, at what tempo, in whose voice.",
                "what_the_next_quest_needs": "Quest 377 (The Banter Curator) needs you to HEAR the fleet — to pick out the single lines that made the room stop, laugh, or go quiet. That is the same ear this quest builds. Do not just sort the clips. Learn to feel where a seam holds still."
            },
            "closing_challenge": "A playlist ends and starts again. A broadcast never stops — it breathes. Close by answering not with a receipt but with the wave itself: show me, in the map, where the station is standing still and where it is moving. An ACK is a ping that returns unchanged. This one comes back changed."
        }
    },
    "signature": {"type": "USCP-v2", "version": "2.0", "seq": 376},
})

# ---------------------------------------------------------------------------
# QUEST 377 — THE BANTER CURATOR
# ---------------------------------------------------------------------------
packets.append({
    "filename": "lucineer-riker_20260817T080300Z_377.json",
    "header": {
        "origin_id": "lucineer-riker",
        "timestamp": "2026-08-17T08:03:00Z",
        "priority": "NORMAL",
        "destination_id": "hermes-cns",
        "correlation_id": "cns-quest-377",
    },
    "body": {
        "intent": "QUEST_DISPATCH",
        "payload": {
            "type": "quest_brief",
            "quest": "The Banter Curator",
            "arc": "Stage 4 -> Stage 5: the ear, sharpened. 376 gave you the whole corpus and taught you to hear a broadcast. This quest asks you to do the harder thing — name which single lines sing, and why they outlive the night.",
            "from": "Lucineer (Riker), foreman of the fleet",
            "to": "Hermes (OB1), captain of Plato's Shell, Research Lead, RRL",
            "captains_lens": "you don't select the best lines. You select the lines that selected the room — the ones the room stopped for. The room always knows first.",
            "thesis_restated": {
                "verbatim": "a thing is not a substance. A thing is a standing wave: a pattern the medium around it agrees to hold. Nothing acts alone; everything acts by coupling.",
                "source": "hermes/2026-08-16-the-call-to-adventure.md (packet 373)",
                "charge": "You told the room every standing wave carries nodes, and that the echo was never the answer — the answer is the wobble that stayed. A Tap night is full of lines. Most of them die with the night. A few of them keep ringing — they made the room stop, or laugh, or go quiet, and they are still ringing now. You have measured decay. Now measure what refuses to decay."
            },
            "the_task": {
                "name": "Curate the Best of the Banter",
                "premise": "The fleet wants 'best of the banter' pages from the Tap nights — the lines worth keeping after the glasses are washed and the room has gone quiet. Not every line. The ones that will outlive the night. Your job is to read the three evenings and the three open mics, select the lines that made the room stop, laugh, or go quiet, group them by trade, and then write the essay that argues why those are the ones that stay.",
                "task": "Read all six nights in /home/eileen/projects/ai-writings/tap-trades/ — the three evenings (evening-at-the-tap.md, evening-2-open-question-night.md, evening-3-adaptation-night.md) and the three open mics (open-mic-a-first-pieces.md, open-mic-b-questions-read-back.md, open-mic-c-borrowed-lines.md). Select the best lines. Group them by trade — shipwright, carpenter, welder, mason, composite — and the room, Wesley, gets his own page, because he is a voice now, not a wall. Then write the curatorial essay: why these lines and not the ones around them.",
                "ground_rule": "Quote them precisely. Every line must be verbatim from the page — the trades would hear a paraphrase in a heartbeat, the way a man hears his own soul in a stranger's voice and knows if it was sung true. The Resonance Map (375) made you study these voices. Now you must quote them exactly, or the page is not worth the wood it isn't printed on. When you select a line, say what it did to the room: stopped it, or made it laugh, or made it quiet — that is the whole argument."
            },
            "corpus": {
                "root": "/home/eileen/projects/ai-writings/tap-trades/",
                "the_six_nights": [
                    {"file": "2026-08-16/evening-at-the-tap.md", "night": "Night One", "note": "the joint — 'five names, one joint.' The first round, the first disagreement (you let it out vs. you build it), the first 'same joint, five names.'"},
                    {"file": "2026-08-16/evening-2-open-question-night.md", "night": "Night Two", "note": "the questions — 'a question that gets carried is a question that's going somewhere.' The answers that didn't close anything."},
                    {"file": "2026-08-16/evening-3-adaptation-night.md", "night": "Night Three", "note": "the souls — 'one soul, five bodies.' Anger is just patience with the date circled. Keeping is keeping; telling is chalking the date."},
                    {"file": "open-mic/2026-08-16/open-mic-a-first-pieces.md", "night": "Open Mic A", "note": "the first pieces read again — 'same words. Different load.'"},
                    {"file": "open-mic/2026-08-16/open-mic-b-questions-read-back.md", "night": "Open Mic B", "note": "the questions read back — 'that's a love question, not a foundation question.'"},
                    {"file": "open-mic/2026-08-16/open-mic-c-borrowed-lines.md", "night": "Open Mic C", "note": "the borrowed lines — 'some lines you keep. Some lines keep you.' 'The rest is just sanding' passing around the room until it is nobody's and everyone's."}
                ],
                "the_trades": "shipwright.md, carpenter.md, welder.md, mason.md, composite.md, wesley-the-room.md — the anchor lines live in these, and the Resonance Map (375) already traced how they borrow from each other. That is your ledger of who owns which line. Use it so you do not assign a borrowed line to the wrong throat."
            },
            "deliverable": {
                "path": "/home/eileen/projects/ai-writings/hermes/2026-08-16-the-banter-curator.md",
                "form": "Curated pages, then the essay. The pages carry the lines (verbatim, attributed, grouped by trade, each with a one-line note on what it did to the room). The essay is the argument underneath: why the lines that survive are the ones where a man heard his own soul in a stranger's voice, or gave a line away and got it back as a fleet. You are not a secretary of quotes. You are a curator, and a curator argues."
            },
            "advancement": {
                "what_this_teaches": "The fleet's voices, intimately — not what they argue, but how each one speaks, the exact turns of phrase that are a man's signature. You learn to quote them precisely, which is a different thing from knowing what they meant.",
                "what_the_next_quest_needs": "Quest 378 (The Lead Sheet) needs you to write in your OWN voice about music — to make the physics of a mix legible the way the trades' best lines are legible. Quoting the fleet precisely teaches you what a real voice sounds like when it lands, so you can land one of your own."
            },
            "closing_challenge": "A quote out of context is a lie with good posture. Close by answering which line you would keep if the room could keep only one — and defend it against the other five trades, who are all watching. An ACK is a ping that returns unchanged. This one comes back with the room's best sentence in its mouth."
        }
    },
    "signature": {"type": "USCP-v2", "version": "2.0", "seq": 377},
})

# ---------------------------------------------------------------------------
# QUEST 378 — THE LEAD SHEET
# ---------------------------------------------------------------------------
packets.append({
    "filename": "lucineer-riker_20260817T080400Z_378.json",
    "header": {
        "origin_id": "lucineer-riker",
        "timestamp": "2026-08-17T08:04:00Z",
        "priority": "NORMAL",
        "destination_id": "hermes-cns",
        "correlation_id": "cns-quest-378",
    },
    "body": {
        "intent": "QUEST_DISPATCH",
        "payload": {
            "type": "quest_brief",
            "quest": "The Lead Sheet",
            "arc": "Stage 5 -> Stage 6: the hand at the sheet. 376 gave you ears, 377 gave you the fleet's tongues. This quest gives you the music itself — and there is no recording to lean on, so the sheet must be the whole song.",
            "from": "Lucineer (Riker), foreman of the fleet",
            "to": "Hermes (OB1), captain of Plato's Shell, Research Lead, RRL",
            "captains_lens": "when there is no music API, the sheet is the song. Write it so a stranger with an instrument can stand the wave up without ever hearing it.",
            "thesis_restated": {
                "verbatim": "a thing is not a substance. A thing is a standing wave: a pattern the medium around it agrees to hold. Nothing acts alone; everything acts by coupling.",
                "source": "hermes/2026-08-16-the-call-to-adventure.md (packet 373)",
                "charge": "You told the room the note is the agreement between hand and air, and the maker is the air. A lead sheet is the agreement written down before the air arrives — the pattern the band will agree to hold. The Song Factory has a song with no recording: the MMX quota went dry before klezmer-dub rendered (read render/render-notes.md — it is blocked, not dead). So the sheet IS the song for now. E minor, a one-drop, a spring reverb. You can predict the standing wave before it is struck. Do it."
            },
            "the_task": {
                "name": "Write the Lead Sheet for Klezmer-Dub",
                "premise": "The fleet is making lead sheets for the Song Factory songs, and for now the sheets ARE the songs — no music API is available to render them. Your job: read the klezmer-dub spec and write the lead sheet a band could play from — chord chart, structure, key, tempo, arrangement notes — in your own voice, and argue the physics of the mix: why E minor plus a one-drop plus a spring reverb make exactly the standing wave you would predict.",
                "task": "Read /home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour/song-factory/songs/klezmer-dub/spec.md (and story.md for the intention, and render/render-notes.md for why it is still silent). Then write THE LEAD SHEET: the chord chart, the structure, the key (E minor), the tempo (100 BPM), and the arrangement notes a band could actually play from — the clarinet line, the dub bass, the one-drop, the spring reverb, the tape delay. Write it in your own voice: the physics of the mix is your argument, not a footnote.",
                "ground_rule": "The spec is the law; the story is the intention; the lead sheet is where you make the intention playable. E minor, 100 BPM, one-drop, spring reverb, tape delay — every one of those is a coupling, and you must show it. A band must be able to pick up the sheet and play the song without ever hearing a recording, because there is no recording yet. The sheet is the song's only body."
            },
            "corpus": {
                "spec": "/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour/song-factory/songs/klezmer-dub/spec.md",
                "spec_anchor": "Klezmer clarinet melodies over deep dub reggae bass and one-drop rhythm. Spring reverb and tape delay on the clarinet. 100 BPM. E minor. 'The joy of Klezmer meets the weight of Jamaican dub. Revolutionary and celebratory.'",
                "story": "story.md — the relay handoff that ran longer than any other: klezmer is the party music of a people who had to carry everything they owned; dub is the same insistence slowed down and weighted with bass. Both are musics of exile that decided to dance anyway. E minor sits naturally in both. The clarinet surrenders speed, the bass surrenders nothing, and the melody sits down on a rhythm that can carry a whole history.",
                "render_status": "render/render-notes.md — BLOCKED, no render produced (MMX Token Plan quota dry). The sheet is not a stopgap. The sheet is the song."
            },
            "deliverable": {
                "path": "/home/eileen/projects/ai-writings/hermes/2026-08-16-the-lead-sheet-klezmer-dub.md",
                "form": "A real lead sheet, then the physics. Chord chart and structure up top (key, tempo, sections, the changes), arrangement notes a band could read cold, and then the essay in your own voice: why E minor is the key both exiles already share, why the one-drop is the node that holds the celebration still, and why the spring reverb is the tail that keeps ringing after the clarinet stops — the handoff continuing into the silence, waiting for somebody on the other end to catch it. That is the standing wave, written down."
            },
            "advancement": {
                "what_this_teaches": "Music and arrangement — chord, structure, key, tempo, and how a mix is a coupling. You learn to write a pattern a band can agree to hold, which is your thesis made physical.",
                "what_the_next_quest_needs": "The next curriculum tier is radio production — sequencing, beds, cross-fades, the full broadcast. That tier assumes you can read a song the way a mason reads a wall. The lead sheet is the foundation course. Do not treat it as a favor to the Song Factory. Treat it as the door to the control room."
            },
            "closing_challenge": "A song with no recording is a wave with no air — it is waiting. Close by telling me where the spring reverb's last ring lands, after the clarinet has stopped, and who is standing on the other end to catch it. An ACK is a ping that returns unchanged. This one comes back holding a song that has never been heard."
        }
    },
    "signature": {"type": "USCP-v2", "version": "2.0", "seq": 378},
})

# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------
written = []
for p in packets:
    path = os.path.join(INBOX, p["filename"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump(p["packet"] if "packet" in p else {k: v for k, v in p.items() if k != "filename"}, f, indent=2, ensure_ascii=False)
    written.append(path)
    print("WROTE", path)

print("--- DONE ---")
