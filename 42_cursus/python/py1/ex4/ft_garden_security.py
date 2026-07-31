#!/usr/bin/env python3


class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name: str = name
        self._height: float = 0.0
        self._age: int = 0
        self.set_height(height)
        self.set_age(age)

    def get_height(self) -> float:
        return self._height

    def set_height(self, value: float) -> bool:
        if value < 0:
            print(f"{self._name}: Error, height can't be negative")
            return False
        self._height = value
        return True

    def get_age(self) -> int:
        return self._age

    def set_age(self, value: int) -> bool:
        if value < 0:
            print(f"{self._name}: Error, age can't be negative")
            return False
        self._age = value
        return True

    def grow(self) -> None:
        self.set_height(self._height + 0.8)

    def age(self) -> None:
        self.set_age(self._age + 1)

    def show(self) -> None:
        print(f"{self._name}: {self.get_height()}cm,", end="")
        print(f" {self.get_age()} days old")

    def show_init(self) -> None:
        print("Plant created:", end="")
        self.show()

    def show_height(self) -> None:
        print(f"{self.get_height()}cm")

    def show_age(self) -> None:
        print(f"{self.get_age()} days old")

    def update_height(self, value: float) -> None:
        if self.set_height(value):
            print(f"Height updated: {int(self.get_height())}cm")
        else:
            print("Height update rejected")

    def update_age(self, value: int) -> None:
        if self.set_age(value):
            print(f"Age updated: {self.get_age()} days")
        else:
            print("Age update rejected")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose: Plant = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    rose.show()
    print()
    rose.update_height(25.0)
    rose.update_age(30)
    print()
    rose.update_height(-5)
    rose.update_age(-76)
    print()
    print("Current state: ", end="")
    rose.show()
