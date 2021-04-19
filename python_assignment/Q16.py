File = open("mbox-short.txt",'r')

Read = File.readline()

counter = 0

for line in File:
    if line.startswith('From'):
        y = line.split(' ')
        print(y[1])
        counter += 1

print(f"there are {counter} lines with from as first word")
File.close()