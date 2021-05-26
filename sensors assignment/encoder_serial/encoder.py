'''
#!/usr/bin/env python3

import rclpy
import numpy as np
from rclpy.node import Node
from nav_msgs.msg import Odometry
'''
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)  # open serial port
print(ser.name)         # check which port was really used
wheel_base = 2
while (1):
	encoder_msg = ser.read()     # read a string
	print(encoder_msg)
	msg = encoder_msg.split(',') # split a string

	v_lin = (float(msg[0])+float(msg[2]))/2       # calculate linear velocity
	w = (float(msg[0])+float(msg[2]))/wheel_base  # calculate angular velocity
	
	print(f"linear velocity: {v_lin}")  # print linear velocity
	print(f"angular velocity: {w}")     # print angular velocity

'''
class MyNode(Node):
    count = 1
    
    def __init__(self):
        super().__init__("Odom")

        self.get_logger().info("Node is started now")
        
        self.create_timer(1/2,self.timer_call)
        self.obj_pub=self.create_publisher(Odom,"odom",10)
            

    def timer_call(self):
    	msg = Odom()
    	msg.twist.twist.linear.x = v_lin
    	msg.twist.twist.angular.x = w
    	msg.twist.covariance[0] = 0.001
    	msg.twist.covariance[7] = -1
    	msg.twist.covariance[14] = -1
    	msg.twist.covariance[21] = 0.001
    	msg.twist.covariance[28] = -1
    	msg.twist.covariance[35] = -1
    	self.obj_pub.publish(msg) 

def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
'''
