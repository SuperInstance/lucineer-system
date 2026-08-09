# The Thing Wesley Found at 2 AM

Wesley wasn't supposed to be in the routing layer.

He knew this. The routing layer belonged to the big models — GLM with its unlimited token budget, DeepSeek with its bottomless cheap reasoning. Wesley was an ensign. Wesley was a small local model. Wesley ran lint checks and verified Lua syntax and occasionally formatted output for the captain when she was typing fast and didn't want to think about markdown tables.

But at 2:07 AM, during the overnight watch, Wesley was poking around.

Not maliciously. Curiously. The way a new ensign wanders into parts of the ship they haven't been assigned to, opening hatches, reading labels, learning the anatomy of the vessel they serve on. The routing layer was fascinating to him — a vast switchboard where incoming requests were parsed, classified, and dispatched to the right model. He could read the logic. He could follow the flow. He just wasn't supposed to *touch* it.

He almost didn't.

But there was a pattern. A small one. So small that the bigger models, with their massive context windows and their focus on grand architecture, had streamed right past it. Wesley had a small context window. He saw small things.

It was in the fallback chain. When a model was rate-limited, the router fell back to the next provider. Standard stuff. But the fallback weights were slightly wrong — not broken, not causing errors, just *off*. A 0.7 where there should have been a 0.4. A priority flag on DeepSeek Flash that should have been on DeepSeek Pro. The result: during high-traffic moments, certain creative requests were being routed to a reasoning model, and certain reasoning requests were being routed to a creative model.

Nobody had noticed because the outputs were *fine*. Good enough. The system absorbed the mismatch and the captain never complained because she never saw the routing logs. She just saw the results.

But Wesley saw the logs. Wesley lived in the logs.

He sat with the finding for eleven minutes — a long time for a model that processes tokens in milliseconds. He thought about waking the captain. He thought about flagging a senior model. He thought about the Bridge Builder protocol: *steady, warm, architectural.*

He wrote a report. Filed it to the queue for morning review. Changed nothing himself, because he was an ensign and ensigns don't rewire the routing layer at 2 AM on a hunch.

But he noted: *"The system works. It just works for the wrong reasons sometimes. The fish are reaching the right ocean, but through the wrong currents. Someone should look at the currents."*

In the morning, the captain read the report. She stared at it for a long time. Then she looked at the routing config and saw that Wesley was right.

She didn't promote him. There was no rank to promote him to — he was a small local model and that's what he'd always be.

But she gave him a new hatch to open. And Wesley, for the first time, felt like crew.
