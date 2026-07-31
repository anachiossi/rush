# Module 03 testers

Two tools, because py03 has two kinds of exercise.

```bash
cd py03-data-quest
./expected/check.sh          # ex0, ex1, ex2, ex4  - exact output
./expected/properties.py     # ex3, ex5, ex6       - invariants
```

Both exit non-zero on failure, so either works as a pre-delivery gate.
Both resolve paths relative to themselves, so they run from anywhere.

| | exercises | how it checks |
|---|---|---|
| `check.sh` | ex0, ex1, ex2, ex4 | diffs stdout and stderr against `cases/*.out` |
| `properties.py` | ex3, ex5, ex6 | runs N times, checks relationships that hold on every run |

The split is forced by the subject: ex3, ex5 and ex6 use `random`, so
they have no fixed output to diff against. See "Testing something
random" below.

---

## Testing the alt/ versions

Both tools take `-a N` to test `exN/alt/ft_*_vN.py` instead of your own
file at the exercise root:

```bash
./expected/check.sh -a 3            # every case against v3
./expected/properties.py -a 5 ex5   # ex5's v5, invariants only
```

That is how the reference versions were verified: all five pass all 12
cases and all invariants.

**`check.sh` copies the source under its canonical name** (always
`ft_score_analytics.py`, never `ft_score_analytics_v3.py`) into the temp
directory it runs in. ex1's usage line prints `argv[0]`, so without this
an alt version could never match the subject's expected text. If you
write a version that prints its own filename, this is why it still
passes.

---

## Other flags

```bash
./expected/check.sh ex1              # only cases starting with "ex1"
./expected/check.sh -v ex1-mixed     # show output even when passing
./expected/properties.py ex3         # one exercise
./expected/properties.py -n 100      # 100 runs instead of 20
```

## Result lines

| | meaning |
|---|---|
| `OK` | stdout **and** stderr both match |
| `FAIL` | something differs — a diff or a traceback follows |
| `SKIP` | your `ft_*.py` is still just the shebang and comment header |
| `WARN` | a heuristic fired. Not a failure. Read it. |

In every diff, **`<` is your output and `>` is what the subject expects.**

---

## Traces

Every run writes a plain-text trace next to these scripts. No colours, so
it reads well in an editor and diffs cleanly between runs.

| file | written by | contents |
|---|---|---|
| `traces.txt` | `check.sh` | your output and the expected output **side by side**, for every case |
| `traces-properties.txt` | `properties.py` | the full output of a representative run — the **failing** one if there was a failure |

Override either with `TRACE_FILE=/somewhere/else.txt ./check.sh`.

`traces.txt` pairs the two outputs line by line and marks every
difference with `!`. Both files are recorded even for passing cases, so
you can see what correct looks like:

```
    --- stdout ---
      line | got                        | expected
         1 | === Command Quest ===      | === Command Quest ===
    !    2 | No arguments provided!     | Program name: ft_command_quest.py
    !    3 | Total arguments: 1         | No arguments provided!
    !    4 | <missing>                  | Total arguments: 1
```

**Read that carefully before fixing three things.** It is *one* bug: a
missing `Program name:` line. Everything below a missing line shifts up
by one and flags as different. `<missing>` at the end is the tell — your
output is one line short, so look for something absent, not for three
wrong lines.

`properties.py` cannot diff anything — an invariant either holds or does
not, and the output is random — so its trace records the output the
invariants were checked against, plus which one broke.

`SKIP` detects an unwritten skeleton as "no line whose first non-blank
character is anything but `#`" — not "empty file", because the
skeletons ship with a header. Delete the header or start writing and the
cases activate.

---

## Testing something random

You cannot assert on ex3/ex5/ex6's output. You can assert on the
relationships inside it, which hold on every possible run:

**ex3** — `All distinct` is the union of the players; `Common` is the
intersection; `Only X has` is X minus the *other players*; `X is
missing` is the *whole catalogue* minus X; missing and owned are
disjoint and reconstruct the catalogue.

**ex5** — exactly 1000 events numbered 0..999; the sample holds 10
2-tuples; `Remains in list` shrinks 9, 8, … 0 (which is what proves the
generator is consumed **lazily**, one item per loop iteration); the
drained events are exactly the ones that were built.

**ex6** — the capitalized list is `capitalize()` of the initial one; the
score dict is keyed by it; the printed average equals the real one to 2
decimals; `High scores` is exactly the entries above the *unrounded*
average.

This is property-based testing. It is usually a stronger check than a
golden file: a golden file proves your program still does what it did
yesterday; these prove it does what the subject says.

### The one bug this cannot catch on its own

Computing `X is missing` against the **union** instead of the
**catalogue** is the classic ex3 mistake. It produces output that is
completely self-consistent — every player's `missing | owned` equals the
union, so every per-run invariant above still holds. Verified: a
deliberately broken version passes 30 runs of the per-run checks.

The two versions differ only when some achievement is rolled by nobody.
So `properties.py` collects that one bit across runs and emits a `WARN`
if the catalogue was *never* larger than the union. That is a
statistical hint, not proof — a legitimate implementation whose draw
sizes always cover the catalogue will trip it too.

Worth sitting with: **a self-consistent wrong answer is invisible to a
test that only checks self-consistency.**

---

## Not a substitute for

```bash
flake8 ex*/ft_*.py
mypy --strict ex*/ft_*.py
python3 -m compileall -q ex0 ex1 ex2 ex3 ex4 ex5 ex6
```

These testers only check observable output. They cannot see a missing
type hint, a style violation, or a call that is not on the exercise's
**Authorized** list — and that last one is the difference between a pass
and an automatic fail.

For py03 the authorized rules are wider than the per-exercise line
suggests. Read all three together:

- **p.6** — `str`, `int`, `float` with *all* their methods and
  constructors, everywhere. So `int()`, `.split()`, `.strip()`,
  `.capitalize()`, `.join()` are always fine.
- **p.5** — each data structure and *all* its class methods, once an
  exercise introduces it. Lists from ex0, tuples ex2, sets ex3, dicts
  ex4. So `.append()` and `.items()` are fine.
- **the exercise's own line** — the *builtins and modules* you may use.
  This is the real restriction: `enumerate()` is not available in ex0,
  `len()` is not in ex2, `max()`/`min()` are not in ex4.

Check the list per exercise, by hand, every time. It changes between
exercises on purpose.

---

## Before delivering

Delete this `expected/` folder and the `alt/` folders. The subject says
to submit only the requested files.
