#!/usr/bin/env python3


import random


EX_NAME = "Achievement Tracker System"
CATALOG = (
    "Brave", "Clever", "Fun", "Lucky", "Fierce",
    "Chill", "Bold", "Quick", "Wise", "Wild",
    "Tough", "Calm", "Patient", "Loyal", "Kind",
)
PLAYER_NAMES = ("Ana", "Pedro", "Paulo", "Thomas", "Laura")
MIN_ACHIEVEMENTS = 5
MAX_ACHIEVEMENTS = 9


COLOR = False
BOXES = False
ALIGNED = False


# color codes in ANSI escape sequences
Q = "\033[0m" if COLOR else ""          # reset
B = "\033[1m" if COLOR else ""          # bold
C = "\033[36m" if COLOR else ""         # cyan
R = "\033[31m" if COLOR else ""         # red
G = "\033[32m" if COLOR else ""         # green
Y = "\033[38;5;179m" if COLOR else ""   # yellow
M = "\033[35m" if COLOR else ""         # magenta
W = "\033[37m" if COLOR else ""         # white


# box drawing characters
AR = "→ " if BOXES else ""
TL = "╭" if BOXES else ""
TR = "╮" if BOXES else ""
BL = "╰" if BOXES else ""
BR = "╯" if BOXES else ""
VB = "│" if BOXES else ""
HB = "─" if BOXES else ""
WIDTH = 48 if BOXES else 0
NL = "\n" if BOXES else ""
EQ = "" if BOXES else "==="
TITLE = f"{EQ} {EX_NAME} {EQ}"

# label column alignment width
LW = 28 if ALIGNED else 0          # label column
VW = 0 if ALIGNED else 0           # value column


def banner() -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{TITLE:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def print_label(label: str, l_clr: str, value: str, v_clr: str) -> None:
    print(f"{l_clr}{label:<{LW}}{Q}"
          f"{v_clr}{value:>{VW}}{Q}")


def gen_player_achievements() -> set[str]:
    n: int = random.randint(MIN_ACHIEVEMENTS, MAX_ACHIEVEMENTS)
    achievements: set[str] = set(random.sample(CATALOG, n))
    return achievements


def build_progress() -> dict[str, set[str]]:
    print()
    progress: dict[str, set[str]] = {}
    for name in PLAYER_NAMES:
        achievements: set[str] = gen_player_achievements()
        progress[name] = achievements
        label: str = f"Player {Y}{name}: "
        value: str = f"{achievements!s}"
        print_label(label, C, value, W)
    return progress


def print_claimed(progress: dict[str, set[str]]) -> set[str]:
    print()
    claimed: set[str] = set()
    for name in PLAYER_NAMES:
        claimed = set.union(claimed, progress[name])
    label: str = "All distinct achievements: "
    value: str = f"{claimed!s}"
    print_label(label, C, value, Y)
    return claimed


def print_common(progress: dict[str, set[str]],
                 claimed: set[str]) -> set[str]:
    print()
    common: set[str] = claimed
    for name in PLAYER_NAMES:
        common = set.intersection(common, progress[name])
    label: str = "Common achievements: "
    value: str = f"{common!s}"
    print_label(label, C, value, M)
    return common


def print_only(progress: dict[str, set[str]]) -> None:
    print()
    for name in PLAYER_NAMES:
        others: set[str] = set()
        for other in PLAYER_NAMES:
            if other != name:
                others = set.union(others, progress[other])
        only: set[str] = set.difference(progress[name], others)
        label: str = f"Only {name} has: "
        value: str = f"{only!s}"
        print_label(label, C, value, G)


def print_missing(progress: dict[str, set[str]],
                  catalog: set[str]) -> None:
    print()
    for name in PLAYER_NAMES:
        missing: set[str] = set.difference(catalog, progress[name])
        label: str = f"{name} is missing: "
        value: str = f"{missing!s}"
        print_label(label, C, value, R)


def main() -> None:
    banner()
    progress: dict[str, set[str]] = build_progress()
    catalog: set[str] = set(CATALOG)
    claimed: set[str] = print_claimed(progress)
    print_common(progress, claimed)
    print_only(progress)
    print_missing(progress, catalog)


if __name__ == "__main__":
    main()
