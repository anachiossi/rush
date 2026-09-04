
from .dark_spellbook import dark_spell_allowed_ingredients as dark


def validate_ingredients(ingredients: str) -> str:
    ingredients = ingredients.lower()
    allowed = dark()
    for ingredient in allowed:
        if ingredient in ingredients:
            return "VALID"
    return "INVALID"
