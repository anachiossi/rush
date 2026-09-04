#!/usr/bin/env python3

"""Protocols and structural typing.
 Concepts learned:
 typing.Protocol for duck typing that a type checker can verify.
 Structural typing - shape decides compatibility - versus nominal
 inheritance.
"""

from typing import Protocol
from ex1 import HealingCreatureFactory, TransformCreatureFactory

HEAL_BANNER = "Testing Creature with healing capability"
TRANSFORM_BANNER = "Testing Creature with transform capability"
BASE_LABEL = " base:"
EVOLVED_LABEL = " evolved:"


def banner(title: str) -> None:
    print(f"{title}")


class Healer(Protocol):

    def describe(self) -> str: ...

    def attack(self) -> str: ...

    def heal(self) -> str: ...


class Transformer(Protocol):

    def describe(self) -> str: ...

    def attack(self) -> str: ...

    def transform(self) -> str: ...

    def revert(self) -> str: ...


def show_healer(creature: Healer) -> None:
    print(f"{creature.describe()}")
    print(f"{creature.attack()}")
    print(f"{creature.heal()}")


def show_transformer(creature: Transformer) -> None:
    print(f"{creature.describe()}")
    print(f"{creature.attack()}")
    print(f"{creature.transform()}")
    print(f"{creature.attack()}")
    print(f"{creature.revert()}")


def test_healing() -> None:
    banner(HEAL_BANNER)
    factory = HealingCreatureFactory()
    print(f"{BASE_LABEL}")
    show_healer(factory.create_base())
    print(f"{EVOLVED_LABEL}")
    show_healer(factory.create_evolved())


def test_transform() -> None:
    banner(TRANSFORM_BANNER)
    factory = TransformCreatureFactory()
    print(f"{BASE_LABEL}")
    show_transformer(factory.create_base())
    print(f"{EVOLVED_LABEL}")
    show_transformer(factory.create_evolved())


def main() -> None:
    test_healing()
    print()
    test_transform()


if __name__ == "__main__":
    main()
