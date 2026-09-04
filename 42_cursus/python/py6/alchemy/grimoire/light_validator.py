
def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients as light
    ingredients = ingredients.lower()
    allowed = light()
    for ingredient in allowed:
        if ingredient in ingredients:
            return "VALID"
    return "INVALID"
