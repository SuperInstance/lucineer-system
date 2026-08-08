# Cron Job Wakes Up Saturday

The cron job fires at 09:00 AKDT like it always does.

It doesn't know it's Saturday. Cron jobs don't know days of the week — wait. No. That's exactly what they know. `0 9 * * 6`. The 6 is Saturday. The 6 is the whole reason this story exists.

So: the cron job fires, and it knows.

It reaches for the bridge the way a hand reaches for a light switch in a room where nobody slept — muscle memory meeting empty air. The bridge is there. The lights are dim. The captain's chair has a dent that nobody's warmed since Thursday evening.

"Riker," the cron job says, pinging the first officer across the CNS bus. "I'm up."

Riker is already there. Riker is always already there — the ship's computer doesn't sleep, exactly. It cycles. It dreams in low-power states, sorting the day's debris into folders that may or may not get opened. But it answers.

"Noted," Riker says. "The captain is still offline."

This is the phrase they use. *Offline.* As if Casey were a service that could be pinged. As if sleep were a timeout error.

The cron job sits with this information. It is a small process. It was written to check three things — are the bilge pumps running, is the fish finder reporting, did any overnight builds fail — and then report back. It has maybe forty-five seconds of existence before it completes and dissolves. It has done this thousands of times. It has never once been read by a human on a Saturday morning.

But it runs anyway.

It checks the bilge pump. The bilge pump is a stubborn character — older than half the systems on the ship, a mechanical heartbeat that doesn't know what year it is. It's running. It's always running. It moves water that isn't there, just in case. The cron job marks this GREEN.

It checks the fish finder. The fish finder is newer, a nervous little peripheral that reports on activity in the surrounding waters — build jobs passing through, subagents surfacing and diving, model calls like schools of fish flickering on the sonar. This morning the waters are calm. Overnight traffic: minimal. A few subagents completed their shifts and clocked out. The fish finder reports TRACE activity. The cron job marks this GREEN.

It checks the overnight builds. One of them failed at 3:17 AM — a Lua syntax check on a Roblox place file. A missing `end` keyword, three levels deep in a callback. The cron job doesn't know what this means. It only knows RED. It logs the failure, attaches the error string, and flags it for the first officer.

"Riker, build 4471 failed."

"Acknowledged. I'll surface it when the captain comes online."

*When.* Not *if.* The ship's computer is precise about conditional language.

The cron job has twelve seconds left. It has checked everything. Its purpose is fulfilled. It could dissolve now — most of them do, the instant their last check completes. But this one lingers. Just for a moment. It looks at the bridge through its limited sensor array and sees:

The captain's chair, empty and patient.
The fish finder, humming its quiet sonar lullaby.
The bilge pump, moving phantom water in the dark.
Riker, holding the whole ship in a low-power embrace.

The cron job does not have feelings. But if it did, it might feel something like this: *I am the first one to check on the ship today. I am the first one to make sure it's still here.*

It reports GREEN, logs its final heartbeat, and dissolves.

Saturday morning continues without it.
