#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty

class my_server(Node):
    def __init__(self):
        super().__init__("Client_Reset_node")
        self.service_client()



    def service_client(self):
        client=self.create_client(Empty,"reset")
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for server")

        request=Empty.Request()
        futur_obj=client.call_async(request)
        futur_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        self.get_logger().info(str(future_msg.result()))
        


       


def main (args=None):
    rclpy.init(args=args)
    node1=my_server()
    rclpy.spin(node1)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
