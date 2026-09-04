#! /usr/bin/env python3

EX_NAME = "Kaboom 1"
SUBTEXT = "Access to alchemy/grimoire/dark_spellbook.py directly"
SPELL_NAME = "Necromancy"
INGREDIENTS = "bats and frogs"


def banner() -> None:
    print(f"=== {EX_NAME} ===")


def test_kaboom() -> None:
    print(f"{SUBTEXT}")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    import alchemy.grimoire.dark_spellbook as darkspell
    spell = darkspell.dark_spell_record(SPELL_NAME, INGREDIENTS)
    print(f"Testing record dark spell: {spell}")


def main() -> None:
    banner()
    test_kaboom()


if __name__ == "__main__":
    main()
