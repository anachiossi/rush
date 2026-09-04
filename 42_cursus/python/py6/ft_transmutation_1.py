#! /usr/bin/env python3

import alchemy.transmutation as trans

EX_NAME = "Transmutation 1"
SUBTEXT = "Import transmutation module directly"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_transmutation() -> None:
    print(f"{SUBTEXT}")
    gold = trans.lead_to_gold()
    print(f"Testing lead to gold: {gold}")


def main() -> None:
    banner()
    test_transmutation()


if __name__ == "__main__":
    main()
