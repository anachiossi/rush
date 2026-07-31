#!/usr/bin/env python3


import sys


EX_NAME = "Player Score Analytics"

COLOR = False
BOXES = False
ALIGNEMENT = False

# color codes in ANSI escape sequences
Q = "\033[0m" if COLOR else ""         # reset
B = "\033[1m" if COLOR else ""         # bold
C = "\033[36m" if COLOR else ""        # cyan
R = "\033[31m" if COLOR else ""        # red
G = "\033[32m" if COLOR else ""        # green
Y = "\033[38;5;179m" if COLOR else ""  # yellow
M = "\033[35m" if COLOR else ""        # magenta

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

# label values
LW = 20 if ALIGNEMENT else 0         # left
RW = 10 if ALIGNEMENT else 0         # right aligned


def banner() -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{TITLE:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def parse_scores(argv: list[str]) -> tuple[list[int], list[str]]:
    valid_scores: list[int] = []
    invalid_scores: list[str] = []
    for score in argv[1:]:
        try:
            valid_scores.append(int(score))
        except ValueError:
            invalid_scores.append(score)
    return valid_scores, invalid_scores


def print_scores(valid_scores: list[int], invalid_scores: list[str]) -> None:
    if invalid_scores:
        for invalid in invalid_scores:
            print(f"{R}{f'Invalid parameter: '}{Q}{Y}'{invalid}'{Q}")
    if valid_scores:
        print(f"{C}{f'Scores processed: '}{Q}{valid_scores}{Q}")
    if not valid_scores:
        print(f"{R}No scores provided. {Q}", end="")
        print(f"{R}Usage: {Q}python3 {Y}{sys.argv[0]}"
              f" <score1> <score2> ...{Q}")
        return
    total_scores = sum(valid_scores)
    players = len(valid_scores)
    highest = max(valid_scores)
    lowest = min(valid_scores)
    average = total_scores / len(valid_scores)

    print(f"{C}{f'Total players: ':<{LW}}{Q}{players:>{RW}}")
    print(f"{C}{f'Total score: ':<{LW}}{Q}{total_scores:>{RW}}")
    print(f"{C}{f'Average score: ':<{LW}}{Q}{average:>{RW}.1f}")
    print(f"{C}{f'High score: ':<{LW}}{Q}{G}{highest:>{RW}}")
    print(f"{C}{f'Low score: ':<{LW}}{Q}{R}{lowest:>{RW}}")
    print(f"{C}{f'Score range: ':<{LW}}{Q}{highest - lowest:>{RW}}")


def player_score_analytics() -> None:
    banner()
    valid_scores, invalid_scores = parse_scores(sys.argv)
    print_scores(valid_scores, invalid_scores)


def main() -> None:
    if len(sys.argv) < 2:
        banner()
        print(f"{R}No scores provided. {Q}", end="")
        print(f"{R}Usage: {Q}python3 {Y}{sys.argv[0]}"
              f" <score1> <score2> ...{Q}")
        return
    player_score_analytics()


if __name__ == "__main__":
    main()
