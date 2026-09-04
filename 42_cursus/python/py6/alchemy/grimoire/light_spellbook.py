

def light_spell_allowed_ingredients() -> list[str]:
    light = ["earth", "air", "fire", "water"]
    return light


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from .light_validator import validate_ingredients as validate
    result = validate(ingredients)
    return f"Spell recorded: {spell_name} ({ingredients} - {result})"
