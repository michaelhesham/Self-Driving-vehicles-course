#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class my_node (Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(String,"my_topic",self.timer_call,10)
        
        self.get_logger().info("subscriber is started")

    def timer_call(self,msg):
        self.get_logger().info("I received " + msg.data)

        
        
        
      




def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__=="__main__":
    main()


