def fizz_buzz():
    """Fizz buzz exercise"""
    for i in range(1, 101):
        if i % 3 == 0:
            if i % 15 == 0:
                print("fizzbuzz")
            else:
                print("fizz")
        elif i % 5 == 0:
            print("buzz")
        else:
            print(i)


fizz_buzz()
