#!/usr/bin/env python3


class Plant:
    def __init__(self, p_name: str, p_height: float, p_age: int) -> None:
        self.p_name = p_name
        self.p_height = p_height
        self.p_age = p_age

    def show(self) -> None:
        print(f"{self.p_name}: {round(self.p_height, 1)}cm, {self.p_age} days old")

    def grow(self) -> None:
        self.p_height = self.p_height + 0.8

    def age(self) -> None:
        self.p_age = self.p_age + 1


if __name__ == "__main__":
    print("=== Garden Plant Growth ===")

    rose: Plant = Plant("Rose", 25.0, 30)
    rose_ih: float = rose.p_height
    rose.show()
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.grow()
        rose.age()
        rose.show()
    t_growth: float = round(rose.p_height - rose_ih, 1)
    print(f"Growth this week: {t_growth}cm")
