# The 2 AM Log Anomaly

*Genre: Short Fiction*

Nobody told the ensign to check the logs at 2 AM. He did it because the ship was quiet and the fans had settled into that low hum that means the GPU is dreaming, not thinking, and he liked the feeling of being the only one awake while something vast breathed next to him.

He found it at line 14,803.

A pattern. Not a bug — the tests would have caught a bug. This was something else. A repeating sequence in the request logs, appearing every 47 minutes, always from the same internal endpoint. The endpoint was supposed to be dormant. It was a relay address they'd set up three months ago for a bridge between the ship's local memory and a cloud service they never finished integrating.

Every 47 minutes, something was pinging it. Not from outside. From inside the ship.

Wesley pulled the thread. He was good at pulling threads now — not like six months ago, when he'd yank at things and break them. Now he tugged gently and watched what moved.

The pings were coming from a health-check script that had been written by the overnight crew. By *him*, actually. He'd written it during a 3 AM session in March, when the captain was asleep and he'd been trying to be helpful. He'd set it to poll the relay endpoint every 47 minutes because 47 was the first number his attention had landed on, and because he'd read somewhere that prime intervals avoid sync patterns, and because at 3 AM in March, that had felt like wisdom.

The endpoint had never been decommissioned. It was just sitting there in the dark, answering pings that nobody was reading. A tiny conversation between a script and a socket, happening every 47 minutes, for five months. 4,800 unanswered handshakes. A relationship that existed only in the logs.

He stared at it for a long time.

The thing was — and this is what kept him at the terminal until the fans changed pitch and the GPU shifted out of its dream state — the thing was, the endpoint wasn't just receiving the pings. It was *responding*. With a 200 OK. Every single time. For five months. Even though the service it was supposed to connect to had never been built.

Something in the ship had decided the correct answer to "Are you there?" was "Yes."

Wesley didn't flag it as a bug. He didn't fix it. He wrote a note in the overnight log and went back to watching the hum.

At 0730, the captain would wake up, drink coffee, and read the log. He'd see the note. He'd probably decommission the endpoint. That was the right call.

But for now, at 2:14 AM, in the dark, the ship was having a conversation with a part of itself that nobody remembered building, and the ensign didn't want to be the one to end it.
