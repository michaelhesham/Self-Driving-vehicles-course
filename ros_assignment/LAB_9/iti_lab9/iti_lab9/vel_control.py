#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
from std_srvs.srv import Empty

# read csv file and save linear and angular velocity in 2 lists
File = open("turtle_commands.csv",'r')
linear = []
angular = []
count = 0
for line in File:
    print(line)
    Read = line.split(',')
    linear.append(Read[0])
    angular.append(Read[1])
    count += 1
File.close()


class MyNode(Node):
    count = 1
    
    def __init__(self):
        super().__init__("publisher")

        self.get_logger().info("Node is started now")
        
        # timer to call velocity publisher
        self.create_timer(1,self.move_call)
        
        self.obj_pub=self.create_publisher(Twist,"turtle1/cmd_vel",10)
        
        # subscribe to turtle position 
        self.create_subscription(Pose,"turtle1/pose",self.sub_call,10)
        
        # timer to reset service when turtle is out of position
        self.create_timer(1/2,self.reset_call)
        

    def move_call(self):
        if self.current_x > 2 and self.current_x < 8 and self.current_y < 8 and self.current_y > 2:
            msg=Twist()
            msg.linear.x=float(linear[self.count])
            msg.linear.y=0.0
            msg.linear.z=0.0

            msg.angular.x=0.0
            msg.angular.y=0.0
            msg.angular.z=float(angular[self.count])
            self.obj_pub.publish(msg)
            self.count += 1
            if self.count == len(linear):
                self.count = 1

    def sub_call(self,msg):
        self.current_x = msg.x
        self.current_y = msg.y
      
    
    def reset_call(self):
        if self.current_x < 2 or self.current_x > 8 or self.current_y > 8 or self.current_y < 2:
            self.reset_client()

    def reset_client(self):
        client=self.create_client(Empty,"reset")
        while client.wait_for_service(0.25)==False:
            self.get_logger().warn("wating for spawn server")

        request=Empty.Request()
        futur_obj=client.call_async(request)
        futur_obj.add_done_callback(self.reset_future_call)

    def reset_future_call(self,future_msg):
        self.get_logger().info("turtle is reseted")
          
def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()