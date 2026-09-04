from alchemy.potions import strength_potion as sp
from ..elements import create_air as ca
import elements


def lead_to_gold() -> str:
    air = ca()
    fire = elements.create_fire()
    strength = sp()
    return (
        f"Recipe transmuting Lead to Gold: brew '{air}' "
        f"and '{strength}' mixed with '{fire}'"
    )
