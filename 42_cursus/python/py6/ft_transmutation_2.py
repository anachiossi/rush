#! /usr/bin/env python3

import alchemy

EX_NAME = "Transmutation 2"
SUBTEXT = "Import alchemy module only"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_transmutation() -> None:
    print(f"{SUBTEXT}")
    gold = alchemy.lead_to_gold()
    print(f"Testing lead to gold: {gold}")


def main() -> None:
    banner()
    test_transmutation()


if __name__ == "__main__":
    main()
