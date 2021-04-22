import numpy as np

zed_file = open("python_test_file.txt")
zed_file_update = open("zed_file_update.txt",'a')
read_zed_file = zed_file.readline().splitlines

for line in zed_file:
    index = line.find("velocity")
    new_line = line[index:]
    print(new_line)
    arr = new_line.split('   ')
    arr[1]=arr[1].replace('+','')
    arr[2]=arr[2].replace('+','')
    arr[3]=arr[3].replace('+','')
    arr[1]=arr[1].replace('-','')
    arr[2]=arr[2].replace('-','')
    arr[3]=arr[3].replace('-','')
    arr[1]=arr[1].replace(',','')
    arr[2]=arr[2].replace(',','')
    arr[3]=arr[3].replace(',','')
    if arr[1] != '':
        speed = pow(float(arr[1]),2)+pow(float(arr[2]),2)+pow(float(arr[3]),2)
        print(speed)
    else:
        speed = ''
    zed_file_update.write(line + " ,speed " + str(speed) + "\n")

zed_file.close()
zed_file_update.close()