def ft_water_reminder():
    w = int(input("Days since last watering: "))
    if w <= 2:
        print("Plants are fine")
    else:
        print("Water the plants!")
