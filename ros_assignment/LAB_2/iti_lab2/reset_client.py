#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool

class my_server(Node):
    def __init__(self):
        super().__init__("reset_client")
        self.service_client(bool(1))



    def service_client(self,data):
        client=self.create_client(SetBool,"data")
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for server")

        request=SetBool.Request()
        request.data=data
        futur_obj=client.call_async(request)
        futur_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        self.get_logger().info(str(future_msg.result().success))
        


       


def main (args=None):
    rclpy.init(args=args)
    node1=my_server()
    rclpy.spin(node1)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
