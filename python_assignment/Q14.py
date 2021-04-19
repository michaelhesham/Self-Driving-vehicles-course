max = 0
min = 0

while 1:
    x = input("Enter a number")
    if x > max:
        max = x
    elif x < min:
        min = x
    
    if x == "done":
        print(f"Maximum is {max}")
        print(f"Minimum is {min}")
    else:
        print("Invalid input")
    