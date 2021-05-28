#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
import numpy as np
from example_interfaces.msg import Int16

class my_server(Node):
    goal = 0
    kill = 0
    def __init__(self):
        super().__init__("Client_Spawn_node")
        x = np.random.randint(1,10)
        y = np.random.randint(1,10)
        self.service_client(float(x), float(y), 0.0, 'new_one')
        
        self.create_subscription(Int16,"goal",self.sub_call,10)
        self.get_logger().info("subscriber started")
        
        self.create_timer(1,self.kill_call)
        self.create_timer(1,self.spawn_call)
    
    def sub_call(self,msg):
        self.goal = msg.data

    def spawn_call(self):
        if self.kill == 1:
            self.goal = 0
            x = np.random.randint(1,10)
            y = np.random.randint(1,10)
            self.service_client(float(x), float(y), 0.0, 'new_one')
          
    def kill_call(self):
        if self.goal == 1 and self.kill == 0:
            self.kill_client('new_one')
          

    def service_client(self,x,y,theta,name):
        client=self.create_client(Spawn,"spawn")
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for spawn server")

        request=Spawn.Request()
        request.x=x
        request.y=y
        request.theta=theta
        request.name=name
        futur_obj=client.call_async(request)
        futur_obj.add_done_callback(self.future_call)

    def kill_client(self,name):
        client=self.create_client(Kill,"kill")
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for kill server")
        request=Kill.Request()
        request.name=name
        futur_obj=client.call_async(request)
        futur_obj.add_done_callback(self.kill_future_call)

    def future_call(self,future_msg):
        self.get_logger().info("new_one is spawned")
        self.kill = 0
        self.goal = 0
        
    def kill_future_call(self,future_msg):
        self.get_logger().info("new_one is killed")
        self.goal = 0
        self.kill = 1

       


def main (args=None):
    rclpy.init(args=args)
    node1=my_server()
    rclpy.spin(node1)
    rclpy.shutdown()

if __name__ == "__main__":
    main()