#! /usr/bin/env python3


def secure_archive(filename: str, mode: str = "r",
                   content: str = "") -> tuple[bool, str]:

    if mode not in ("r", "w"):
        return (False, f"Unknown mode '{mode}'"
                "Use 'r' to read or 'w' to write.")
    else:
        try:
            with open(filename, mode) as file:
                if mode == "r":
                    return (True, file.read())
                else:
                    file.write(content)
                    return (True, "Content successfully written to file")
        except OSError as error:
            return (False, str(error))


def main() -> None:
    print("=== Cyber Archives Security ===")
    print()
    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print()
    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/shadow"))
    print()
    print("Using 'secure_archive' to read from a regular file:")
    print(secure_archive("ancient_fragment.txt"))
    print()
    content = secure_archive("ancient_fragment.txt")
    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_vault.txt", "w", content[1]))


if __name__ == "__main__":
    main()
