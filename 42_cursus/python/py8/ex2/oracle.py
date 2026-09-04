#! /usr/bin/env python3

"""Environment and dependency management.

Concepts learned:
 Reading configuration from environment variables instead of hardcoding it.
 Keeping secrets out of source, and providing safe defaults when a variable
 is unset.
"""

import os
import sys

try:
    from dotenv import dotenv_values, load_dotenv
except ImportError:
    print("python-dotenv not installed. Run: pip install -r requirements.txt")
    raise SystemExit(1)


CONFIG_KEYS: tuple[str, ...] = (
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)

DEFAULTS: dict[str, str] = {
    "MATRIX_MODE": "development",
    "LOG_LEVEL": "DEBUG",
}

SECRET_KEYS: tuple[str, ...] = ("DATABASE_URL", "API_KEY")
PRODUCTION_KEYS: tuple[str, ...] = (
    "DATABASE_URL",
    "API_KEY",
    "ZION_ENDPOINT",
)

ENV_FILE: str = ".env"

COLOR: bool = sys.stdout.isatty() and not sys.platform.startswith("win")

G: str = "\033[32m" if COLOR else ""
R: str = "\033[31m" if COLOR else ""
Q: str = "\033[0m" if COLOR else ""


def load_config() -> dict[str, str]:
    load_dotenv()

    config: dict[str, str] = {}
    for key in CONFIG_KEYS:
        config[key] = os.environ.get(key, DEFAULTS.get(key, ""))
    return config


def report(config: dict[str, str]) -> None:
    production: bool = config["MATRIX_MODE"] == "production"

    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {'Connected' if config['DATABASE_URL'] else 'Offline'}")
    api: str = "Authenticated" if config["API_KEY"] else "Anonymous"
    zion: str = "Online" if config["ZION_ENDPOINT"] else "Offline"
    print(f"API Access: {api}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {zion}")
    if production:
        print("Policy: every key is required, missing ones abort the run")
    else:
        print("Policy: missing keys are tolerated and reported below")


def hardcoded_secrets(config: dict[str, str]) -> list[str]:
    try:
        with open(__file__, encoding="utf-8") as handle:
            source: str = handle.read()
    except OSError:
        return []
    return [
        key for key in SECRET_KEYS
        if config[key] and config[key] in source
    ]


def security_check(config: dict[str, str]) -> None:
    file_values: dict[str, str | None] = dotenv_values(ENV_FILE)
    overridden: list[str] = [
        key for key, value in file_values.items()
        if key in os.environ and os.environ[key] != value
    ]

    exposed: list[str] = hardcoded_secrets(config)

    print("Environment security check:")
    if exposed:
        print(f"{R}[FAIL]{Q} secrets written in the source: {exposed}")
    else:
        print(f"{G}[OK]{Q} No hardcoded secrets detected")
    if file_values:
        print(f"{G}[OK]{Q} {ENV_FILE} file properly configured")
    else:
        print(f"{R}[FAIL]{Q} no {ENV_FILE} file found")
    print(f"{G}[OK]{Q} Production overrides available "
          f"({len(overridden)} in effect)")

    for key in CONFIG_KEYS:
        if not config[key]:
            print(f"{R}[MISSING]{Q} {key}")


def main() -> int:
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    config: dict[str, str] = load_config()

    absent: list[str] = [key for key in PRODUCTION_KEYS if not config[key]]
    if config["MATRIX_MODE"] == "production" and absent:
        print(f"{R}[FAIL]{Q} production requires: {', '.join(absent)}")
        return 0

    report(config)
    print()
    security_check(config)
    print()
    print("The Oracle sees all configurations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
