max = 0
min = 0

x = input("Enter a number ")

while 1:
    x = input("Enter a number ")
    if x>0:
        if int(x) > max:
            max = int(x)
        elif int(x) < min:
            min = int(x)
    else:
        if x == "done":
            print(f"Maximum is {max}")  
            print(f"Minimum is {min}")
        else:
            print("invalid input")