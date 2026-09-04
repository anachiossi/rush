#! /usr/bin/env python3

import alchemy

EX_NAME = "Alembic 4"
IMPORT_LITERAL = "import alchemy"
MODULE = "alchemy"
SUBTEXT = f"Accessing the {MODULE} module using '{IMPORT_LITERAL}'"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_alembic_v2() -> None:
    print(f"{SUBTEXT}")
    print(f"Testing {alchemy.create_air.__name__}: {alchemy.create_air()}")


def test_reach() -> None:
    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    print("Testing the hidden create_earth:")
    print(alchemy.create_earth())


def main() -> None:
    banner()
    test_alembic_v2()
    test_reach()


if __name__ == "__main__":
    main()
