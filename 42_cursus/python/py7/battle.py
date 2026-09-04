#!/usr/bin/env python3

"""Exercising the factories.

Concepts learned:
 Calling a factory hierarchy through its abstract type only.
 Verifying that each concrete factory honours the shared contract.
"""

from ex0 import AquaFactory, CreatureFactory, FlameFactory, FloraFactory

FACTORY_BANNER = "Testing factory"
BATTLE_BANNER = "Testing battle"
VS_LABEL = " vs."
FIGHT_LABEL = " fight!"


def banner(title: str) -> None:
    print(f"{title}")


def test_factory(factory: CreatureFactory) -> None:
    banner(FACTORY_BANNER)
    primary = factory.create_base()
    print(f"{primary.describe()}")
    print(f"{primary.attack()}")
    evolved = factory.create_evolved()
    print(f"{evolved.describe()}")
    print(f"{evolved.attack()}")


def test_battle(my_factory: CreatureFactory,
                wild_factory: CreatureFactory) -> None:
    banner(BATTLE_BANNER)
    my_creature = my_factory.create_base()
    wild_creature = wild_factory.create_base()
    print(f"{my_creature.describe()}")
    print(f"{VS_LABEL}")
    print(f"{wild_creature.describe()}")
    print(f"{FIGHT_LABEL}")
    print(f"{my_creature.attack()}")
    print(f"{wild_creature.attack()}")


def main() -> None:
    test_factory(FlameFactory())
    print()
    test_factory(AquaFactory())
    print()
    test_factory(FloraFactory())
    print()
    test_battle(FlameFactory(), AquaFactory())
    print()
    test_battle(AquaFactory(), FloraFactory())


if __name__ == "__main__":
    main()
