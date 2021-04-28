#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class MyNode(Node):
    number_counter = 0
    def __init__(self):
        super().__init__("number_counter")
        self.create_timer(1/2,self.pub_call)
        self.create_subscription(Int64,"/Number",self.timer_call,10)
        self.get_logger().info("number_counter is started")
        self.obj_pub=self.create_publisher(Int64,"number_counter",10)
        self.create_service(SetBool,"data",self.srv_call)

    def timer_call(self,msg):
        self.number_counter += msg.data
        
    def pub_call(self):
    	msg=Int64()
    	msg.data=self.number_counter
    	self.obj_pub.publish(msg)
    	self.get_logger().info(str(self.number_counter))
    
    def srv_call(self,rq,rsp):
    	req_data=rq.data
    	rsp.success=req_data
    	self.get_logger().info(str(rsp))
    	self.number_counter = 0
    	return rsp
   

def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
