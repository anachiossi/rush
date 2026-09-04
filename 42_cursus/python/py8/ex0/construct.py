#! /usr/bin/env python3

"""Environment and dependency management.

Concepts learned:
 Virtual environments to isolate a project's dependencies from the system
 Python.
 Declaring and pinning third-party packages so an environment is
 reproducible.
"""

import os
import site
import sys

COLOR: bool = sys.stdout.isatty() and not sys.platform.startswith("win")

G: str = "\033[32m" if COLOR else ""
R: str = "\033[31m" if COLOR else ""
Y: str = "\033[38;5;220m" if COLOR else ""
Q: str = "\033[0m" if COLOR else ""

env_info: dict[str, str | bool] = {
    "current_root": sys.prefix,
    "system_root": sys.base_prefix,
    "python_executable": sys.executable,
    "is_venv": sys.prefix != sys.base_prefix,
    "venv_name": os.path.basename(sys.prefix),
}


def matrix_status() -> None:
    msg_true: str = "MATRIX STATUS: Welcome to the construct"
    msg_false: str = "MATRIX STATUS: You're still plugged in"
    if env_info["is_venv"]:
        print(msg_true)
    else:
        print(msg_false)


def python_info() -> None:
    print(f"Current Python: {env_info['python_executable']}")


def venv_info() -> None:
    msg_none: str = "Virtual Environment: None detected"
    if env_info["is_venv"]:
        print(f"Virtual Environment: {env_info['venv_name']}")
        print(f"Environment Path: {env_info['current_root']}")
    else:
        print(msg_none)


def activation_instructions() -> None:
    msg_warning: str = f"{R}WARNING:{Q} You're in the global environment!\n" \
                       "The machines can see everything you install."

    msg_instructions: str = (
        "To enter the construct, run:\n"
        f"{Y}python -m venv matrix_env{Q}\n"
        f"{Y}source matrix_env/bin/activate{Q} # On Unix\n"
        f"{Y}matrix_env\\Scripts\\activate{Q} # On Windows\n"
        "\nThen run this program again."
    )

    print(msg_warning)
    print()
    print(msg_instructions)


def site_packages_for(prefix: str) -> str | None:
    if not hasattr(site, "getsitepackages"):
        return None
    for path in site.getsitepackages([prefix]):
        if os.path.isdir(path):
            return path
    return None


def packages_instructions() -> None:
    msg_invenv: str = f"{G}SUCCESS:{Q} You're in an isolated environment!\n" \
                      "Safe to install packages without affecting\n" \
                      "the global system."

    msg_error: str = "Unable to locate site-packages directory.\n" \
                     "Your virtual environment may be corrupted\n" \
                     "or not standard, try recreating it with:\n" \
                     "python -m venv matrix_env"

    msg_success: str = "Package installation path:"

    current: str = str(env_info["current_root"])
    site_packages: str | None = site_packages_for(current)

    print(msg_invenv)
    print()
    if site_packages:
        print(msg_success)
        print(site_packages)
    else:
        print(msg_error)


def packages_comparison() -> None:
    msg_header: str = "Package locations:"
    msg_unknown: str = "not found"
    msg_novenv: str = "none - no virtual environment active"

    system: str = str(env_info["system_root"])
    global_packages: str | None = site_packages_for(system)

    print(msg_header)
    print(f"Global: {global_packages or msg_unknown}")
    if env_info["is_venv"]:
        current: str = str(env_info["current_root"])
        venv_packages: str | None = site_packages_for(current)
        print(f"Virtual environment: {venv_packages or msg_unknown}")
    else:
        print(f"Virtual environment: {msg_novenv}")


def main() -> None:
    print()
    matrix_status()
    print()
    python_info()
    venv_info()
    print()
    if not env_info["is_venv"]:
        activation_instructions()
    else:
        packages_instructions()
    print()
    packages_comparison()


if __name__ == "__main__":
    main()
