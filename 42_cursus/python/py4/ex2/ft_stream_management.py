#! /usr/bin/env python3

import sys


def read_archive(file_name: str) -> str | None:

    print(f"Accessing file '{file_name}'")
    f = None
    try:
        f = open(file_name, "r")
        content = f.read()
    except (OSError, UnicodeError) as e:
        print(f"[STDERR] Error opening file "
              f"'{file_name}': {e}", file=sys.stderr)
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
    return converted


def write_archive(file_name: str, content: str) -> bool:

    new = None
    try:
        new = open(file_name, "w")
        new.write(content)
        return True
    except OSError as error:
        print(f"[STDERR] Error opening file "
              f"'{file_name}': {error}", file=sys.stderr)
        return False
    finally:
        if new is not None:
            new.close()


def get_target() -> str | None:

    print("Enter new file name (or empty): ", end="")
    sys.stdout.flush()
    target = sys.stdin.readline()
    if target == "":
        return None
    target = target.rstrip("\n")
    return target


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
    target = get_target()
    if target is None:
        print("Not saving data.")
        return
    else:
        print(f"Saving data to '{target}'")
    if write_archive(target, converted):
        print(f"Data saved in file '{target}'.")
    else:
        print("Data not saved.")


if __name__ == "__main__":
    main()
