#!/usr/bin/env python3

import sys

EX_NAME = "Inventory System Analysis"

NEW_ITEM_NAME = "magic_item"
NEW_ITEM_QUANTITY = 1

COLOR = False
BOXES = False
ALIGNED = False


# color codes in ANSI escape sequences
Q = "\033[0m" if COLOR else ""          # reset
B = "\033[1m" if COLOR else ""          # bold
C = "\033[36m" if COLOR else ""         # cyan
R = "\033[31m" if COLOR else ""         # red
G = "\033[32m" if COLOR else ""         # green
Y = "\033[38;5;179m" if COLOR else ""   # yellow
M = "\033[35m" if COLOR else ""         # magenta
W = "\033[37m" if COLOR else ""         # white


# box drawing characters
AR = "→ " if BOXES else ""
TL = "╭" if BOXES else ""
TR = "╮" if BOXES else ""
BL = "╰" if BOXES else ""
BR = "╯" if BOXES else ""
VB = "│" if BOXES else ""
HB = "─" if BOXES else ""
WIDTH = 48 if BOXES else 0
NL = "\n" if BOXES else ""
EQ = "" if BOXES else "==="
TITLE = f"{EQ} {EX_NAME} {EQ}"

# label column alignment width
LW = 36 if ALIGNED else 0
VW = 0 if ALIGNED else 0


def banner() -> None:
    print(f"{C}{TL}{HB * WIDTH}{TR}{Q}", end=NL)
    print(f"{C}{VB}{Q}{B}{C}{TITLE:^{WIDTH}}{Q}{C}{VB}{Q}")
    print(f"{C}{BL}{HB * WIDTH}{BR}{Q}", end=NL)


def print_label(label: str, l_col: str, value: str, v_col: str) -> None:
    print(f"{l_col}{label:<{LW}}{Q}"
          f"{v_col}{value:>{VW}}{Q}")


def parse_inventory() -> dict[str, int]:
    inventory: dict[str, int] = {}
    for argv in sys.argv[1:]:
        try:
            thing, quantity_str = argv.split(":")
        except ValueError:
            label = "Error - invalid parameter "
            value = f"'{argv}'"
            print_label(label, R, value, Y)
            continue

        if thing in inventory:
            label = f"Redundant item '{thing}' - discarding"
            print_label(label, R, "", Y)
            continue

        try:
            quantity = int(quantity_str)
        except ValueError as error:
            label = f"Quantity error for '{thing}': "
            value = f"{error}"
            print_label(label, R, value, Y)
            continue
        inventory.update({thing: quantity})
    return inventory


def print_inventory(inventory: dict[str, int]) -> None:
    label = "Got inventory: "
    value = f"{inventory!s}"
    print_label(label, C, value, W)

    things_list = list(inventory.keys())
    label = "Item list: "
    print_label(label, C, f"{things_list!s}", W)

    total = sum(inventory.values())
    things_count = len(inventory)
    label = f"Total quantity of the {things_count} items: "
    print_label(label, C, f"{total!s}", W)


def print_percentages(inventory: dict[str, int]) -> None:
    total = sum(inventory.values())
    for thing in inventory:
        quantity = inventory[thing]
        percentage = round(quantity / total * 100, 1)
        label = f"Item {thing} represents "
        print_label(label, C, f"{percentage!s}%", W)


def print_abundance(inventory: dict[str, int]) -> None:
    if len(inventory) == 0:
        return

    most_name, most_quantity = "", 0
    least_name, least_quantity = "", 0
    seen = False
    for thing in inventory:
        quantity = inventory[thing]
        if not seen or quantity > most_quantity:
            most_name, most_quantity = thing, quantity
        if not seen or quantity < least_quantity:
            least_name, least_quantity = thing, quantity
        seen = True

    label = "Item most abundant: "
    value = f"{most_name} with quantity {most_quantity}"
    print_label(label, C, value, W)

    label = "Item least abundant: "
    value = f"{least_name} with quantity {least_quantity}"
    print_label(label, C, value, W)


def main() -> None:
    banner()
    inventory = parse_inventory()
    print_inventory(inventory)
    print_percentages(inventory)
    print_abundance(inventory)
    inventory.update({NEW_ITEM_NAME: NEW_ITEM_QUANTITY})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
