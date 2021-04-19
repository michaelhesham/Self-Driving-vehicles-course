num = input("please enter any number ")
num = int(num)

sum_of_num = 0

for i in range(num+1):
	sum_of_num = sum_of_num + i

print(f"The sum of Natural Numbers from 1 to {num} = {sum_of_num}")   
sum_of_num = float(sum_of_num)
print(f"Average Natural Numbers from 1 to {num} = {sum_of_num/num}")   
	
