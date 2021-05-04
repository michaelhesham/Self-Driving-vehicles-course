#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_msgs.msg import Lab3

class MyNode(Node):
    def __init__(self):
        super().__init__("int_publisher")
        self.create_timer(1/2,self.timer_call)
        self.get_logger().info("Node is started now")
        self.obj_pub=self.create_publisher(Lab3,"number",10)


    def timer_call(self):
        msg=Lab3()
        msg.message="Michael is publishing: 5"
        msg.number=5
        self.obj_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()