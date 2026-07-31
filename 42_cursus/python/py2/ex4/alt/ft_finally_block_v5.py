#!/usr/bin/env python3
"""v5 - recovery instead of abort, and how to make a retry safe.

v1-v4 all answer the subject's question: an invalid name ends the
batch. This one asks the follow-up question a real system has to
answer - CAN the failure be repaired, and should we continue?

Both policies are correct in different places. Abort when continuing
risks corrupting data. Recover when the failure is local and
self-healing. What is never correct is not knowing which one you
chose.

--------------------------------------------------------------------
THE THREE OUTCOMES, and why they need three different messages

  "lettuce"   capitalize() changes it -> retry -> succeeds
              => repaired, batch continues

  "1234"      capitalize() changes NOTHING. Capitalization was never
              the problem, so a retry cannot possibly help.
              => "Auto-fix not applicable"  (I did not even try)

  "tomato1"   capitalize() DOES change it ("Tomato1"), so the fix
              looked applicable - but the retry hits the digit rule
              anyway.
              => "Auto-fix Capitalize failed"  (I tried, it failed)

The last two are different facts. Collapsing them into one message
throws away the distinction between "declined" and "attempted", which
is exactly what someone reading a log at 3am needs.

--------------------------------------------------------------------
WHAT MAKES THE RETRY SAFE - three separate decisions

1. THE GUARD (`if capitalized == plant_name`). Do not retry when the
   correction changes nothing. A retry that cannot help is just a
   slower failure - and against a network or a pump instead of a
   print(), it is a wasted round-trip on every malformed input.

2. THE RETRY CALLS water_plant(), NOT water_plant_fix(). Recursing
   into the fixer means an unfixable name retries forever. One
   attempt, then let the error out. Every retry loop needs a hard
   stop; this is the cheapest one that exists.

3. `raise ... from error`. Both failure paths raise a NEW error that
   names the recovery layer, chained to the original so the reason
   survives. Without `from`, str(e) would say only "auto-fix failed"
   and the caller would never learn WHY the name was invalid - and
   test_watering_system prints exactly str(e).

   raise X from err  -> __cause__ set, "direct cause of"      (intent)
   raise X           -> __context__ only, "during handling"   (accident)
   raise             -> re-throws the original, traceback intact

   The retry path produces a TWO-level chain: the failure of
   'Tomato1', and behind it the original failure of 'tomato1'. The
   whole story - what was tried, what it became, how each attempt
   died - is reconstructable.

--------------------------------------------------------------------
WHY water_plant HAS EXTRA RULES HERE

With only the subject's rule (raise iff name != name.capitalize()),
BOTH failure paths above are unreachable - not hard to hit, literally
impossible:

  - the guard asks `capitalized == plant_name`, the exact negation of
    the condition that made water_plant raise. Contradictory.
  - capitalize() is idempotent, so the retry can never fail.

Brute-forced over 200,000 random strings: 0 hits on either. Adding the
empty and letters-only rules makes both live (4,115 and 11,723 hits in
30,000 inputs).

The lesson is bigger than this file: the reachability of an error path
is a property of the CODE, not of your test data. You cannot test your
way into a branch that logic excludes. When a handler cannot be
triggered by any input, it is either deliberate future-proofing or it
is dead weight - and you should know which.

--------------------------------------------------------------------
AUTHORIZED-LIST NOTE

ex4 allows print() and str.capitalize() only. That is why the letters
check is a `for ... in` loop with `not in`, rather than .isalpha():
`in` and `not in` are OPERATORS, not function calls. .isalpha(),
.isdigit(), any() and len() would all be unauthorized.

Cost of ASCII LETTERS: "Cherry Tomato" (space) and "Éclair" (accent)
are rejected. The space case was ALREADY broken before the rule -
"cherry tomato".capitalize() gives "Cherry tomato", lowercasing the
second word. The rule only makes the failure loud instead of silent.

NOT FOR SUBMISSION: the extra rules and the whole auto-fix layer go
beyond the subject, which asks only for capitalization. Use v1-v4 to
submit; use this one to understand recovery.
"""

LETTERS = ("abcdefghijklmnopqrstuvwxyz"
           "ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


def water_plant(plant_name: str) -> None:
    if plant_name == "":
        raise PlantError("Invalid plant name to water: '' (empty)")
    for char in plant_name:
        if char not in LETTERS:
            raise PlantError(f"Invalid plant name to water: "
                             f"'{plant_name}' (bad character '{char}')")
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def water_plant_fix(plant_name: str) -> None:
    try:
        water_plant(plant_name)
    except PlantError as error:
        capitalized = plant_name.capitalize()
        if capitalized == plant_name:
            raise PlantError(
                f"Auto-fix not applicable to '{plant_name}': {error}"
            ) from error
        print(f"Auto-fixing name: {error}")
        print(f"Retrying with capitalized plant name: '{capitalized}'")
        try:
            water_plant(capitalized)
        except PlantError as retry_error:
            raise PlantError(
                f"Auto-fix Capitalize failed for '{plant_name}': "
                f"{retry_error}"
            ) from retry_error


def test_watering_system(plant_list: list[str],
                         use_fix: bool = False) -> None:
    print("Opening watering system")
    try:
        for plant in plant_list:
            if use_fix:
                water_plant_fix(plant)
            else:
                water_plant(plant)
    except PlantError as error:
        print(f"Caught {error.__class__.__name__}: {error}")
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===")
    print()
    print("Testing valid plants...")
    test_watering_system(["Tomato", "Lettuce", "Carrots"])
    print()
    print("Testing invalid plants...")
    test_watering_system(["Tomato", "lettuce", "Carrots"])
    print()
    print("Cleanup always happens, even with errors!")
    print()
    print("Auto-fix: name it CAN repair...")
    test_watering_system(["Tomato", "lettuce", "Carrots"], True)
    print()
    print("Auto-fix: fix not applicable (guard fires)...")
    test_watering_system(["Tomato", "1234"], True)
    print()
    print("Auto-fix: fix applied but retry still fails...")
    test_watering_system(["Tomato", "tomato1"], True)
