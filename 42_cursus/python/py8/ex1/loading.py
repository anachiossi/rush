#! /usr/bin/env python3

"""Environment and dependency management.

Concepts learned:
 Installing and importing third-party packages inside an isolated
 environment.
 Verifying that a dependency resolves to the expected version at runtime.
"""

from __future__ import annotations

import importlib
import importlib.metadata
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas

# Packages required for the program to run
REQUIRED: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "requests": "Network access ready",
    "matplotlib": "Visualization ready",
}

# Example data for testing purposes: Pokemon base stats
API_URL: str = "https://pokeapi.co/api/v2/pokemon"
CACHE_FILE: str = "pokedex.csv"
BASE_STATS: tuple[str, ...] = (
    "hp", "attack", "defense",
    "special-attack", "special-defense", "speed",
)
COLUMNS: tuple[str, ...] = ("id",) + BASE_STATS
MAX_RECORD_ID: int = 10000

# Identify OS for installation instructions
POETRY_UNIX: str = "curl -sSL https://install.python-poetry.org | python3 -"
POETRY_WINDOWS: str = (
    "(Invoke-WebRequest -Uri https://install.python-poetry.org "
    "-UseBasicParsing).Content | py -"
)

WINDOWS: bool = sys.platform.startswith("win")
PYTHON_CMD: str = "python" if WINDOWS else "python3"
POETRY_INSTALLER: str = POETRY_WINDOWS if WINDOWS else POETRY_UNIX
ACTIVATE: str = (
    "matrix_env\\Scripts\\activate" if WINDOWS
    else "source matrix_env/bin/activate"
)

# Color codes for terminal output
COLOR: bool = sys.stdout.isatty() and not sys.platform.startswith("win")

G: str = "\033[32m" if COLOR else ""        # Green for successful packages
R: str = "\033[31m" if COLOR else ""        # Red for missing packages
Y: str = "\033[38;5;220m" if COLOR else ""  # Yellow for command lines
Q: str = "\033[0m" if COLOR else ""         # Quit color formatting

# Output file configuration
OUTPUT_FILE: str = "matrix_analysis.png"


def check_dependencies() -> dict[str, str | None]:
    status: dict[str, str | None] = {}

    for package in REQUIRED:
        try:
            status[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            status[package] = None
    return status


def report_dependencies(status: dict[str, str | None]) -> None:
    print("Checking dependencies:")
    for package, version in status.items():
        if version is None:
            print(f"{R}[MISSING]{Q} {package} - not installed")
        else:
            print(f"{G}[OK]{Q} {package} ({version}) - {REQUIRED[package]}")


def installed_with(package: str) -> str:
    distribution = importlib.metadata.distribution(package)
    installer = distribution.read_text("INSTALLER")
    return installer.strip() if installer else "unknown"


def compare_pip_and_poetry(status: dict[str, str | None]) -> None:
    installed: int = len(list(importlib.metadata.distributions()))
    rows: str = "\n".join(
        f"{package:<12} {version:<10} {installed_with(package)}"
        for package, version in status.items()
    )

    print(
        "Comparing pip and Poetry:\n"
        f"Interpreter: {sys.executable}\n\n"
        f"{'package':<12} {'version':<10} installed by\n"
        f"{rows}\n\n"
        f"Declared: {len(REQUIRED)}    Installed here: {installed}\n"
    )
    print(
        "Run it both ways to compare:\n\n"
        "Pip flow:\n"
        f"{Y}{PYTHON_CMD} -m venv matrix_env{Q}\n"
        f"{Y}{ACTIVATE}{Q}\n"
        f"{Y}pip install -r requirements.txt{Q}\n"
        f"{Y}{PYTHON_CMD} loading.py{Q}\n\n"
        "Poetry flow:\n"
        f"{Y}deactivate{Q}\n"
        f"{Y}poetry install{Q}\n"
        f"{Y}poetry run python loading.py{Q}"
    )


def install_instructions() -> None:

    msg_header: str = "Programs not loaded. Install them with pip:"
    run_pip: str = f"{PYTHON_CMD} loading.py"
    msg_pip: str = (
        f"{Y}{'pip install -r requirements.txt':<32}{Q}(once)\n"
        f"{Y}{run_pip:<32}{Q}(every run)"
    )
    msg_why_pip: str = (
        "Why pip: it ships with Python, nothing else to install."
    )
    msg_or: str = "or with Poetry:"
    msg_why_poetry: str = (
        "Why Poetry: it locks exact versions and manages the venv for you."
    )
    msg_poetry: str = (
        f"{Y}{'poetry install':<32}{Q}(once)\n"
        f"{Y}{'poetry run python loading.py':<32}{Q}(every run)"
    )
    msg_no_pip: str = (
        "No pip? Restore it with:\n"
        f"{Y}{PYTHON_CMD} -m ensurepip --upgrade{Q}"
    )
    msg_no_poetry: str = (
        "No Poetry? Install it outside your virtual environment:\n"
        f"{Y}deactivate{Q} (to exit the virtual environment)\n"
        f"{Y}pipx install poetry{Q}\n"
        f"or: {Y}{POETRY_INSTALLER}{Q}\n"
    )

    print(msg_header)
    print(msg_why_pip)
    print(msg_pip)
    print()
    print(msg_or)
    print(msg_why_poetry)
    print(msg_poetry)
    print()
    print(msg_no_pip)
    print()
    print(msg_no_poetry)


def internet_available() -> bool:
    import requests

    try:
        requests.head(API_URL, timeout=3)
    except requests.RequestException:
        return False
    return True


def filter_index(entries: list[dict[str, str]]) -> list[dict[str, str]]:
    kept: list[dict[str, str]] = []
    for entry in entries:
        number = int(entry["url"].rstrip("/").split("/")[-1])
        if number < MAX_RECORD_ID:
            kept.append(entry)
    return kept


def fetch_data() -> dict[str, dict[str, int]]:
    import requests

    records: dict[str, dict[str, int]] = {}
    try:
        index = requests.get(f"{API_URL}?limit=100000", timeout=10)
        index.raise_for_status()
        entries = filter_index(index.json()["results"])
    except (requests.RequestException, KeyError, ValueError):
        return records

    total: int = len(entries)
    for number, entry in enumerate(entries, start=1):
        try:
            response = requests.get(entry["url"], timeout=5)
            response.raise_for_status()
            payload = response.json()
            raw = payload["stats"]
            stats = {s["stat"]["name"]: s["base_stat"] for s in raw}
            row: dict[str, int] = {"id": int(payload["id"])}
            row.update({n: int(stats[n]) for n in BASE_STATS})
            records[payload["name"]] = row
        except (requests.RequestException, KeyError, ValueError):
            continue
        print(f"\rFetching data: {number}/{total}", end="")
    print()
    return records


def load_data() -> dict[str, dict[str, int]]:
    import pandas

    try:
        frame = pandas.read_csv(CACHE_FILE, index_col="name")
        rows = frame.to_dict("index")
        return {
            str(name): {column: int(row[column]) for column in COLUMNS}
            for name, row in rows.items()
        }
    except (OSError, ValueError, KeyError):
        pass

    if not internet_available():
        return {}

    records: dict[str, dict[str, int]] = fetch_data()
    if records:
        frame = pandas.DataFrame.from_dict(records, orient="index")
        frame.to_csv(CACHE_FILE, index_label="name")
    return records


def analyze_data(dataset: dict[str, dict[str, int]]) -> pandas.DataFrame:
    import numpy
    import pandas

    frame = pandas.DataFrame.from_dict(dataset, orient="index")
    frame.index.name = "name"
    stats = frame[list(BASE_STATS)].to_numpy()
    frame["total"] = numpy.sum(stats, axis=1)
    order = numpy.argsort(frame["total"].to_numpy())[::-1]
    return frame.iloc[order]


def report_analysis(frame: pandas.DataFrame) -> None:
    import numpy

    totals = frame["total"].to_numpy()
    print(f"Strongest: {frame.index[0]} ({totals[0]})")
    print(f"Weakest: {frame.index[-1]} ({totals[-1]})")
    print(f"Average total: {numpy.mean(totals):.1f}")
    print(f"Median total: {numpy.median(totals):.1f}")


def visualize(frame: pandas.DataFrame, path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot

    figure, axes = matplotlib.pyplot.subplots(figsize=(10, 6))
    axes.hist(frame["total"].to_numpy(), bins=40, color="#2e7d32")
    axes.set_title(f"Base stat totals of {len(frame)} species")
    axes.set_xlabel("base stat total")
    axes.set_ylabel("species")

    figure.tight_layout()
    figure.savefig(path, dpi=120)
    matplotlib.pyplot.close(figure)


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    status: dict[str, str | None] = check_dependencies()
    report_dependencies(status)
    if None in status.values():
        print()
        install_instructions()
        return

    print()
    compare_pip_and_poetry(status)

    print()
    dataset: dict[str, dict[str, int]] = load_data()
    if not dataset:
        print()
        print("No Matrix data: no local cache and no network.")
        print("Connect to the network and run this program again.")
        return

    print()
    print("Analyzing Matrix data...")
    print(f"Processing {len(dataset)} data points...")
    frame = analyze_data(dataset)
    print()
    report_analysis(frame)
    print()
    print("Generating visualization...")
    visualize(frame, OUTPUT_FILE)
    print()
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
