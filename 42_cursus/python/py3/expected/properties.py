#!/usr/bin/env python3
"""Invariant checks for the RANDOM exercises: ex3, ex5, ex6.

check.sh compares output literally, which only works when the output is
determined by the input. ex3, ex5 and ex6 use `random`, so there is no
fixed expected output to diff against.

What IS fixed is the RELATIONSHIPS between the numbers - the union
really must be the union, the drained events really must be the ones
that were built, the high scores really must be above the average.
Those hold on every run whatever the dice say, so they can be checked.

That is property-based testing, and randomness is what forces you into
it. It is usually a stronger check than a golden file: a golden file
proves your program still does what it did yesterday, while these
properties prove it does what the SUBJECT says.

Every run also writes expected/traces-properties.txt: the full output of
a representative run of each exercise, plus the verdict. On a failure it
records the run that FAILED, so you can read the output that broke the
invariant instead of trying to reproduce it. Override the path with
TRACE_FILE=/somewhere/else.txt ./properties.py

Usage:
    ./properties.py                 # every exercise, root files, 20 runs
    ./properties.py ex3             # one exercise
    ./properties.py -a 3            # test ex*/alt/ft_*_v3.py instead
    ./properties.py -c              # test ex*/color/ft_*_vc.py instead
    ./properties.py -a 5 ex5 -n 50  # 50 runs of one alt version

This is a TEST HARNESS, not exercise code: it uses whatever it likes
from the standard library. The authorized-list rules apply to what you
submit, not to the tools you build around it.
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE.parent

CANONICAL = {
    "ex3": "ft_achievement_tracker.py",
    "ex5": "ft_data_stream.py",
    "ex6": "ft_data_alchemist.py",
}

RED = "\033[31m"
GRN = "\033[32m"
YEL = "\033[33m"
DIM = "\033[2m"
OFF = "\033[0m"


class Failure(Exception):
    """An invariant did not hold."""


def source_for(exercise: str, alt: str | None,
               color: bool = False) -> Path:
    """Path to the implementation under test."""
    canonical = CANONICAL[exercise]
    stem = canonical[:-len(".py")]
    if color:
        return MODULE / exercise / "color" / f"{stem}_vc.py"
    if alt is None:
        return MODULE / exercise / canonical
    return MODULE / exercise / "alt" / f"{stem}_v{alt}.py"


def is_written(path: Path) -> bool:
    """False for a skeleton that is only a shebang and comments."""
    if not path.is_file():
        return False
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return True
    return False


def run(path: Path) -> list[str]:
    """Run the program and return its stdout lines. Raises on crash."""
    result = subprocess.run(
        [sys.executable, path.name],
        cwd=path.parent,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise Failure(f"exited {result.returncode}\n{result.stderr.strip()}")
    if result.stderr.strip():
        raise Failure(f"wrote to stderr: {result.stderr.strip()}")
    return result.stdout.splitlines()


def parse_set(text: str) -> set[str]:
    """Parse a printed set. `set()` is not a literal, so handle it."""
    text = text.strip()
    if text == "set()":
        return set()
    value = ast.literal_eval(text)
    if not isinstance(value, set):
        raise Failure(f"expected a set, got {type(value).__name__}: {text}")
    return value


def need(lines: list[str], pattern: str) -> list[re.Match[str]]:
    """Every line matching `pattern`, or raise if there are none."""
    found = [m for m in (re.match(pattern, ln) for ln in lines) if m]
    if not found:
        raise Failure(f"no line matching {pattern!r}")
    return found


# --------------------------------------------------------------------
# ex3 - Achievement Hunter
# --------------------------------------------------------------------
def check_ex3(lines: list[str]) -> bool:
    """Union, intersection, exclusivity and complement must agree.

    Returns True if the catalogue was STRICTLY larger than the union on
    this run - i.e. some achievement was rolled by nobody. See
    diagnose_ex3 for why that single bit is worth returning.
    """
    if lines[0] != "=== Achievement Tracker System ===":
        raise Failure(f"bad header: {lines[0]!r}")

    players: dict[str, set[str]] = {}
    for m in need(lines, r"^Player (\w+): (.+)$"):
        players[m.group(1)] = parse_set(m.group(2))
    if len(players) < 4:
        raise Failure(f"subject requires >= 4 players, found {len(players)}")

    distinct = parse_set(need(lines, r"^All distinct achievements: (.+)$")[0]
                         .group(1))
    common = parse_set(need(lines, r"^Common achievements: (.+)$")[0].group(1))

    only: dict[str, set[str]] = {}
    for m in need(lines, r"^Only (\w+) has: (.+)$"):
        only[m.group(1)] = parse_set(m.group(2))

    missing: dict[str, set[str]] = {}
    for m in need(lines, r"^(\w+) is missing: (.+)$"):
        missing[m.group(1)] = parse_set(m.group(2))

    if set(only) != set(players) or set(missing) != set(players):
        raise Failure("the four report blocks name different players")

    # union
    expected_union: set[str] = set().union(*players.values())
    if distinct != expected_union:
        raise Failure("'All distinct' is not the union of the players")

    # intersection
    first = next(iter(players.values()))
    expected_common = first.intersection(*players.values())
    if common != expected_common:
        raise Failure("'Common' is not the intersection of the players")

    # the catalogue must be the SAME universe for every player, and it
    # must be a superset of the union - this is the ex3 trap: computing
    # 'missing' against the union instead of the catalogue.
    universes = {name: missing[name] | players[name] for name in players}
    catalogs = set(frozenset(u) for u in universes.values())
    if len(catalogs) != 1:
        raise Failure(
            "'is missing' is measured against a different universe for "
            "different players - it must always be the whole catalogue"
        )
    catalog = set(next(iter(catalogs)))
    if not expected_union <= catalog:
        raise Failure("the catalogue does not contain every owned achievement")

    for name, owned in players.items():
        if missing[name] != catalog - owned:
            raise Failure(f"'{name} is missing' != catalogue - owned")
        if not missing[name].isdisjoint(owned):
            raise Failure(f"'{name} is missing' overlaps what {name} owns")
        others: set[str] = set()
        for other, other_owned in players.items():
            if other != name:
                others |= other_owned
        if only[name] != owned - others:
            raise Failure(f"'Only {name} has' != owned - the other players")

    return catalog > expected_union


def diagnose_ex3(evidence: list[bool]) -> str:
    """Heuristic for the ex3 trap, which no SINGLE run can detect.

    Measuring "is missing" against the union instead of the catalogue
    produces output that is entirely self-consistent: every player's
    (missing | owned) equals the union, so all the per-run invariants
    above still hold. The two implementations differ only when some
    achievement was rolled by NOBODY - then the correct one still
    reports it as missing, and the buggy one cannot.

    So the tell is cross-run: with a catalogue of 14 and four players
    drawing 5-9, roughly half of all runs leave at least one
    achievement unrolled. If that NEVER happens across many runs, either
    the draw always covers the catalogue (legitimate - a small
    catalogue or large draws) or "missing" is being measured against
    the union.

    This is a WARNING, not a failure. It is a statistical hint, and a
    valid implementation can trip it.
    """
    if evidence and not any(evidence):
        return (
            f"in {len(evidence)} runs the catalogue was NEVER larger than "
            "the union of what players own.\n"
            "Either your draw sizes always cover the catalogue, or "
            "'X is missing' is being computed\n"
            "against the union instead of the whole catalogue - the ex3 "
            "trap. Check ex3/alt/..._v3.py."
        )
    return ""


# --------------------------------------------------------------------
# ex5 - Stream Wizard
# --------------------------------------------------------------------
def check_ex5(lines: list[str]) -> bool:
    """1000 numbered events, then a sample drained to nothing."""
    if lines[0] != "=== Game Data Stream Processor ===":
        raise Failure(f"bad header: {lines[0]!r}")

    events = need(lines, r"^Event (\d+): Player (\w+) did action (\w+)$")
    if len(events) != 1000:
        raise Failure(f"expected 1000 events, found {len(events)}")
    numbers = [int(m.group(1)) for m in events]
    if numbers != list(range(1000)):
        raise Failure("events are not numbered 0..999 in order")

    built = ast.literal_eval(
        need(lines, r"^Built list of \d+ events: (\[.*\])$")[0].group(1))
    if len(built) != 10:
        raise Failure(f"sample should hold 10 events, holds {len(built)}")
    for event in built:
        if not (isinstance(event, tuple) and len(event) == 2):
            raise Failure(f"event is not a 2-tuple: {event!r}")

    got = [ast.literal_eval(m.group(1))
           for m in need(lines, r"^Got event from list: (\(.+\))$")]
    remains = [ast.literal_eval(m.group(1))
               for m in need(lines, r"^Remains in list: (\[.*\])$")]

    if len(got) != 10 or len(remains) != 10:
        raise Failure(f"drained {len(got)} events, {len(remains)} remains "
                      "lines - both should be 10")

    # laziness: the caller sees the list shrink one item at a time
    if [len(r) for r in remains] != [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
        raise Failure(
            "'Remains in list' lengths are not 9,8,...,0 - the generator "
            "is not being consumed lazily, or is not removing items"
        )
    if remains[-1] != []:
        raise Failure("the list is not empty at the end")

    # conservation: drained events are exactly the ones built
    if sorted(got) != sorted(built):
        raise Failure("the drained events are not the ones that were built")

    return False


# --------------------------------------------------------------------
# ex6 - Data Alchemist
# --------------------------------------------------------------------
def check_ex6(lines: list[str]) -> bool:
    """Comprehension results must agree with each other."""
    if lines[0] != "=== Game Data Alchemist ===":
        raise Failure(f"bad header: {lines[0]!r}")

    initial = ast.literal_eval(
        need(lines, r"^Initial list of players: (\[.*\])$")[0].group(1))
    capitalized = ast.literal_eval(
        need(lines, r"^New list with all names capitalized: (\[.*\])$")[0]
        .group(1))
    only_caps = ast.literal_eval(
        need(lines, r"^New list of capitalized names only: (\[.*\])$")[0]
        .group(1))

    if not any(n != n.capitalize() for n in initial):
        raise Failure("the initial list has no lowercase names - the subject "
                      "asks for a mix")
    if capitalized != [n.capitalize() for n in initial]:
        raise Failure("the capitalized list is not capitalize() of "
                      "the initial list")
    if len(only_caps) >= len(initial):
        raise Failure("'capitalized names only' did not filter anything")
    for name in only_caps:
        if name not in initial:
            raise Failure(f"{name!r} is not in the initial list")

    scores = ast.literal_eval(
        need(lines, r"^Score dict: (\{.*\})$")[0].group(1))
    if set(scores) != set(capitalized):
        raise Failure("the score dict is not keyed by the capitalized names")
    for name, score in scores.items():
        if not isinstance(score, int):
            raise Failure(f"score for {name} is {type(score).__name__}, "
                          "not int")

    shown = float(need(lines, r"^Score average is ([\d.]+)$")[0].group(1))
    average = sum(scores.values()) / len(scores)
    if abs(shown - round(average, 2)) > 1e-9:
        raise Failure(f"average shown {shown}, computed {round(average, 2)}")

    high = ast.literal_eval(
        need(lines, r"^High scores: (\{.*\})$")[0].group(1))
    expected_high = {n: s for n, s in scores.items() if s > average}
    if high != expected_high:
        raise Failure("'High scores' is not the entries above the average")

    return False


CHECKS = {"ex3": check_ex3, "ex5": check_ex5, "ex6": check_ex6}
DIAGNOSTICS = {"ex3": diagnose_ex3}


def main() -> int:
    """Run the invariant checks and report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("exercise", nargs="?", choices=sorted(CHECKS))
    parser.add_argument("-a", "--alt", help="test ex*/alt/ft_*_vN.py")
    parser.add_argument("-c", "--color", action="store_true",
                        help="test ex*/color/ft_*_vc.py")
    parser.add_argument("-n", "--runs", type=int, default=20)
    options = parser.parse_args()

    targets = [options.exercise] if options.exercise else sorted(CHECKS)
    if options.color:
        print(f"  {DIM}testing signature-style color/ versions{OFF}\n")
    elif options.alt:
        print(f"  {DIM}testing alt version v{options.alt}{OFF}\n")

    target_label = ("signature-style color/ versions" if options.color
                    else f"alt version v{options.alt}" if options.alt
                    else "ex*/ft_*.py")
    trace: list[str] = [
        f"py03 property trace - {datetime.now():%Y-%m-%d %H:%M:%S}",
        f"target: {target_label}",
        "Invariants cannot be diffed, so this records the OUTPUT they were",
        "checked against - the failing run if there was one.",
    ]

    failed = 0
    skipped = 0
    for exercise in targets:
        path = source_for(exercise, options.alt, options.color)
        label = str(path.relative_to(MODULE))

        if not is_written(path):
            print(f"  {YEL}SKIP{OFF}    {exercise:<6} "
                  f"{DIM}({label} not written yet){OFF}")
            trace.append(f"\n=== {exercise} === SKIP "
                         f"({label} not written yet)")
            skipped += 1
            continue

        problem = ""
        evidence: list[bool] = []
        sample: list[str] = []
        for _ in range(options.runs):
            try:
                sample = run(path)
                evidence.append(CHECKS[exercise](sample))
            except Failure as error:
                problem = str(error)
                break
            except (ValueError, SyntaxError, IndexError) as error:
                problem = f"could not parse the output: {error}"
                break

        trace.append(f"\n=== {exercise} ===")
        trace.append(f"    source : {label}")
        trace.append(f"    runs   : {options.runs}")
        verdict = f"FAIL - {problem}" if problem else "all invariants held"
        which = "the run that FAILED" if problem else "a representative run"
        trace.append(f"    result : {verdict}")
        trace.append(f"\n    --- {which} ---")
        trace.extend(f"    | {line}" for line in sample)

        if problem:
            print(f"  {RED}FAIL{OFF}    {exercise:<6} {DIM}{label}{OFF}")
            for line in problem.splitlines():
                print(f"            {line}")
            failed += 1
        else:
            print(f"  {GRN}OK{OFF}      {exercise:<6} "
                  f"{DIM}{options.runs} runs, all invariants held{OFF}")
            diagnose = DIAGNOSTICS.get(exercise)
            if diagnose:
                warning = diagnose(evidence)
                if warning:
                    print(f"  {YEL}WARN{OFF}    {exercise:<6} "
                          f"{DIM}(heuristic, not a failure){OFF}")
                    for line in warning.splitlines():
                        print(f"            {line}")

    summary = (f"{len(targets) - failed - skipped} passed, {failed} failed, "
               f"{skipped} skipped")
    print(f"\n  {summary}")

    trace.append(f"\n{summary}")
    trace_path = Path(os.environ.get("TRACE_FILE",
                                     HERE / "traces-properties.txt"))
    trace_path.write_text("\n".join(trace) + "\n")
    print(f"  {DIM}trace: {trace_path}{OFF}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
