#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class MyNode(Node):
    flag = 0
    def __init__(self):
        super().__init__("publisher")
        self.create_timer(1,self.timer_call)
        self.get_logger().info("Node is started now")
        self.obj_pub=self.create_publisher(String,"publisher_msg",10)


    def timer_call(self):
        msg=String()
        if self.flag == 0:
        	msg.data="Hi"
        	self.flag = 1
        else:
        	msg.data="Hello"
        	self.flag = 0
        self.obj_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
