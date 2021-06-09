#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, sqrt, atan2
from example_interfaces.msg import Int16


class MyNode(Node):
    goal_x = 9
    goal_y = 9
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

        self.create_subscription(Pose,"turtle1/pose",self.current_call,10)
        self.get_logger().info("subscriber started")

    
    def current_call(self,msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def euclidean_distance(self):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((self.goal_x - self.current_x), 2) +
                    pow((self.goal_y - self.current_y), 2))
    kp_linear=1.5
    ki_linear=0.01
    kd_linear=0.1
    cum_error_linear=0
    error_linear = 0
    t2 = time.time()
    t1 = time.time()
    def linear_vel(self, constant=1.5):
        self.t1 = time.time()
        elapsed_time = self.t1 - self.t2
        last_error = self.error_linear
        self.error_linear = self.euclidean_distance()
        self.cum_error_linear += self.error_linear*elapsed_time
        rate_error = (self.error_linear - last_error)/elapsed_time
        u_linear = self.kp_linear*self.error_linear + self.ki_linear*self.cum_error_linear + self.kd_linear*rate_error
        self.t2 = time.time()
        print(u_linear)
        return u_linear
    kp_angular=1.5
    ki_angular=0.001
    kd_angular=0.2
    cum_error_angular=0
    error_angular = 0
    t2_angular = time.time()
    t1_angular = time.time()
    def steering_angle(self):
        self.t1_angular = time.time()
        elapsed_time = self.t1_angular - self.t2_angular
        last_error = self.error_angular
        self.error_angular = atan2(self.goal_y - self.current_y, self.goal_x - self.current_x) 
        self.cum_error_angular += self.error_angular*elapsed_time
        rate_error = (self.error_angular - last_error)/elapsed_time
        u_angular = self.kp_angular*self.error_angular + self.ki_angular*self.cum_error_angular + self.kd_angular*rate_error
        self.t2_angular = time.time()
        print(u_angular)
        return u_angular

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