#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MyServer(Node):
	def __init__(self):
		super().__init__("server_node")
		self.create_service(AddTwoInts,"First_server",self.srv_call)
		
	def srv_call(self,rq,rsp):
		req_a=rq.a
		req_b=rq.b
		rsp.sum=req_a + req_b
		self.get_logger().info(str(rsp))
		return rsp
		

def main(args=None):
	rclpy.init(args=args)
	node1=MyServer()
	rclpy.spin(node1)
	rclpy.shutdown()
	
if __name__ == "__main__":
	main()

