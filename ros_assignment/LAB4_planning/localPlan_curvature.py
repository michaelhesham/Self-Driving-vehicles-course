#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from example_interfaces.msg import String
import math
import numpy as np

class MyNode(Node):
    def __init__(self):
        super().__init__("subscriber")
        self.create_subscription(Path,"local_plan",self.timer_call,10)
        
        self.create_timer(1000,self.pub_call)
        self.obj_pub=self.create_publisher(String,"publisher_msg",10)
        self.get_logger().info("subscriber started")
    
    def timer_call(self,msg):
        self.get_logger().info(str(msg.poses[0].pose.position))
        self.plan_len = len(msg.poses)
        
        if self.plan_len >1:
            self.x1 = msg.poses[0].pose.position.x
            self.y1 = msg.poses[0].pose.position.y
    
            self.x2 = msg.poses[int(self.plan_len/2)].pose.position.x
            self.y2 = msg.poses[int(self.plan_len/2)].pose.position.y
    
            self.x3 = msg.poses[-1].pose.position.x
            self.y3 = msg.poses[-1].pose.position.y

            self.curvature = self.menger_curvature(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
            
            if float(self.curvature) < 1:
            	self.pub_call("The path is straight ")
            else:
                yaw_2 = self.euler_from_quaternion(msg.poses[1].pose.orientation)
                yaw_before_end = self.euler_from_quaternion(msg.poses[self.plan_len-1].pose.orientation)
                self.get_logger().info(str(yaw_2))
                self.get_logger().info(str(yaw_before_end))

                if yaw_2 > yaw_before_end:
                    self.pub_call(f"The robot is turning right with a curvature {self.curvature}")
                else:
                    self.pub_call(f"The robot is turning left with a curvature {self.curvature}")

    def pub_call(self,msg_data=""):
        msg=String()
        msg.data = msg_data
        self.obj_pub.publish(msg)

    def menger_curvature(self, point_1_x, point_1_y, point_2_x, point_2_y, point_3_x, point_3_y):
        triangle_area = 0.5 * abs( (point_1_x*point_2_y) + (point_2_x*point_3_y) + (point_3_x*point_1_y) - (point_2_x*point_1_y) - (point_3_x*point_2_y) - (point_1_x*point_3_y))#Shoelace formula 
            
        try:
            curvature = (4*triangle_area) / (math.sqrt(pow(point_1_x - point_2_x,2)+pow(point_1_y - point_2_y,2)) * math.sqrt(pow(point_2_x - point_3_x,2)+pow(point_2_y - point_3_y,2)) * math.sqrt(pow(point_3_x - point_1_x,2)+pow(point_3_y - point_1_y,2)))#Menger curvature 
            return curvature
        except:
            return 0 

    def euler_from_quaternion(self, quaternion):
	    """
	    Converts quaternion (w in last place) to euler roll, pitch, yaw
	    quaternion = [x, y, z, w]
	    Bellow should be replaced when porting for ROS 2 Python tf_conversions is done.
	    """
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

	    return yaw  

def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
