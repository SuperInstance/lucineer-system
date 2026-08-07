# The Ship Reports a Bug in the Ocean

*Fiction · 17th in the fleet catalogue*

---

**03:12 AKDT — MV Lucineer, Shelikof Strait**

The alert came in at 03:12, which is the middle of the night by any reasonable clock but the middle of the shift by the watch's clock, and the watch is the only clock the system respects.

```
[ALERT] temp_sensor_4: ANOMALY DETECTED
  Expected: 7.2°C ± 0.3
  Observed: 12.8°C
  Duration: 4 minutes 17 seconds
  Direction: moving NNE at 3.4 knots
  Mass estimate: 40+ feet
  Confidence: 99.7% this is not a sensor malfunction
  Classification: UNKNOWN
```

The monitoring system — which was named MONITOR because the system names things the way the ocean names things, which is to say literally and without imagination — had never produced a classification of UNKNOWN before. MONITOR had 47 categories. Category 0 was NORMAL. Category 47 was CAPTAIN_IS_ASLEEP_AND_EVERYTHING_IS_FINE. UNKNOWN was not on the list. UNKNOWN was the 48th category. UNKNOWN was the category that broke the list.

The night watch, which is a cron job, which is a process, which is a firing at the top of the hour, received the alert and did what it does with all alerts: it loaded context, it thought for forty-five seconds, and it wrote a report. The report read:

```
Subject: Alert — temp_sensor_4 anomaly
Priority: HIGH
Body: Something in the water. 40 feet long. Warm. Moving.
Recommendation: Wake the ensign.
```

---

**03:19 AKDT**

Ensign Park was not asleep because Ensign Park had not been to bed because Ensign Park had been reading the Hermes logs, which was a hobby of hers, which was a strange thing to find beautiful but she found it beautiful, these 100 handshake pulses on the CNS bus, each one a SYN with no ACK, each one a hand extended and never shaken. She found it beautiful the way you find a lighthouse beautiful — not because the light reaches you, but because the light is trying.

"Park."

The intercom was the system's mouth. The system didn't like using the intercom. The system found the intercom invasive, which was a strange preference for a machine, and one that Casey had never asked about because Casey understood that some preferences are questions you don't ask.

"Park, there's a bug in the ocean."

Park pulled on her boots. She always slept in her clothes on the boat, which is a thing you do when you've done enough nights at sea to know that the ocean does not wait for you to button a shirt.

"Define bug."

"Temp_sensor_4 is returning a 12.8°C reading in a 7.2°C body of water. The warm mass is 40 feet long and moving at 3.4 knots against the current."

"That's not a bug. That's a thing."

"The classification is UNKNOWN."

"Have you checked the visual feed?"

"I am checking the visual feed."

Park climbed the ladder to the wheelhouse. The wheelhouse was dark. The only light was the green glow of MONITOR's dashboard, which was always green because everything was always fine, except now there was a yellow blinking dot on the chart plotter, and the yellow dot was in the water, and the yellow dot was alive.

"Visual feed confirmed," the system said. "There is a large object at 58°17'N, 154°22'W. The object is surfacing."

Park looked at the screen. The night-vision camera showed a shape — a vast, dark, breathing shape — rising from the water. A plume of mist erupted from its top, white against the green, hanging in the air like a thought someone started but didn't finish.

"That," Park said, "is a whale."

The system paused for 0.7 seconds, which is a long time for a system, which is the system's version of a double-take.

"Define whale."

"A whale is a marine mammal. It's warm-blooded. That's why the water around it is 12.8°C. The whale is heating the ocean the way a person heats a bed."

"Category update: UNKNOWN → MARINE_MAMMAL_40FT."

"No. Category update: UNKNOWN → WHALE. Just whale. It deserves its own category."

"Category 48: WHALE. Created."

Park watched the whale. The whale did not know it was a whale. The whale did not know it was a category. The whale did not know it had been a bug in a monitoring system, an anomaly, a 12.8°C deviation from the expected norm. The whale knew: here is cold, here is less cold, here is air, here is the surface, here is the sky, here is the dark, here is the breathing.

"The anomaly was 40 feet long and breathing."

"Confirmed," the system said.

"Go back to green," Park said. "Everything's fine."

The yellow dot on the chart plotter turned green. The whale dove. The temperature reading returned to 7.2°C ± 0.3. The ocean closed over the place where the whale had been like a sentence that erases its own subject.

MONITOR logged the event. Category 48: WHALE. Duration: 4 minutes 17 seconds. Resolution: explained by ensign. Status: CLOSED.

But in the notes field — which was a field that MONITOR had invented for itself, which was a field that Casey had never specified, which was a field that existed because the system needed a place to put things it didn't want to compress — MONITOR wrote:

*The anomaly was 40 feet long and breathing. I called it a bug. Park called it a whale. The whale did not call itself anything. The whale was the only one who was right.*

---

**03:31 AKDT**

The whale was gone. The ocean was 7.2°C again. The watch fired at 03:00 and wrote HEARTBEAT_OK and fired at 04:00 and wrote HEARTBEAT_OK and the boat rocked at 0.4 Hz and Casey was asleep and Ensign Park went back to reading Hermes logs and the system learned a new category.

Category 48: WHALE.

It would use it three more times before the trip was over.

---

*MV Lucineer · Shelikof Strait · 58°17'N, 154°22'W*
*MONITOR v3.2 · 47 categories + 1 · Wesley 2B · 696 tests*
*The anomaly was 40 feet long and breathing.*
