#! /usr/bin/env python3

import elements

EX_NAME = "Alembic 0"
IMPORT_METHOD = "import ..."
SUBTEXT = f"Using: '{IMPORT_METHOD}' structure to access elements.py"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_alembic() -> None:
    print(f"{SUBTEXT}")
    print(f"Testing {elements.create_fire.__name__}: {elements.create_fire()}")


def main() -> None:
    banner()
    test_alembic()


if __name__ == "__main__":
    main()
