#! /usr/bin/env python3

from alchemy import create_air

EX_NAME = "Alembic 5"
IMPORT_METHOD = "from alchemy import ..."
MODULE = "alchemy"
SUBTEXT = f"Accessing the {MODULE} module using '{IMPORT_METHOD}'"


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
