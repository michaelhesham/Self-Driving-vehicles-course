#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class MyNode(Node):
    def __init__(self):
        super().__init__("subscriber")
        self.create_subscription(String,"publisher_msg",self.timer_call,10)
        self.get_logger().info("subscriber started")

    def timer_call(self,msg):
        self.get_logger().info("I heard " + msg.data)


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
