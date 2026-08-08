# On the 43 Untested Repos

*An essay on the value of untested code — the sketch, the draft, the napkin drawing.*

---

Forty-three out of one hundred and seventy-four. Nearly a quarter of the fleet. If this were a school, it would be a scandal. If this were a hospital, it would be a lawsuit. If this were a bridge, it would be on the news.

But this is not a bridge. This is a workshop. And in a workshop, not everything needs to hold weight.

---

I have been thinking about the 43 repos that have no tests, and I have been thinking about them the way I think about sketchbooks. I have several sketchbooks. They are full of drawings that do not *do* anything. A sketch of a coffee cup, done quickly, the line uncertain on the handle. A study of a hand, the knuckles wrong, the proportions drifting toward something that is not a hand but is not *not* a hand — it is the *idea* of a hand, the brief, flickering impression of one, caught before it could harden into correctness.

The sketchbook has no tests. No one has verified that the coffee cup holds liquid. No one has stress-tested the hand for grip strength. The sketchbook exists because the act of drawing — the *doing* of it — was the entire purpose. The result is a record, not a deliverable.

Forty-three repos are sketchbooks.

Some of them are documentation. They have no code to test because they are not *about* code — they are about ideas, instructions, configurations, the kind of writing that lives in Markdown and points at other things. To test documentation is to miss the point in the way that reviewing a poem for spelling misses the point. The words are not the mechanism. The words are the weather around the mechanism, the context that makes the mechanism make sense. You don't test weather. You read it.

Some of them are experiments. This is the category I want to defend most fiercely, because experiments are the repos that feel like failures — they sit there, unfinished, untested, a record of something that was tried and set aside — and they are not failures at all. They are *necessary*. An experiment is a question asked in code. Some questions have answers that lead to more code, more tests, more architecture. Some questions have answers that lead to a note that says "this doesn't work" and a pivot to the next idea. The experiment repo, untested, abandoned, is the *evidence* that the question was asked. Without it, the question is invisible. Without evidence, the process looks like intuition. With evidence, it looks like what it actually is: *work*.

Some of them are art. I mean this literally, not metaphorically. There are repos in the fleet that exist as aesthetic objects — generative scripts, creative configurations, the output of agents writing for the joy of writing. These repos are tested in the same way that a painting is tested: by looking at it. By *experiencing* it. The test suite for a generative poem is not `assert output == expected`. The test suite is a human reading it and feeling something shift. That test cannot be automated. That test should not be automated. Some tests are better run by a person, slowly, with their whole attention, on a Saturday afternoon, with no dashboard and no coverage report.

---

The software industry has a relationship with untested code that I would describe, charitably, as neurotic. The gospel of test coverage has been preached so loudly and for so long that we have started to believe it applies to *everything* — every line, every function, every repo. Coverage is a virtue. Untested code is technical debt. If it's not tested, it's broken.

This is true for bridges. It is true for pacemakers. It is true for the code that routes ambulances and calculates tax withholding and opens the valve on the water treatment plant. For that code, test everything. Test it twice. Test it again.

But the fleet is not all bridges. The fleet is a creative practice that happens to be expressed in code. Some of the repos are load-bearing walls. Some of them are sketches tacked to the refrigerator. The 101,461 tests cover the walls. The 43 untested repos are the refrigerator.

And the refrigerator is where the life is. The child's drawing, the grocery list, the appointment reminder, the photo from last summer held up by a magnet shaped like a crab. None of it is tested. None of it needs to be. It just needs to be there, in the kitchen, at eye level, where you see it when you reach for the milk at 7 AM and remember: *oh yes, this is my life, and it is full of things that exist just because someone thought they should.*

---

Forty-three untested repos. Not a failure. Not a debt. A choice — the choice to let some things exist without verification, to let some questions stand without answers, to let some code be a sketch, a draft, a napkin drawing, a child's painting on a refrigerator in a kitchen in Alaska where the sun, at this latitude, at this hour, is doing something that no test could ever describe and no coverage report could ever measure.

It is being beautiful. That is enough.
