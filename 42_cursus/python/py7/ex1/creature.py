"""Multiple inheritance from capabilities.

Concepts learned:
 Inheriting from a base class and one or more capability interfaces.
"""

from ex0 import Creature
from .capability import HealCapability, TransformCapability


class Cottonee(Creature, HealCapability):

    NAME: str = "Cottonee"
    KIND: list[str] = ["Grass", "Fairy"]
    ATTACK: list[str] = ["Vine Whip"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"

    def heal(self) -> str:
        return f"{self.name} heals itself for a small amount"


class Whimsicott(Creature, HealCapability):

    NAME: str = "Whimsicott"
    KIND: list[str] = ["Grass", "Fairy"]
    ATTACK: list[str] = ["Petal Dance"]

    def attack(self) -> str:
        return f"{self.name} uses {self.attack_list[0]}!"

    def heal(self) -> str:
        return f"{self.name} heals itself and others for a large amount"


class Ditto(Creature, TransformCapability):

    NAME: str = "Ditto"
    KIND: list[str] = ["Normal"]
    ATTACK: list[str] = ["Transform"]

    def attack(self) -> str:
        if self.boosted:
            return f"{self.name} uses a boosted {self.attack_list[0]}!"
        return f"{self.name} uses {self.attack_list[0]}!"

    def transform(self) -> str:
        self.boosted = True
        return f"{self.name} transforms into a copy of its opponent!"

    def revert(self) -> str:
        self.boosted = False
        return f"{self.name} reverts to its original form!"


class MegaDitto(Creature, TransformCapability):

    NAME: str = "Mega Ditto"
    KIND: list[str] = ["Normal"]
    ATTACK: list[str] = ["Mega Transform"]

    def attack(self) -> str:
        if self.boosted:
            return f"{self.name} uses a boosted {self.attack_list[0]}!"
        return f"{self.name} uses {self.attack_list[0]}!"

    def transform(self) -> str:
        self.boosted = True
        return f"{self.name} transforms into a mega copy of its opponent!"

    def revert(self) -> str:
        self.boosted = False
        return f"{self.name} reverts to its original form!"
