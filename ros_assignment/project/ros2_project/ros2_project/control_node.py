#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, sqrt, atan2
from example_interfaces.msg import Int16


class MyNode(Node):
    goal_x = 0
    goal_y = 0
    current_x = 0
    current_y = 0
    current_theta = 0
    goal = False
    def __init__(self):
        super().__init__("control_node")

        self.create_timer(1/2,self.move_call)
        self.get_logger().info("Node is started now")
        self.obj_pub=self.create_publisher(Twist,"turtle1/cmd_vel",10)

        self.goal_pub=self.create_publisher(Int16,"goal",10)


        self.create_subscription(Pose,"new_one/pose",self.goal_call,10)
        self.get_logger().info("subscriber started")
        
        self.create_subscription(Pose,"turtle1/pose",self.current_call,10)
        self.get_logger().info("subscriber started")


    def goal_call(self,msg):
        self.goal_x = msg.x
        self.goal_y = msg.y
    
    def current_call(self,msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def euclidean_distance(self):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((self.goal_x - self.current_x), 2) +
                    pow((self.goal_y - self.current_y), 2))

    def linear_vel(self, constant=1.5):
        return constant * self.euclidean_distance()

    def steering_angle(self):
        return atan2(self.goal_y - self.current_y, self.goal_x - self.current_x)

    def angular_vel(self, constant=2):
        return constant * (self.steering_angle() - self.current_theta)

    def move_call(self):
        if self.euclidean_distance() >= 0.1:
            self.linear_x = self.linear_vel()
            self.angular_z = self.angular_vel()
            if abs(self.angular_z) > 11:
                self.angular_z = 0
            
            msg=Twist()
            msg.linear.x=self.linear_x
            msg.linear.y=0.0
            msg.linear.z=0.0

            msg.angular.x=0.0
            msg.angular.y=0.0
            msg.angular.z=float(self.angular_z)
            self.obj_pub.publish(msg)
            msg1 = Int16()
            msg1.data = 0
            self.goal_pub.publish(msg1)
        else:
            msg1 = Int16()
            msg1.data = 1
            self.goal_pub.publish(msg1)
            
    
def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
        


if __name__ == "__main__":
    main()