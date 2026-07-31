# Module 04 output tester

Runs each exercise against the outputs shown in the subject PDF and diffs them.

```bash
cd py04-data-archivist
./expected/check.sh
```

Exit status is `0` only when every case passes, so it works as a
pre-delivery gate.

---

## Usage

```bash
./expected/check.sh                # every case
./expected/check.sh ex1            # only cases starting with "ex1"
./expected/check.sh ex2-denied     # one case
./expected/check.sh -v ex0         # verbose: show output even when passing
```

Runs from anywhere — paths resolve relative to the script, not your shell:

```bash
~/42/cursus/python/py04-data-archivist/expected/check.sh
```

## Result lines

| | meaning |
|---|---|
| `OK` | stdout **and** stderr both match |
| `FAIL` | something differs — a diff or a traceback follows |
| `SKIP` | your `ft_*.py` is empty or missing (not written yet) |

In every diff, **`<` is your output and `>` is what the subject expects.**

## Does it show traces?

Yes. stdout and stderr are captured **separately and never merged**, so:

- **If your program crashes**, the case prints `CRASHED - traceback:`
  followed by the full Python traceback. You get the file, line number and
  exception, not a confusing output diff.
- **If output merely differs**, you get two labelled diffs — one for stdout,
  one for stderr — so you can see *which stream* was wrong.

That separation matters for ex2 specifically. Its whole point is that errors
belong on stderr. A tester that merged the streams (like the py02 one)
would happily pass a program that printed every error to stdout. This one
fails it, and shows you the line on the wrong stream.

The exit code of your program is printed on every line (`exit 0`, `exit 1`).
Nothing in the subject requires a particular exit code, so it is shown for
information only and never compared.

---

## How cases work

Everything lives in `cases/`. One case = a set of files sharing a name:

| file | meaning |
|---|---|
| `NAME.args` | command-line arguments, **one per line**. Absent = no arguments. |
| `NAME.in` | text fed to stdin. Absent = `/dev/null`, i.e. immediate EOF. |
| `NAME.out` | expected stdout. **Required** — this is what defines a case. |
| `NAME.err` | expected stderr. Absent = stderr must be **empty**. |

The part before the first `-` picks the exercise: `ex2-denied` runs
`ex2/ft_stream_management.py`.

### Current cases

| case | what it checks |
|---|---|
| `ex0-usage` | no argument → usage message |
| `ex0-missing` | nonexistent file → Errno 2 |
| `ex0-denied` | unreadable file → Errno 13 |
| `ex0-read` | normal file → header, content, footer |
| `ex1-nosave` | empty filename → "Not saving data." |
| `ex1-save` | filename given → transform written to disk |
| `ex2-missing` | error goes to **stderr**, not stdout |
| `ex2-denied` | write to `/etc/passwd` → stderr error, "Data not saved." |
| `ex3-demo` | the four `secure_archive()` results |

### Adding a case

```bash
cd expected/cases
printf 'somefile.txt\n' > ex0-mycase.args      # arguments
./../check.sh ex0-mycase                        # run it, copy the output
```

Then paste the correct output into `ex0-mycase.out`. Verify the expectation
against the **subject PDF**, not against your own program — otherwise you are
only testing that your code still does what it did yesterday.

---

## Dropping it into another repo

`expected/` is self-contained and location-independent. Copy the whole folder
so it sits **next to `ex0/ ex1/ ex2/ ex3/`** and run it — the script resolves
every path relative to itself, not to your shell's working directory. The
parent folder can be named anything.

Verified by copying it into a differently-named folder in a different
location, with four different implementations: 9 passed.

The only requirement is that layout:

```
whatever-you-called-it/
├── ex0/ft_ancient_text.py
├── ex1/ft_archive_creation.py
├── ex2/ft_stream_management.py
├── ex3/ft_vault_security.py
└── expected/          <- drop this in
```

### On a school Mac

Written to survive macOS, which is not a given for bash scripts:

- **No `declare -A`.** macOS ships bash 3.2 (2007 — Apple froze it over the
  GPLv3 licence change), which has no associative arrays. This script uses a
  `case` statement instead.
- **No `timeout`.** That is GNU coreutils, absent from stock macOS. The script
  detects `timeout`, then `gtimeout` (Homebrew), and runs without a watchdog
  if neither exists. Tested with the watchdog forced off: 9 passed.
- **`set -u` + empty array.** In bash 3.2, `"${args[@]}"` on an empty array
  aborts as an unbound variable — which would break the no-argument case
  (`ex0-usage`). Written as `${args[@]+"${args[@]}"}` to avoid it.

If a case ever hangs on a Mac with no `timeout`, press Ctrl-C — that almost
certainly means your program is blocking on a stdin read.

## Isolation

Each case runs in a fresh `mktemp -d` directory containing a copy of
`ancient_fragment.txt` and a copy of your `.py`. So:

- files your program writes (`new_fragment.txt`) never land in the repo
- `ancient_fragment.txt` is always pristine
- `argv[0]` is the plain filename, so a hardcoded usage string matches
- a 10-second `timeout` stops a program that blocks forever on stdin

---

## Things that can legitimately differ

Read these before assuming your code is wrong.

**1. `ex0-denied` assumes you are not root.** It expects
`[Errno 13] Permission denied: '/etc/shadow'`. As root, `/etc/shadow` is
readable and the case fails for the wrong reason. Same for `ex2-denied`,
which writes to `/etc/passwd`.

**2. The subject was written on macOS.** It uses `/etc/master.passwd` for the
"inaccessible file" example. That path **does not exist on Linux** — you get
`[Errno 2] No such file or directory`, not `[Errno 13] Permission denied`. The
cases here use `/etc/shadow`, which really is permission-denied on Linux.
If you hardcode the subject's path, the error you demonstrate will be the
wrong one.

**3. `ex3-demo` depends on paths *you* choose.** The subject's `main` uses
hardcoded paths, so the expected output can only match if you use the same
ones. `ex3-demo.out` assumes:

```
/not/existing/file        nonexistent
/etc/shadow               permission denied
ancient_fragment.txt      readable
new_vault.txt             the write target
```

Use different paths and the case will fail even though your code is correct —
edit `ex3-demo.out` to match your choices.

**4. `ex1`/`ex2` prompts have no trailing newline.** `Enter new file name
(or empty): ` is printed with no `\n`, so the next message lands on the
**same line**. That is correct and the expected files reflect it.

---

## Not a substitute for

```bash
flake8 ex*/ft_*.py
mypy --strict ex*/ft_*.py
python3 -m compileall -q ex0 ex1 ex2 ex3
```

This tester only checks observable output. It cannot see missing type hints,
style violations, or a call that is not on the exercise's **Authorized** list —
and that last one is the difference between a pass and an automatic fail.
Check the authorized list per exercise, by hand, every time; it changes
between exercises on purpose.

---

## Before delivering

Delete this `expected/` folder. The subject says to submit only the requested
files.
