#!/usr/bin/env python3


def garden_operations(operation_id: int) -> None:

    match operation_id:
        case 0:
            int("abc")
        case 1:
            42 / 0
        case 2:
            open("/non/existent/file")
        case 3:
            "Ana" + 42  # type: ignore[operator]
        case _:
            return


def test_error_types() -> None:

    print("=== Garden Error Types Demo ===")
    for operation_id in range(5):
        print(f"Testing operation {operation_id}...")

        try:
            garden_operations(operation_id)
            print("Operation completed successfully")

        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as error:
            print(f"Caught {error.__class__.__name__}: {error}")

    print()
    print("All error types tested successfully!")


if __name__ == "__main__":

    test_error_types()
