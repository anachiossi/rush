#! /usr/bin/env python3

import alchemy.transmutation.recipes as atr

EX_NAME = "Transmutation 0"
SUBTEXT = "Using file alchemy/transmutation/recipes.py directly"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_transmutation() -> None:
    print(f"{SUBTEXT}")
    gold = atr.lead_to_gold()
    print(f"Testing lead to gold: {gold}")


def main() -> None:
    banner()
    test_transmutation()


if __name__ == "__main__":
    main()
