#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

def main(args=None):
	rclpy.init(args=args)
	client=Node("My_client_node")
	client_obj=client.create_client(AddTwoInts,"First_server")
	while client_obj.wait_for_service(0.5) == False:
		client.get_logger().warn("wait for server node")
	
	req = AddTwoInts.Request()
	req.a=10
	req.b=10
	future_obj=client_obj.call_async(req)
	rclpy.spin_until_future_complete(client,future_obj)
	response=future_obj.result()
	client.get_logger().error(str(response.sum))
	
	rclpy.shutdown
	
if __name__ == "__main__":
	main()

