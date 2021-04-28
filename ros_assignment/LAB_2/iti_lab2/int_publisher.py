#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class MyNode(Node):
    def __init__(self):
        super().__init__("int_publisher")
        self.create_timer(1/2,self.timer_call)
        self.get_logger().info("int_publisher is started")
        self.obj_pub=self.create_publisher(Int64,"Number",10)


    def timer_call(self):
        msg=Int64()
        msg.data=5
        self.obj_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
