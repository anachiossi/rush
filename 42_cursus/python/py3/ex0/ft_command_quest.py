#! /usr/bin/env python3


import sys


EX_NAME = "Command Quest"

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
LW = 28 if ALIGNEMENT else 0         # left
RW = 20 if ALIGNEMENT else 0         # right aligned


def banner() -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{TITLE:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def command_quest() -> tuple[int, list[str]]:
    argc = len(sys.argv)
    argv: list[str] = sys.argv
    return argc, argv


def print_command(argc: int, argv: list[str]) -> None:
    banner()
    print(f"{C}{f'Program name: ':<{LW}}{Q}{Y}{argv[0]:>{RW}}{Q}")
    if argc == 1:
        print(f"{C}{f'No arguments provided!':<{LW}}{Q}")
    else:
        print(f"{C}{f'Arguments received: ':<{LW}}{Q}{argc - 1:>{RW}}")
        i = 1
        while i < argc:
            print(f"{C}{f'Argument {i}: ':<{LW}}{Q}{argv[i]:>{RW}}")
            i += 1
    print(f"{C}{f'Total arguments: ':<{LW}}{Q}{argc:>{RW}}")


def main() -> None:
    argc, argv = command_quest()
    print_command(argc, argv)


if __name__ == "__main__":
    main()
