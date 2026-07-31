#!/usr/bin/env python3


import random
from typing import Generator


EX_NAME = "Game Data Stream Processor"

PLAYERS = ("Ana", "Pedro", "Paulo", "Thomas", "Laura")
ACTIONS = ("run", "rest", "sleep", "take", "use",
           "release", "jump", "call", "dogde")

REPEAT = 1000
SAMPLE_SIZE = 10

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
LW = 0 if ALIGNED else 0
VW = 10 if ALIGNED else 0


def banner() -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{TITLE:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def sub_banner(sub_title: str) -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{sub_title:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def print_label(label: str, l_col: str, value: str, v_col: str,
                end: str = "\n") -> None:
    print(f"{l_col}{label:<{LW}}{Q}"
          f"{v_col}{value:>{VW}}{Q}", end=end)


def print_event(index: int, player: str, action: str) -> None:
    label = "Event "
    value = f"{index}: "
    print_label(label, C, value, W, end="")
    label = "Player "
    value = f"{player}"
    print_label(label, C, value, Y, end="")
    label = " did action "
    value = f"{action}"
    print_label(label, C, value, M, end="\n")


def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        player = random.choice(PLAYERS)
        action = random.choice(ACTIONS)
        yield player, action


def call_gen(n: int) -> None:
    event = gen_event()
    for i in range(n):
        player, action = next(event)
        print_event(i, player, action)


def create_event_list(n: int) -> list[tuple[str, str]]:
    event = gen_event()
    event_list: list[tuple[str, str]] = []
    for _ in range(n):
        event_list.append(next(event))
    return event_list


def print_event_list(event_list: list[tuple[str, str]]) -> None:
    n = len(event_list)
    label = f"Built list of {n} events: "
    value = f"{event_list}"
    print_label(label, C, value, G)


def consume_event(events: list[tuple[str, str]]
                  ) -> Generator[tuple[str, str], None, None]:
    while events:
        index = random.randrange(len(events))
        yield events.pop(index)


def print_consumed_event(event: tuple[str, str],
                         event_list: list[tuple[str, str]]) -> None:
    label = "Got event from list: "
    value = f"{event}"
    print_label(label, C, value, R)
    label = "Remains in list: "
    value = f"{event_list}"
    print_label(label, C, value, G)


def main() -> None:
    banner()
    call_gen(REPEAT)
    if BOXES:
        sub_banner(f"Draining a list of {SAMPLE_SIZE} events")
    event_list = create_event_list(SAMPLE_SIZE)
    print_event_list(event_list)
    for event in consume_event(event_list):
        print_consumed_event(event, event_list)


if __name__ == "__main__":
    main()
