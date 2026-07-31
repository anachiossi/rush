#!/usr/bin/env python3


class GardenError(Exception):

    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def force_plant_error() -> None:
    raise PlantError("The tomato plant is wilting!")


def force_water_error() -> None:
    raise WaterError("Not enough water in the tank!")


def test_garden_errors() -> None:

    print("=== Custom Garden Errors Demo ===")
    print()

    print("Testing PlantError...")
    try:
        force_plant_error()
    except PlantError as error:
        print(f"Caught PlantError: {error}")
    print()

    print("Testing WaterError...")
    try:
        force_water_error()
    except WaterError as error:
        print(f"Caught WaterError: {error}")
    print()

    print("Testing catching all garden errors...")
    for function_error in (force_plant_error, force_water_error):
        try:
            function_error()
        except GardenError as error:
            print(f"Caught GardenError: {error}")

    print()
    print("All custom error types work correctly!")


if __name__ == "__main__":

    test_garden_errors()
