#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

'''
def main(args=None):
    rclpy.init(args=args)
    node = Node("Michael")
    node.get_logger().info("Node is strated")
    rclpy.spin(node)

    rclpy.shutdown()
'''

class MyNode(Node):
    def __init__(self):
        super().__init__("node_name")
        self.create_timer(1/2,self.timer_call)
        self.get_logger().info("Node is started now")

    def timer_call(self):
        self.get_logger().info("Hello number 1234")

def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
    
