def ft_count_harvest_recursive():
    n = int(input("Days until harvest: "))
    ft_count(1, n)


def ft_count(day, n):
    if day > n:
        print("Harvest time!")
        return
    print(f"Day {day}")
    ft_count(day + 1, n)
