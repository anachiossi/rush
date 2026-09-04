#! /usr/bin/env python3

import alchemy

EX_NAME = "Distillation 1"
IMPORT_METHOD = "import alchemy"
SUBTEXT = f"Using: '{IMPORT_METHOD}' structure to access potions"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_distillation() -> None:
    print(f"{SUBTEXT}")
    print(f"Testing strength_potion: {alchemy.strength_potion()}")
    print(f"Testing heal alias: {alchemy.heal()}")


def main() -> None:
    banner()
    test_distillation()


if __name__ == "__main__":
    main()
