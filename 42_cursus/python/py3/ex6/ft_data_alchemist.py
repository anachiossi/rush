#!/usr/bin/env python3

# Exercise 6: Data Alchemist
# Authorized: import random, random.*, print(), len(), sum(), round()
#
# Start from a list of player names, some capitalized and some not.
# Two list comprehensions: every name capitalized, then only the names that
# were already capitalized in the initial list.
# Then a dict comprehension mapping the capitalized names to random scores,
# and a second one keeping only the scores above the average.
#

import random


EX_NAME = "Game Data Alchemist"

# A LIST, not a tuple: the subject says "create a list" and its output
# shows square brackets. list() is not authorized in ex6, so it has to
# be written as a list literal to print as one.
# Mixed case on purpose - "some are capitalized and others are not" -
# otherwise both comprehensions below become invisible no-ops.
PLAYERS = ["ana", "Pedro", "paulo", "Thomas", "Laura"]
MIN_SCORE = 50
MAX_SCORE = 950

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
WIDTH = 54 if BOXES else 0
NL = "\n" if BOXES else ""
EQ = "" if BOXES else "==="
TITLE = f"{EQ} {EX_NAME} {EQ}"

# label column alignment width
LW = 38 if ALIGNED else 0
VW = 10 if ALIGNED else 0


def banner() -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{TITLE:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def print_label(label: str, l_col: str, value: str, v_col: str,
                end: str = "\n") -> None:
    print(f"{l_col}{label:<{LW}}{Q}"
          f"{v_col}{value:>{VW}}{Q}", end=end)


def print_original_players(players: list[str]) -> None:
    label = "Initial list of players: "
    value = f"{players!s}"
    print_label(label, C, value, W)


def print_capitalized(players: list[str]) -> None:
    label = "New list with all names capitalized: "
    value = f"{players!s}"
    print_label(label, C, value, Y)


def print_only_caps(only_caps: list[str]) -> None:
    label = "New list of capitalized names only: "
    value = f"{only_caps!s}"
    print_label(label, C, value, G)


def print_scores(scores: dict[str, int]) -> None:
    label = "Score dict: "
    value = f"{scores!s}"
    print_label(label, C, value, M)


def print_average(average: float) -> None:
    label = "Score average is "
    value = f"{round(average, 2)!s}"
    print_label(label, C, value, Y)


def print_high_scores(high: dict[str, int]) -> None:
    label = "High scores: "
    value = f"{high!s}"
    print_label(label, C, value, G)


def main() -> None:
    players: list[str] = [name.capitalize() for name in PLAYERS]
    only_caps: list[str] = [n for n in PLAYERS if n == n.capitalize()]
    scores: dict[str, int] = {player: random.randint(MIN_SCORE, MAX_SCORE)
                              for player in players}
    average: float = sum(scores.values()) / len(scores)
    high: dict[str, int] = {player: scores[player] for player in scores
                            if scores[player] > average}

    banner()
    print()
    print_original_players(PLAYERS)
    print_capitalized(players)
    print_only_caps(only_caps)
    print()
    print_scores(scores)
    print_average(average)
    print_high_scores(high)


if __name__ == "__main__":
    main()
