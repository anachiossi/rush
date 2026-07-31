#!/usr/bin/env python3


import math


EX_NAME = "Game Coordinate System"
PROMPT = "Enter new coordinates as floats in format 'x,y,z': "
ORIGIN = (0.0, 0.0, 0.0)

COLOR = False
BOXES = False


# color codes in ANSI escape sequences
Q = "\033[0m" if COLOR else ""          # reset
B = "\033[1m" if COLOR else ""          # bold
C = "\033[36m" if COLOR else ""         # cyan
R = "\033[31m" if COLOR else ""         # red
G = "\033[32m" if COLOR else ""         # green
Y = "\033[38;5;179m" if COLOR else ""   # yellow
M = "\033[35m" if COLOR else ""         # magenta
XR = "\033[38;5;174m" if COLOR else ""  # soft red
YG = "\033[38;5;150m" if COLOR else ""  # soft green
ZB = "\033[38;5;110m" if COLOR else ""  # soft blue

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


def banner() -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{TITLE:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def parse_position(text: str) -> tuple[float, float, float] | None:
    try:
        x, y, z = text.split(",")
    except ValueError:
        print(f"{R}Invalid syntax{Q}")
        return None

    try:
        for node in (x, y, z):
            float(node)
    except ValueError as error:
        print(f"{R}Error on parameter '{Y}{node}': {R}{error}{Q}")
        return None

    return float(x), float(y), float(z)


def get_player_pos() -> tuple[float, float, float]:

    while True:
        pos = parse_position(input(PROMPT))
        if pos is not None:
            return pos


def calc_distance(start: tuple[float, float, float],
                  end: tuple[float, float, float]) -> float:
    distance = math.sqrt((end[0] - start[0]) ** 2 +
                         (end[1] - start[1]) ** 2 +
                         (end[2] - start[2]) ** 2)
    return distance


def main() -> None:
    banner()
    print()
    print(f"{M}{B}Get a first set of coordinates{Q}")

    pos = get_player_pos()

    print(f"{C}{f'Got a first tuple: '}{Q}"
          f"{pos}")
    print(f"{C}{f'It includes:'}{Q}"
          f" X={XR}{f'{pos[0]}{Q}'},"
          f" Y={YG}{f'{pos[1]}{Q}'},"
          f" Z={ZB}{f'{pos[2]}{Q}'}")

    distance = round(calc_distance(ORIGIN, pos), 4)

    print(f"{C}{f'Distance to center: '}{Q}"
          f"{B}{distance:>.4f}{Q}")
    print()
    print(f"{M}{B}Get a second set of coordinates{Q}")

    pos2 = get_player_pos()
    distance2 = round(calc_distance(pos, pos2), 4)

    print(f"{C}{f'Distance between the 2 sets of coordinates: '}{Q}"
          f"{B}{distance2:>.4f}{Q}")


if __name__ == "__main__":
    main()
