"""Factories for capability-bearing types.

Concepts learned:
 Extending a factory hierarchy without changing existing factories.
 The open/closed idea: add a subclass rather than edit a working one.
"""

from ex0 import CreatureFactory
from .creature import Cottonee, Whimsicott, Ditto, MegaDitto


class HealingCreatureFactory(CreatureFactory):

    def create_base(self) -> Cottonee:
        return Cottonee()

    def create_evolved(self) -> Whimsicott:
        return Whimsicott()

    def create_final(self) -> Whimsicott:
        return Whimsicott()


class TransformCreatureFactory(CreatureFactory):

    def create_base(self) -> Ditto:
        return Ditto()

    def create_evolved(self) -> MegaDitto:
        return MegaDitto()

    def create_final(self) -> MegaDitto:
        return MegaDitto()
