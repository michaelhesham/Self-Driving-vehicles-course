#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class MyNode(Node):
    def __init__(self):
        super().__init__("sub_task2")
        self.create_subscription(Pose,"turtle1/custom_pose",self.timer_call,rclpy.qos.qos_profile_sensor_data)
        self.get_logger().info("subscriber started")



    def timer_call(self,msg):
        X = str(msg.x)
        Y = str(msg.y)
        print(f"{X}, {Y}")


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()