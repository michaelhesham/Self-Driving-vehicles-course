#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class MyNode(Node):
    front_scan = []
    free_path = 0
    cmd_vel_msg = Twist()

    def __init__(self):
        super().__init__("publisher")
        self.get_logger().info("Node is started now")
        self.create_subscription(LaserScan,"scan",self.scan_callback,10)
        self.create_subscription(Twist,"key_cmd_vel",self.key_cmd_vel_callback,10)
        self.create_timer(1/2,self.cmd_vel_pub)
        self.obj_pub=self.create_publisher(Twist,"cmd_vel",10)


    def scan_callback(self,msg):
        self.front_scan = msg.ranges[0:45]
        self.front_scan.extend(msg.ranges[315:360])
        self.obstacle = min(self.front_scan)

        if self.obstacle > 0.45:
            self.free_path = 1
        else:
            self.free_path = 0

        self.get_logger().info("obs: "+str(self.obstacle))


    def key_cmd_vel_callback(self,msg):
        self.cmd_vel_msg = msg

    def cmd_vel_pub(self):
        msg=Twist()

        self.get_logger().info(str(msg))
        if self.free_path:
            msg = self.cmd_vel_msg
            self.get_logger().info("free path")

        else:
            msg = self.cmd_vel_msg
            if msg.linear.x > 0:
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
