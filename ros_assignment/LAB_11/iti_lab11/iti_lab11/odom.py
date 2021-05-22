#!/usr/bin/env python3

import rclpy
import numpy as np
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from math import sin, cos, pi


File = open("pose.csv",'r')
X_goal = []
Y_goal = []
yaw_goal = []
goal = -1
for line in File:
    print(line)
    Read = line.split(',')
    X_goal.append(Read[0])
    Y_goal.append(Read[1])
    yaw_goal.append(Read[2])
    goal += 1
File.close()

class MyNode(Node):
    count = 1
    
    def __init__(self):
        super().__init__("Odom")

        self.get_logger().info("Node is started now")
        
        
        self.create_subscription(Odometry,"odom",self.timer_call,10)
            

    def timer_call(self,msg):
        self.pose_x = msg.pose.pose.position.x
        self.pose_y = msg.pose.pose.position.y

        self.orienation = msg.pose.pose.orientation

        self.roll, self.pitch, self.yaw = self.euler_from_quaternion(self.orienation)
        
        self.get_logger().info(f"x {self.pose_x}")
        self.get_logger().info(f"x_goal {X_goal[self.count]}")

        self.get_logger().info(f"y {self.pose_y}")
        self.get_logger().info(f"y_goal {Y_goal[self.count]}")

        self.get_logger().info(f"yaw {self.yaw*(180/np.pi)}")
        self.get_logger().info(f"count {self.count}")
        self.get_logger().info(f"yaw_goal {yaw_goal[self.count]}")

        x_min = (float(X_goal[self.count])-0.5)
        x_max = (float(X_goal[self.count])+0.5)

        y_min = (float(Y_goal[self.count])-0.5)
        y_max = (float(Y_goal[self.count])+0.5)

        yaw_min = float(yaw_goal[self.count])-5
        yaw_max = float(yaw_goal[self.count])+5


        if (self.pose_x > x_min and self.pose_x < x_max) and \
           (self.pose_y > y_min and self.pose_y < y_max) and \
           ((self.yaw*(180/np.pi)) > yaw_min and (self.yaw*(180/np.pi)) < yaw_max):
            if self.count >= goal:
                self.get_logger().info(f"I execute all positions and last one is {X_goal[self.count]}, {Y_goal[self.count]}, {yaw_goal[self.count]}")
            else:
                self.get_logger().info(f"I have reached goal {self.count}")
                self.count += 1
                self.get_logger().info(f"Go to {self.count} position")

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