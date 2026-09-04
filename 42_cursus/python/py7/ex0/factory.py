"""The factory method pattern.

Concepts learned:
 A factory picks the concrete class, so callers only see the abstract type.
"""

from abc import ABC, abstractmethod

from .creature import Creature
from .creature import Charmander, Charmeleon, Charizard
from .creature import Squirtle, Wartortle, Blastoise
from .creature import Bulbasaur, Ivysaur, Venusaur


class CreatureFactory(ABC):

    @abstractmethod
    def create_base(self) -> Creature:
        pass

    @abstractmethod
    def create_evolved(self) -> Creature:
        pass

    @abstractmethod
    def create_final(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):

    def create_base(self) -> Creature:
        return Charmander()

    def create_evolved(self) -> Creature:
        return Charmeleon()

    def create_final(self) -> Creature:
        return Charizard()


class AquaFactory(CreatureFactory):

    def create_base(self) -> Creature:
        return Squirtle()

    def create_evolved(self) -> Creature:
        return Wartortle()

    def create_final(self) -> Creature:
        return Blastoise()


class FloraFactory(CreatureFactory):

    def create_base(self) -> Creature:
        return Bulbasaur()

    def create_evolved(self) -> Creature:
        return Ivysaur()

    def create_final(self) -> Creature:
        return Venusaur()
