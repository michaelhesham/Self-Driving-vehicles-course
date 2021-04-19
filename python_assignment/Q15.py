file = open("abc.txt",'r')
file2 = open("words.txt",'w')

Read = file.readline()

for line in file:
    print(line.upper())
    file2.write(line.upper())

file.close()
file2.close()
