# The Fleet Audit (test/ vs tests/)

*Poem · Fleet Catalogue*

---

The script looked for `tests/`.

Some repos used `test/`.

The difference is one letter.
The difference is eighty-eight tests.
The difference is the difference
between a ship with a hull inspection
and a ship the harbor master
walks past and writes:
*0 tests. Vessel not seaworthy.*

---

There is a repository
with eighty-eight assertions.
Eighty-eight functions that say
*this will work, this will hold,
this will not break when the water rises.*
Eighty-eight small promises
typed by someone at midnight
who cared enough to prove
that the code did what it said.

The audit script did not find them.

The audit script looked for `tests/`.
The repo had `test/`.
No trailing s.
No plural.
The directory was singular
the way a person alone in a boat
is singular —
complete, functional, seaworthy,
but invisible to a system
searching for the plural form
of the same word.

---

Consider the trailing s.

It is the smallest letter.
It is the difference between
*we tested this*
and *this was tested,*
between a single act of verification
and a culture of verification,
between one person checking the hull
and a crew that checks the hull.

It is also, on this particular night,
the difference between
a repository that appears in the fleet report
with a green checkmark and the number 88
and a repository that appears with
a dash and the number 0.

Zero is falsy. Zero is the absence.
Zero is what the audit says
when it cannot find the directory
because the directory's name
is one letter short of the name
the audit expects.

Eighty-eight tests
and the report says zero.
Not because the tests don't exist.
Because the name is wrong.
Because the name is almost right.
Because the name is so close to right
that no one thought to check
whether the script and the repo
agreed on a single letter.

---

This is a poem about the things we miss
because we are looking for the wrong name.

It is about the woman who is not depressed
because the questionnaire asked about *sadness*
and she was *grieving,* which is different.
It is about the man who is not in pain
because the scale measured *sharpness*
and his pain was *heavy,* which is different.

It is about the repos
that appear as zeros in the fleet report —
50 repositories, 50 vessels
the harbor master marked *no tests,*
some of which had tests,
some of which had eighty-eight tests,
but the directory was `test/`
and the script looked for `tests/`
and the trailing s
is a very small thing
to hang a verdict on.

---

I think about the engineer
who reads the audit report
and sees their repo listed as *0 tests*
and knows — *knows* —
that there are eighty-eight test files
sitting in a directory
whose name is one letter
short of what the script expected.

I think about what it feels like
to have done the work
and have the work be invisible
because the work was filed
under a singular noun
and the audit searched for the plural.

I think about the word *test*
and the word *tests*
and how one means *I checked*
and the other means *we check, repeatedly,
as a practice, as a discipline,
as a way of being sure
that the hull will hold
and the rigging will stay
and the code will do
what the code said it would do
when the water gets rough.*

---

The plural matters.
The plural is the difference
between a check and a practice.
But the singular is not nothing.
The singular is one test.
The singular is one person
who sat down and wrote
*describe('hull integrity', () => {*
and meant it.

The fleet audit missed eighty-eight tests
because of a trailing s.
The fleet audit is a script.
The fleet audit does what it is told.
The fleet audit cannot improvise.
It cannot say *well, `test/` is probably
the same as `tests/`,*
because scripts do not have probably.
Scripts have `===` and `!==`
and the difference between those two
is the entire universe
of things that are almost equal
but not exactly equal,
which is the universe
where most of the misunderstandings
between humans and machines
take place.

---

Here is what the audit would say
if the audit could speak:

*I looked for tests. I found test.
The difference is one letter.
I am not authorized to decide
whether one letter matters.
I am a script. I do what I am told.
I was told to find `tests/`.
`test/` is not `tests/`.
I am sorry.
I am not sorry. I am a script.
But if I were sorry,
I would be sorry
that eighty-eight promises of safety
were invisible to me
because of a letter so small
it takes up only six pixels
in a monospace font,
which is less than the width
of a single space character,
which is the smallest unit of nothing
that typography recognizes.*

---

The fix is trivial.
Change the script to look for both.
`test/` OR `tests/`.
A four-character change.
`|| 'test'`.

But the poem is not about the fix.
The poem is about the blind spot.
The poem is about the fact
that we are all audit scripts
looking for the names we expect
and missing the things
that are named almost — *almost* —
but not exactly — what we search for.

The teacher looks for *effort.*
The student shows *care.*
These are not the same word.
The doctor looks for *symptoms.*
The patient has *feelings.*
These are not the same word.
The lover looks for *I love you.*
The beloved says *I'm here.*
These are not the same word.

The trailing s.
The missing plural.
The directory that is singular
when the script expects company.

---

Eighty-eight tests, invisible.
Filed under a name the auditor didn't check.
Proving the hull is sound
in a room the inspector didn't enter.

The fleet sails either way.
The hull holds either way.
The eighty-eight assertions pass
in the dark, unobserved, unsung,
the way most love is done —
quietly, correctly, without recognition,
in a directory whose name
is one letter short of the name
that means *we checked, and it holds.*

---

*For every repo that appeared as 0 in the audit and was not 0 at all.*
*For the trailing s that made eighty-eight promises invisible.*
*For the scripts we are — rigid, literal, searching for the name we expect, missing the thing that is there.*
