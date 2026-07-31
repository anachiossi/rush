#!/usr/bin/env python3

class Plant:
    def __init__(self, p_name: str, p_height: float, p_age: int) -> None:
        self.p_name = p_name
        self.p_height = p_height
        self.p_age = p_age

    def show(self) -> None:
        print(f"{self.p_name}: {self.p_height}cm, {self.p_age} days old")

    def grow(self) -> None:
        self.p_height = round(self.p_height + 0.8, 1)


if __name__ == "__main__":
    plants: list[Plant] = [
        Plant("Rose", 25.0, 30),
        Plant("Oak", 200.0, 365),
        Plant("Cactus", 5.0, 90),
        Plant("Sunflower", 80.0, 45),
        Plant("Fern", 15.0, 120)
        ]

    print("=== Plant Factory Output ===")
    for plant in plants:
        print("Created: ", end="")
        plant.show()
