#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from sensor_msgs.msg import LaserScan
from carkyo_msgs.msg import CameraEmergency
from geometry_msgs.msg import Twist

class MyNode(Node):
    front_scan = []
    back_scan = []
    free_path_fwd_lidar = 0
    free_path_fwd_camera = 0
    free_path_bwd = 0
    cmd_vel_msg = Twist()

    def __init__(self):
        super().__init__("publisher")
        self.get_logger().info("Node is started now")
        self.create_subscription(LaserScan,"scan",self.scan_callback,10)
        self.create_subscription(Twist,"key_cmd_vel",self.key_cmd_vel_callback,10)
        
        self.create_subscription(CameraEmergency,"CameraEmergency",self.camera_callback,10)
        self.create_timer(1/2,self.cmd_vel_pub)
        self.obj_pub=self.create_publisher(Twist,"cmd_vel",10)


    def scan_callback(self,msg):
        self.front_scan = msg.ranges[0:45]
        self.front_scan.extend(msg.ranges[315:360])

        self.back_scan = msg.ranges[135:225]

        self.obstacle = min(self.front_scan)
        self.obstacle_back = min(self.back_scan)

        if self.obstacle > 0.45:
            self.free_path_fwd_lidar = 1
        else:
            self.free_path_fwd_lidar = 0

        if self.obstacle_back > 0.45:
            self.free_path_bwd = 1
        else:
            self.free_path_bwd = 0
       

    def key_cmd_vel_callback(self,msg):
        self.cmd_vel_msg = msg
    
    def camera_callback(self,msg):
        if msg.close_obstacle_detected:
        	self.free_path_fwd_camera = 0
        else:
        	self.free_path_fwd_camera = 1

    def cmd_vel_pub(self):
        msg=Twist()

        self.get_logger().info(str(msg))
        if (self.free_path_fwd_lidar and self.free_path_fwd_camera)  and self.free_path_bwd:
            msg = self.cmd_vel_msg
        
        elif (self.free_path_fwd_lidar==0 or self.free_path_fwd_camera==0) and self.free_path_bwd:
            msg = self.cmd_vel_msg
            if msg.linear.x > 0:
                msg.linear.x = 0.0
        
        elif (self.free_path_fwd_lidar and self.free_path_fwd_camera) and self.free_path_bwd==0:
            msg = self.cmd_vel_msg
            if msg.linear.x < 0:
                msg.linear.x = 0.0
        
        else:
            msg = self.cmd_vel_msg
            msg.linear.x = 0.0
            self.get_logger().info("no free path")

        self.obj_pub.publish(msg)
        
def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
