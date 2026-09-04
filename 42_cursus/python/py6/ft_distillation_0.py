#! /usr/bin/env python3

from alchemy import potions

EX_NAME = "Distillation 0"
SUBTEXT = "Direct access to alchemy/potions.py"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_distillation() -> None:
    print(f"{SUBTEXT}")
    print(f"Testing strength_potion: {potions.strength_potion()}")
    print(f"Testing healing_potion: {potions.healing_potion()}")


def main() -> None:
    banner()
    test_distillation()


if __name__ == "__main__":
    main()
