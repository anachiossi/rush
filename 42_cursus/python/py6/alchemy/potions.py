
from . import elements as earth_air_elements
import elements as fire_water_elements


def healing_potion() -> str:
    earth = earth_air_elements.create_earth()
    air = earth_air_elements.create_air()
    return f"Healing potion brewed with '{earth}' and '{air}'"


def strength_potion() -> str:
    fire = fire_water_elements.create_fire()
    water = fire_water_elements.create_water()
    return f"Strength potion brewed with '{fire}' and '{water}'"
