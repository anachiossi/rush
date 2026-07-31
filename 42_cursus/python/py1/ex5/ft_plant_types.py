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
        print(f"{self.get_height}cm")

    def show_age(self) -> None:
        print(f"{self.get_age} days old")

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


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self._color: str = color
        self._bloomed: bool = False

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if self._bloomed:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")

    def bloom(self) -> None:
        self._bloomed = True


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float) -> None:
        super().__init__(name, height, age)
        self._trunk_diameter: float = trunk_diameter

    def shade(self) -> None:
        print(f"Tree {self._name} now produces a shade of "
              f"{self.get_height()}cm long and {self._trunk_diameter}cm wide.")

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter}cm")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int,
                 harvest_season: str) -> None:
        super().__init__(name, height, age)
        self._harvest_season: str = harvest_season
        self._nutritional_value: int = 0

    def grow(self) -> None:
        super().grow()
        self.grow_bonus()

    def grow_bonus(self) -> None:
        self.set_height(round(self.get_height() + 1.3, 1))
        self._nutritional_value += 1

    def age(self) -> None:
        super().age()

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    print("=== Flower")
    rose: Flower = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()
    print()
    print("=== Tree")
    oak: Tree = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.shade()
    print()
    print("=== Vegetable")
    tomato: Vegetable = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()
