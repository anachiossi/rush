"""Capability interfaces.

Concepts learned:
 Small abstract classes describing one ability that can serve multiple classes.
 Interface segregation and flexibility.
"""

from abc import ABC, abstractmethod


class HealCapability(ABC):

    @abstractmethod
    def heal(self) -> str:
        pass


class TransformCapability(ABC):

    boosted: bool = False

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass
