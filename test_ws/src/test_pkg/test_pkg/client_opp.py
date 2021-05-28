#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn

class my_server(Node):
    def __init__(self):
        super().__init__("Client_Spawn_node")
        self.service_client(4.0, 8.0, 0.0, 'new_one')



    def service_client(self,x,y,theta,name):
        client=self.create_client(Spawn,"spawn")
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for server")

        request=Spawn.Request()
        request.x=x
        request.y=y
        request.theta=theta
        request.name=name
        futur_obj=client.call_async(request)
        futur_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        self.get_logger().info(str(future_msg.result().name))
        


       


def main (args=None):
    rclpy.init(args=args)
    node1=my_server()
    rclpy.spin(node1)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
