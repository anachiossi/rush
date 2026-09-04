"""Abstract base class and concrete subclasses.

Concepts learned:
 ABC and @abstractmethod to define what every creature must have.
 Subclasses supplying their own behaviour.
"""

from abc import ABC, abstractmethod


class Creature(ABC):

    NAME: str
    KIND: list[str]
    ATTACK: list[str]

    def __init__(self) -> None:
        self.name = self.NAME
        self.kind_list = self.KIND
        self.attack_list = self.ATTACK

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return (f"{self.name} is a {'/'.join(self.kind_list)}"
                f" type Creature")


class Charmander(Creature):

    NAME: str = "Charmander"
    KIND: list[str] = ["Fire"]
    ATTACK: list[str] = ["Ember"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"


class Charmeleon(Creature):

    NAME: str = "Charmeleon"
    KIND: list[str] = ["Fire"]
    ATTACK: list[str] = ["Flamethrower"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"


class Charizard(Creature):

    NAME: str = "Charizard"
    KIND: list[str] = ["Fire", "Flying"]
    ATTACK: list[str] = ["Fire Blast"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"


class Squirtle(Creature):

    NAME: str = "Squirtle"
    KIND: list[str] = ["Water"]
    ATTACK: list[str] = ["Water Gun"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"


class Wartortle(Creature):

    NAME: str = "Wartortle"
    KIND: list[str] = ["Water"]
    ATTACK: list[str] = ["Water Pulse"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"


class Blastoise(Creature):

    NAME: str = "Blastoise"
    KIND: list[str] = ["Water"]
    ATTACK: list[str] = ["Hydro Pump"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"


class Bulbasaur(Creature):

    NAME: str = "Bulbasaur"
    KIND: list[str] = ["Grass", "Poison"]
    ATTACK: list[str] = ["Vine Whip"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"


class Ivysaur(Creature):

    NAME: str = "Ivysaur"
    KIND: list[str] = ["Grass", "Poison"]
    ATTACK: list[str] = ["Razor Leaf"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"


class Venusaur(Creature):

    NAME: str = "Venusaur"
    KIND: list[str] = ["Grass", "Poison"]
    ATTACK: list[str] = ["Solar Beam"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"
