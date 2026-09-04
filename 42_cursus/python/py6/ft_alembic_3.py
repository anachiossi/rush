#! /usr/bin/env python3

from alchemy.elements import create_air

EX_NAME = "Alembic 3"
IMPORT_METHOD = "from ... import ..."
IMPORT_FROM = "alchemy/elements.py"
SUBTEXT = f"Accessing {IMPORT_FROM} using '{IMPORT_METHOD}' structure"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_alembic_v2() -> None:
    print(f"{SUBTEXT}")
    print(f"Testing {create_air.__name__}: {create_air()}")


def main() -> None:
    banner()
    test_alembic_v2()


if __name__ == "__main__":
    main()
