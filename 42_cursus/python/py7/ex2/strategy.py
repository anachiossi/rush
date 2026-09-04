"""The strategy pattern.

Concepts learned:
 Interchangeable algorithms behind one interface, selected at runtime.
 isinstance checks against capability interfaces to decide what an actor may
 do.
"""

from abc import ABC, abstractmethod

from ex0 import Creature
from ex1 import HealCapability, TransformCapability

from .errors import BattleError


class BattleStrategy(ABC):

    label: str

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        pass


class NormalStrategy(BattleStrategy):

    label = "normal"

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):

    label = "aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, TransformCapability):
            raise BattleError(creature.name, self.label)
        return [creature.transform(), creature.attack(),
                creature.revert()]


class DefensiveStrategy(BattleStrategy):

    label = "defensive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, HealCapability):
            raise BattleError(creature.name, self.label)
        return [creature.attack(), creature.heal()]
