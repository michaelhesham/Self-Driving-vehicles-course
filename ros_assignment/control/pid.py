#!/usr/bin/env python3

# Michael Hesham
#Mohamed Hesham
#Khaled shalby
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import serial
import time

class MyNode(Node):
    v_linear = 0
    v_angular = 0
    L = 0.58
    vl = 0
    vr = 0

    kp_left=270
    ki_left=30
    kd_left=0
    cum_error_left=0
    error_left = 0
    t2_left = time.time()
    t1_left = time.time()

    kp_right=270
    ki_right=30
    kd_right=0
    cum_error_right=0
    error_right = 0
    t2_right = time.time()
    t1_right = time.time()  

    def __init__(self):
        super().__init__("publisher")
        self.get_logger().info("Node is started now")

        self.create_subscription(Twist,"key_cmd_vel",self.key_cmd_vel_callback,10) 
        self.create_timer(1/20,self.pwm)
        
        self.ser = serial.Serial('/dev/ttyACM0')
        self.ser.flushInput()

    def key_cmd_vel_callback(self,msg):
        # calculations to get v right and v left
        self.v_linear = msg.linear.x
        self.v_angular = msg.angular.z

        v_right_minus_v_left = self.v_angular/self.L
        v_right_plus_v_left = self.v_linear * 2
        
        self.vl = (v_right_plus_v_left - v_right_minus_v_left)/2
        self.vr = v_right_minus_v_left + self.vl
    
    def pwm(self):
        #ser.reset_input_buffer()
        data = self.ser.readline().decode("ascii").split(",")
        vl_actual = float(data[1])
        vr_actual = float(data[2])
        
        # pid control vl
        self.t1_left = time.time()
        elapsed_time_left = self.t1_left - self.t2_left
        last_error_left = self.error_left
        self.error_left = self.vl - vl_actual
        self.cum_error_left += self.error_left*elapsed_time_left
        rate_error_left = (self.error_left - last_error_left)/elapsed_time_left
        if self.ki_left*self.cum_error_left >255:
            self.cum_error_left = 255/18
        u_left = self.kp_left*self.error_left + self.ki_left*self.cum_error_left + self.kd_left*rate_error_left
        u_left %= 255

        if self.v_linear < 0:
            u_left = -u_left
        self.t2_left = time.time()

        
        # pid control vr
        self.t1_right = time.time()
        elapsed_time_right = self.t1_right - self.t2_right
        last_error_right = self.error_right
        self.error_right = self.vr - vr_actual
        self.cum_error_right += self.error_right*elapsed_time_right
        if self.ki_right*self.cum_error_right >255:
            self.cum_error_right = 255/18
        rate_error_right = (self.error_right - last_error_right)/elapsed_time_right
        u_right = self.kp_right*self.error_right + self.ki_right*self.cum_error_right + self.kd_right*rate_error_right
        u_right %= 255
        if self.v_linear < 0:
            u_right = -u_right
        self.t2_right = time.time()

        # send serial message of u_left and u_right
        self.ser.write(("{},{}".format(u_left,u_right).encode()))
        #ser.write("100,100}".encode())
        print(f"command {self.v_linear},{self.v_angular}")
        print(f"{u_left},{u_right}")
        print(f"{vl_actual},{vr_actual}")
        

def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()


'''
    vr - vl = 5
    vr + vl = 2
    v_right_minus_v_left + 2vl = v_right_plus_v_left
    vl = (v_right_plus_v_left - v_right_minus_v_left)/2
'''
