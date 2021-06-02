#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from example_interfaces.msg import String
import math

class MyNode(Node):
    def __init__(self):
        super().__init__("subscriber")
        self.create_subscription(Path,"plan",self.timer_call,10)
        
        self.create_timer(1000,self.pub_call)
        self.obj_pub=self.create_publisher(String,"publisher_msg",10)
        self.get_logger().info("subscriber started")

    def timer_call(self,msg):
        self.get_logger().info(str(msg.poses[0].pose.position))
        self.plan_len = len(msg.poses)
        self.counter = 0
        while self.plan_len > self.counter:
            if self.counter+20 < self.plan_len:
                self.x1 = msg.poses[self.counter].pose.position.x
                self.y1 = msg.poses[self.counter].pose.position.y
                self.counter += 10
                self.x2 = msg.poses[self.counter].pose.position.x
                self.y2 = msg.poses[self.counter].pose.position.y
                self.counter += 10
                self.x3 = msg.poses[self.counter].pose.position.x
                self.y3 = msg.poses[self.counter].pose.position.y
                self.curvature = self.menger_curvature(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
                if float(self.curvature) < 1:
                    self.pub_call("The path is straight ")
                else:
                    self.pub_call(f"The robot is turning with a curvature {self.curvature}")
            else :
                self.counter = self.plan_len
                self.pub_call("The plan curvature calculations finished")
        
    def pub_call(self,msg_data=""):
        msg=String()
        msg.data = msg_data
        self.obj_pub.publish(msg)

    def menger_curvature(self, point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y):
        triangle_area = 0.5 * abs( (point_1_x*point_2_y) + (point_2_x*point_3_y) + (point_3_x*point_1_y) - (point_2_x*point_1_y) - (point_3_x*point_2_y) - (point_1_x*point_3_y))#Shoelace formula 
            
        curvature = (4*triangle_area) / (math.sqrt(pow(point_1_x - point_2_x,2)+pow(point_1_y - point_2_y,2)) * math.sqrt(pow(point_2_x - point_3_x,2)+pow(point_2_y - point_3_y,2)) * math.sqrt(pow(point_3_x - point_1_x,2)+pow(point_3_y - point_1_y,2)))#Menger curvature 
        return curvature


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
