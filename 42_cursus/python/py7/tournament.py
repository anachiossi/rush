#!/usr/bin/env python3

"""Composing the whole system.

Concepts learned:
 Combining factories, capabilities and strategies into one program.
 Handling domain errors at the level that can meaningfully respond to them.
"""

from ex0 import AquaFactory, CreatureFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (AggressiveStrategy, BattleError, BattleStrategy,
                 DefensiveStrategy, NormalStrategy)


def battle(
    opponents: list[tuple[CreatureFactory, BattleStrategy]],
) -> None:
    fighters = [(factory.create_base(), strategy)
                for factory, strategy in opponents]
    print("*** Tournament ***")
    print(f"{len(fighters)} opponents involved")
    try:
        for i, (left, left_strategy) in enumerate(fighters, start=1):
            for right, right_strategy in fighters[i:]:
                print()
                print("* Battle *")
                print(left.describe())
                print(" vs.")
                print(right.describe())
                print(" now fight!")
                for line in left_strategy.act(left):
                    print(line)
                for line in right_strategy.act(right):
                    print(line)
    except BattleError as error:
        print(f"Battle error, aborting tournament: {error}")


def main() -> None:
    flame = FlameFactory()
    aqua = AquaFactory()
    healing = HealingCreatureFactory()
    transform = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(flame, normal), (healing, defensive)])
    print()
    print("Tournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(flame, aggressive), (healing, defensive)])
    print()
    print("Tournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive), "
          "(Transform+Aggressive) ]")
    battle([(aqua, normal), (healing, defensive),
            (transform, aggressive)])


if __name__ == "__main__":
    main()
