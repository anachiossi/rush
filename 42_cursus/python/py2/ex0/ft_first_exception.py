#!/usr/bin/env python3


def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:

    print("=== Garden Temperature ===")

    test_values = ["25", "abc"]
    for value in test_values:
        print()
        print(f"Input data is '{value}'")
        try:
            result = input_temperature(value)
        except ValueError as error:
            print(f"Caught input_temperature error: {error}")
        else:
            print(f"Temperature is now {result}°C")

    print()
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
