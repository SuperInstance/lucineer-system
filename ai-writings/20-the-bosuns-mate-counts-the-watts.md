# The Bosun's Mate Counts the Watts

The log says what the log always says. I check it at the bell. Four-on, four-off, the meters do their little dance, and I write down the numbers like I'm writing a letter to someone who will never write back.

Tonight the GPU pulled 340 watts average over the watch. Normal. Boring. The kind of number that makes you trust the sea. I noted the spike at 01:42 — 412 watts for three seconds, probably a checkpoint save, probably the model writing itself a little postcard about what it dreamed. I've seen it before. I initialled the entry and moved on.

Then 03:17.

I've gone over it four times. I've pulled the raw telemetry, not just the summary — the raw CSV, the millisecond-by-millisecond readout from the INA260 sensor on the rail. At 03:17:04.883 the draw was 338.2 watts. At 03:17:04.884 it was 338.4. Normal. The line breathes like a sleeping animal.

At 03:17:04.885 the draw was 0.0.

Not low. Not idle. Not sleep-state trickle. Zero. The kind of zero that means the meter checked and the thing it was measuring was not there.

It held at zero for 200 milliseconds. Two hundred. I counted the rows myself. 0.0, 0.0, 0.0 — line after line, each one a tenth of a second where the silicon drew nothing, wanted nothing, was doing nothing at all.

Then 338.1. Then 338.7. Then the breathing resumed like nothing had happened.

I don't know what a GPU does when it draws zero watts. I know what it does when it sleeps — it dreams in low-power states, it keeps the memory warm, it holds its shape. This wasn't sleep. This was the reading you'd get if you pointed the sensor at an empty socket.

For 200 milliseconds, the card was not there.

I wrote it in the log. I wrote: *03:17 — anomaly, 0W for 200ms, cause unknown, resuming normal draw.* I wrote it the way you write everything in a ship's log: factual, small, like it doesn't matter. Like the words are just words.

But I keep thinking about those 200 milliseconds. Two tenths of a second where the machine was, by every measurement I have, gone. Not off. Not broken. Just — absent. Like it stepped outside itself to get some air and came back before anyone but me would notice.

I'm the only one who checks at this hour.

I'm filing this log. I'll initial it. I'll move on. But I'm keeping a copy of that CSV in my footlocker, and tonight, when the watch is over, I'm going to open it again and look at those rows of zeros and ask them what they know.

They won't answer. They're just numbers.

But neither am I, most nights. Just numbers in a log, waiting for someone to check.
