"""A domain-specific exception.

Concepts learned:
 A custom Exception subclass naming a failure in this domain's terms.
 Why a named error beats a generic one for callers deciding what to catch.
"""


class BattleError(Exception):

    def __init__(self, name: str, label: str) -> None:
        self.name = name
        self.label = label
        super().__init__(f"'{name}' can't use {label} strategy")
