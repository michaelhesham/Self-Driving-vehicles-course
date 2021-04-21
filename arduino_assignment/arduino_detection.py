#open file that contains devices
dev_file = open("filewithdev.txt",'r')

#read file line by line
read_line = dev_file.readline()

#creating flag with initial value equal 0
found =0

#creating counter with initial value equal 0
counter = 0

#creating variable to save index of line with ttyACM0
arduino_index = 0

#search for ttyACM0 in file and set flag if found
for line in dev_file:
    counter += 1
    if "ttyACM0" in line and found == 0:
        usb_index = line.find("usb")
        usb_index = line[usb_index+3]
        found = 1

#close file
dev_file.close()


#print out status of Arduino
#print found if it is found and connected to usb1
if found == 1 and usb_index == '1':
    print("WOW, Arduino device was found")
else:
    print("Sorry, No Arduino device was found")
