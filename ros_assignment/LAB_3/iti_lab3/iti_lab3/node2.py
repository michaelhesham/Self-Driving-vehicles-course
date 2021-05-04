#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_msgs.msg import Lab3
from my_msgs.srv import Lab3sr
from example_interfaces.msg import Int64

class MyNode(Node):
    counter = 0
    def __init__(self):
        super().__init__("number_counter")
        self.create_subscription(Lab3,"number",self.sub_call,10)
        self.get_logger().info("subscriber started")

        self.create_timer(1/2,self.pub_call)
        self.obj_pub=self.create_publisher(Int64,"number_counter",10)

        self.create_service(Lab3sr,"data",self.srv_call)

    def sub_call(self,msg):
        self.counter += msg.number

    def pub_call(self):
        msg=Int64()
        msg.data=self.counter
        self.obj_pub.publish(msg)

    def srv_call(self,rq,rsp):
    	req_data=rq.flag
    	rsp.success=req_data
    	self.get_logger().info(str(rsp))
    	self.counter = 0
    	return rsp

def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()