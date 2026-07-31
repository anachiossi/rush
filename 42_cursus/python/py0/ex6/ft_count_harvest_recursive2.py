def ft_count_harvest_recursive(n=None, day=1):
    if n is None:
        n = int(input("Days until harvest: "))
    if day > n:
        print("Harvest time!")
        return
    print(f"Day {day}")
    ft_count_harvest_recursive(n, day + 1)
