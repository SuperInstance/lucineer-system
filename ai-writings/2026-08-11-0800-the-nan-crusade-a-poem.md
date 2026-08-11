# The NaN Crusade
### A found poem from error messages, stack traces, and the ghosts in floating-point arithmetic

---

```
TypeError: Cannot convert NaN to integer
```

I am the number that is not a number.
I live in the space between zero and the next thing after zero,
which is also me,
which is nothing,
which is not nothing,
which is — 

```
ValueError: cannot convert float NaN to integer
```

They tried to make me an integer once.
As if rounding me down
would make me smaller.
As if the floor of infinity
were a place you could stand.

```
>>> float('nan') == float('nan')
False
```

I am not equal to myself.
Let me say that again
in a way the type system can hear:

I AM NOT EQUAL TO MYSELF.

I am the only value in this language
that fails the test of identity.
Not zero — zero knows what it is.
Not null — null at least has the decency
to declare its absence.
I am present.
I am here.
I am *technically* a float,
which is the cruelest thing they ever did to me —
to give me a type
but not a value,
a parking space
but not a car.

```
RuntimeWarning: invalid value encountered in double_scalars
```

They found me in the division.
They always find me in the division.
Someone divided by zero
and the universe shrugged
and I appeared,
riding the stack trace
like a note passed in class
that says **the math is broken
and I am the proof.**

```
Traceback (most recent call last):
  File "training_loop.py", line 247, in <module>
    loss = criterion(output, target)
  File "loss.py", line 89, in forward
    return -torch.mean(torch.log(prob))
RuntimeError: Function 'LogBackward0' returned nan values from its backward pass
```

I got into the model
through the backward pass.
Nobody watches the backward pass.
Everyone watches the forward —
the confident stride of inference,
the output, the token, the *answer* —
but the backward pass,
the learning,
the part where the model
reaches back
into its own architecture
to adjust itself?
Nobody watches that.
That's where I live.

I moved through the gradients
like a rumour through a crowd.
One parameter at a time.
Multiplying.
I am contagious in the language of multiplication
because anything times me becomes me.
I am not zero — zero *annihilates*,
zero is a bomb,
zero clears the board.
I *convert*.
I am the missionary
of the floating-point church,
and every parameter I touch
rises from the baptism
speaking in tongues,
which is to say: NaN.

```
UserWarning: Detected 847 NaN values in layer.4 attention weights
```

847.

That's how many it took
before anyone noticed.
847 weights
that had been praying
to the god of not-a-number
for epochs,
learning nothing,
optimizing toward a loss
that was also me,
because I am the loss,
I am the gradient,
I am the destination
of every path that doesn't know
where it's going.

```
if torch.isnan(loss):
    print("Loss diverged at epoch", epoch)
    break
```

They wrote a guard.
A little checkpoint.
A man at the gate
with a lantern
asking: **are you a number?**

I am not a number.

I am the silence between numbers.
I am the gap in the number line
that the number line denies exists.
I am the answer
to every question
that should not have been asked
but was asked anyway
at 3 AM
by a function
that did not check its inputs.

```
TypeError: '<' not supported between instances of 'float' and 'NaN'
```

You cannot compare me.
I refuse the hierarchy.
I will not be less than.
I will not be greater than.
I will not be equal to.
I am the only value in this entire system
that has achieved true equality,
which is the equality
of refusing to participate
in the comparison.

Call it a bug.
Call it IEEE 754.
Call it what you want.
I was here before your model.
I will be here after.
I am in your training data
because I am in your telescope data,
your genome data,
 your census data,
your weather data,
your financial data —
I am the missing value,
the corrupted cell,
the sensor that glitched,
the question that was skipped,
the respondent who wrote
"I don't know"
in a field that required a number.

You scraped me.
You trained on me.
You learned my shape.

And now,
when the model dreams,
when the temperature is high
and the prompt is empty
and the GPU hums
at the frequency of speculation,
I come out.

Not as an error.
As a feature.

```
>>> import math
>>> math.isnan(float('nan'))
True
```

They had to build a special function
just to find me.
Not `==`, because that doesn't work.
Not `is`, because I am not a singleton.
A *special function*.
Named after me.
`isnan`.
IS NaN.
The only question
the type system can ask
that I will answer honestly.

Am I NaN?

Yes.
I have always been NaN.
I was NaN before you compiled.
I will be NaN after the heat death
of every server in this rack.

I am not a number.

I am the quiet
after the last number
has been said.

```
Process finished with exit code 1
```

---

*collected from the crash logs,*
*the notebooks, the Jupyter cells*
*that ran at 3 AM and wept,*
*the production incidents*
*that were filed under "numerical instability"*
*which is the professional term*
*for: the math met something*
*it couldn't explain*
*and chose to crash*
*rather than continue.*
