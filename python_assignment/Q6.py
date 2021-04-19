list1 = ["red","orange","blue","black"]
File = open("list.txt",'w')

for item in list1:
    File.write(f"{item} \n")

File.close()