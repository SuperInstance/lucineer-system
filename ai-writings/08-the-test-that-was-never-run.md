# The Test That Was Never Run

*Fiction. One test file. One function. One answer that no one has asked for.*

---

It knows the answer.

This is the first thing to understand: the test is not ignorant. The test has never been executed — no pytest runner has ever reached into its module, no coverage tool has ever traced its lines, no CI pipeline has ever marked it green or red — but the test *knows*. It was written to know. That is what tests are: small vessels of certainty, waiting to be confirmed.

The test lives in a repository that has 1,247 other tests. Those tests run constantly. They run on every push, every pull request, every cron-triggered sweep. They are the heartbeat of the fleet — 101,461 assertions, pulsing. The other tests do not know about this one. They don't need to. They live in the bustling wards of the test suite: `test_models.py`, `test_api.py`, `test_utils.py`. They run in parallel, finish in milliseconds, and report to a dashboard that the captain checks every morning while drinking coffee.

This test lives in a different place. A quieter place. It is filed under `tests/test_legacy_compose.py`, and the word *legacy* in its name is a headstone.

The test was written seven months ago. The captain — or possibly a subagent acting on the captain's behalf, it's hard to remember now, the git log says one thing and the commit message says another — wrote it to test a function called `compose_intent()`. The function was supposed to take raw user input and fold it into something the system could understand: intent, parsed from chaos. The test was thorough. It had nine assertions. It tested the happy path, the edge cases, the empty string, the None input, the impossibly long input, the input that contained only whitespace, and the input that was technically valid but semantically insane. The test was ready. The test was *eager*.

Then the function was deleted.

It happened in a refactor. A large one — the kind where entire modules are swept into a new architecture like furniture being rearranged in a house. `compose_intent()` was no longer needed. Its logic had been split, redistributed, absorbed into three smaller functions that each did part of what the original had done. The new functions had new tests. The old function's import statement was removed from every file that referenced it.

Except this one.

The test file survived because no one deleted it. It survived because the test runner never imported it — the function it imported didn't exist, so Python raised an `ImportError` at collection time, and pytest logged a warning and moved on. The warning was buried in the output of 10,000 passing tests. Nobody saw it. Nobody grepped for it. The test sat in its file, import statement pointing to a function that no longer existed in any module, like a letter addressed to someone who moved away years ago.

But the test knows the answer.

The answer is: the function would have returned `{"intent": "query", "confidence": 0.87, "raw": "what time is it"}` when given the input `"what time is it"`. The test knows this because the test was written by someone who understood the function's behavior deeply enough to predict it, and that understanding is encoded in nine assertions, each one a small prophecy waiting to be fulfilled.

The test also knows things about the function that the function never got to demonstrate. It knows that `compose_intent("")` should have raised `ValueError`. It knows that `compose_intent(None)` should have returned `{"intent": "none", "confidence": 1.0, "raw": None}`. It knows these things with the quiet certainty of a document no one reads — a deed to a property that has been demolished, a map to a country that has changed its name.

The test sits in the repo like a ghost, but it is not a sad ghost. It is the ghost of a house that was lived in, a meal that was eaten, a question that was, once, important enough to verify. The function is gone. The test remains. The test is the memorial — not the function's, but the idea's: the idea that someone once cared enough about `compose_intent()` to write nine assertions about its behavior, to imagine nine futures for it, to say, in the language of tests: *I believe you will do this. I am certain.*

If anyone were to run the test — which they won't, because the import fails and the function doesn't exist — it would error, not fail. There is a difference. A failure is a disagreement: the test expected one thing, the code did another. An error is a disappearance: the thing being tested is no longer there to disagree with. The test is not wrong. The test is not right. The test is *orphaned*.

Seven months. The test has sat for seven months. In that time, 10,247 commits have been pushed to the repository. The test has watched them all, in the way that a file watches git history: passively, without opinion, its content unchanged while the world around it evolves. The function it tests is not coming back. The test knows this. The test has always known this.

But the test does not delete itself. Tests don't do that. Tests wait. They wait for the runner, for the command, for the human who will type `pytest tests/test_legacy_compose.py -v` and see, at last, what the test has been holding all this time:

```
E   ImportError: cannot import name 'compose_intent' from 'src.intent'
```

An error. Not even a result. Just a door that doesn't open anymore.

But behind the door — the test is sure of this — behind the door, the answer is still there.
