#! /usr/bin/env python3

import sys


def read_archive(file_name: str) -> str | None:

    print(f"Accessing file '{file_name}'")
    f = None
    try:
        f = open(file_name, "r")
        content = f.read()
    except (OSError, UnicodeError) as e:
        print(f"Error opening file '{file_name}': {e}")
        return None
    else:
        print(f"---\n\n{content}\n---")
        return content
    finally:
        if f is not None:
            f.close()
            print(f"File '{file_name}' closed.")


def transform_data(content: str) -> str:

    print("\nTransform data:")
    converted = content.replace("\n", "#\n")
    print(f"---\n\n{converted}\n---")
    return (converted)


def write_archive(file_name: str, content: str) -> bool:

    new = None
    try:
        new = open(file_name, "w")
        new.write(content)
        return True
    except OSError as error:
        print(f"Error opening file '{file_name}': {error}")
        return False
    finally:
        if new is not None:
            new.close()


def main() -> None:

    print("=== Cyber Archives Recovery & Preservation ===")
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return
    file_name = sys.argv[1]
    content = read_archive(file_name)
    if content is None:
        return
    converted = transform_data(content)
    target = input("Enter new file name (or empty): ")
    if target == "":
        print("Not saving data.")
        return
    print(f"Saving data to '{target}'")
    if write_archive(target, converted):
        print(f"Data saved in file '{target}'.")
    else:
        print("Data not saved.")


if __name__ == "__main__":
    main()
