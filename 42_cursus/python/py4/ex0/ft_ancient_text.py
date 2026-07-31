import sys


EX_NAME = "Cyber Archives Recovery"

COLOR = False
BOXES = False

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
DL = "─" * 3 if BOXES else "---"   # content delimiter
TITLE = f"{EQ} {EX_NAME} {EQ}"


def banner() -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{TITLE:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def read_archive(file_name: str) -> None:
    banner()
    print(f"{C}Accessing file {AR}{Y}'{file_name}'{Q}")
    f = None
    try:
        f = open(file_name)
        content = f.read()
    except (OSError, UnicodeError) as e:
        print(f"{R}Error opening file {AR}{Y}'{file_name}'{R}: {e}{Q}")
    else:
        print(f"{DL}\n\n{content}\n{DL}")
    finally:
        if f is not None:
            f.close()
            print(f"{C}File {AR}{Y}'{file_name}'{C} closed.{Q}")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"{R}Usage: {Y}{sys.argv[0]} <file>{Q}")
        return
    file_name = sys.argv[1]
    read_archive(file_name)


if __name__ == "__main__":
    main()
