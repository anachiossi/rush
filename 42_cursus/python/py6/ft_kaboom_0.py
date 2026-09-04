#! /usr/bin/env python3

import alchemy.grimoire as grim

EX_NAME = "Kaboom 0"
SUBTEXT = "Using grimoire module directly"
SPELL_NAME = "Fantasy"
INGREDIENTS = "Earth, wind and fire"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_kaboom() -> None:
    print(f"{SUBTEXT}")
    spell = grim.light_spellbook.light_spell_record(SPELL_NAME, INGREDIENTS)
    print(f"Testing record light spell: {spell}")


def main() -> None:
    banner()
    test_kaboom()


if __name__ == "__main__":
    main()
