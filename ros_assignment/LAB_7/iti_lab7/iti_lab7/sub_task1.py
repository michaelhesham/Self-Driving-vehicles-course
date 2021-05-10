#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class MyNode(Node):
    count = 0
    def __init__(self):
        super().__init__("sub_task1")
        self.create_subscription(String,"my_topic",self.timer_call,rclpy.qos.qos_profile_sensor_data)
        self.get_logger().info("subscriber started")

    def timer_call(self,msg):
        self.count += 1
        self.get_logger().info("Michael heard: " + msg.data + " " + str(self.count) + " times")


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()