#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class MyNode(Node):
    counter = 0
    reset_flag = 0
    def __init__(self):
        super().__init__("Node2")
        self.create_timer(1/2,self.pub_msg)
        self.create_subscription(String,"Node1_msg",self.timer_call,10)
        self.get_logger().info("Node2 is started")
        self.flag_pub=self.create_publisher(String,"flag_msg",10)
        self.count_pub=self.create_publisher(String,"count_msg",10)


    def timer_call(self,msg):
        recieved = msg.data
        self.counter = recieved[-1]
        self.get_logger().info(self.counter)
        

    def pub_msg(self):
        if int(self.counter) == 5:
            self.reset_flag = 1
        else:
            self.reset_flag = 0
        msg2=String()
        msg3=String()
        msg2.data=str(self.counter)
        msg3.data=str(self.reset_flag)
        self.count_pub.publish(msg2)
        self.flag_pub.publish(msg3)


def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()