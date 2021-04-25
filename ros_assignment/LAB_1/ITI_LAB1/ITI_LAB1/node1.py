#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class MyNode(Node):
    counter = 0
    def __init__(self):
        super().__init__("Node1")
        self.create_timer(1/2,self.timer_call)
        self.get_logger().info("Node is started now")
        self.obj_pub=self.create_publisher(String,"Node1_msg",10)
        self.create_subscription(String,"flag_msg",self.sub_call,10)


    def timer_call(self):
        self.get_logger().info("Michael Hesham is publish, "+str(self.counter))
        msg=String()
        msg.data="Michael Hesham is publish, "+str(self.counter)
        self.obj_pub.publish(msg)
        self.counter += 1

    def sub_call(self,msg2):
        reset_flag = msg2.data
        if int(reset_flag) == 1:
            self.counter = 0


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
