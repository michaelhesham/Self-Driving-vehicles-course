#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from my_msgs.msg import Firstone

class MyNode(Node):
    def __init__(self):
        super().__init__("publisher")
        self.create_timer(1/2,self.timer_call)
        self.get_logger().info("Node is started now")
        self.obj_pub=self.create_publisher(Firstone,"publisher_msg",10)


    def timer_call(self):
        msg=Firstone()
        msg.message="My name is Michael"
        msg.number=100
        msg.check=True
        self.obj_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
