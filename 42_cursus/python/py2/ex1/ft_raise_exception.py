#!/usr/bin/env python3

MIN_TEMP = 0
MAX_TEMP = 40


def check_range(temp: int) -> None:

    if temp < MIN_TEMP:
        raise ValueError(f"{temp}°C is too cold for plants (min {MIN_TEMP}°C)")
    if temp > MAX_TEMP:
        raise ValueError(f"{temp}°C is too hot for plants (max {MAX_TEMP}°C)")


def input_temperature(temp_str: str) -> int:

    temp = int(temp_str)
    check_range(temp)
    return temp


def test_temperature() -> None:

    print("=== Garden Temperature Checker ===")

    test_values = ["25", "abc", "100", "-50"]
    for value in test_values:
        print()
        print(f"Input data is '{value}'")
        try:
            result = input_temperature(value)
            print(f"Temperature is now {result}°C")
        except ValueError as error:
            print(f"Caught input_temperature error: {error}")
    print()
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
