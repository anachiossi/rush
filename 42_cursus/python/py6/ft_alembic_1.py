#! /usr/bin/env python3

from elements import create_water

EX_NAME = "Alembic 1"
IMPORT_METHOD = "from ... import ..."
SUBTEXT = f"Using: '{IMPORT_METHOD}' structure to access elements.py"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_alembic() -> None:
    print(f"{SUBTEXT}")
    print(f"Testing {create_water.__name__}: {create_water()}")


def main() -> None:
    banner()
    test_alembic()


if __name__ == "__main__":
    main()
