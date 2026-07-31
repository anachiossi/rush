def ft_count_harvest_recursive():
    n = int(input("Days until harvest: "))

    def ft_count(day):
        if day > n:
            print("Harvest time!")
            return
        print(f"Day {day}")
        ft_count(day + 1)

    ft_count(1)
