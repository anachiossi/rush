#! /usr/bin/env python3

import alchemy.elements

EX_NAME = "Alembic 2"
IMPORT_METHOD = "import ..."
IMPORT_FROM = "alchemy/elements.py"
SUBTEXT = f"Accessing {IMPORT_FROM} using '{IMPORT_METHOD}' structure"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_alembic_v2() -> None:
    print(f"{SUBTEXT}")
    name = alchemy.elements.create_earth.__name__
    print(f"Testing {name}: {alchemy.elements.create_earth()}")


def main() -> None:
    banner()
    test_alembic_v2()


if __name__ == "__main__":
    main()
