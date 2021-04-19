height = input("please enter pyramid height ")
height = int(height)

spaces = height - 1
stars = 1

for i in range(0,height):
	for j in range(0,spaces):
		print(end=" ")
	spaces = spaces - 1
	for j in range(0,stars):
		print("*",end="")
	stars =stars + 2
	print("\r")