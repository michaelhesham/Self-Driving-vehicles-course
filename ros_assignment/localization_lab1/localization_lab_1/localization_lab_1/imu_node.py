#!/usr/bin/env python3

import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from math import sin, cos, pi

class MyNode(Node):
    def __init__(self):
        super().__init__("subscriber")
        self.create_subscription(Imu,"imu",self.timer_call,10)
        self.get_logger().info("subscriber started")

    def timer_call(self,msg):
        self.orientation = msg.orientation
        self.linear_acceleration = msg.linear_acceleration
        self.angular_velocity = msg.angular_velocity

        roll, pitch, yaw = self.euler_from_quaternion(self.orientation)
        
        if yaw * (180/np.pi) > -2 and yaw * (180/np.pi) <2: 
            self.get_logger().info(f"The robot is nearly heading north .. Heading is: {yaw*(180/np.pi)} degrees")

        if abs(self.linear_acceleration.x) > 0.3:
            self.get_logger().warning(f"warnning !! .. linear acceleration x exceeds the limit. Current acceleration is {self.linear_acceleration.x} m/s^2")

        if abs(self.angular_velocity.z) > 0.3:
            self.get_logger().warning(f"warnning !! .. angular velocity exceeds the limit. Current acceleration is {self.angular_velocity.z} rad/s")

    def euler_from_quaternion(self, quaternion):
        x = quaternion.x
        y = quaternion.y
        z = quaternion.z
        w = quaternion.w

        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        pitch = np.arcsin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw 



def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()