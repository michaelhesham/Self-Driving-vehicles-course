#!/usr/bin/env python3

import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from math import sin, cos, pi

# read csv file and save linear and angular velocity in 2 lists
File = open("imu_data.csv",'r')
accX = []
accY = []
accZ = []

angX = []
angY = []
angZ = []

yaw_degree = []

for line in File:
    print(line)
    Read = line.split(',')
    accX.append(float(Read[0]))
    accY.append(float(Read[1]))
    accZ.append(float(Read[2]))

    angX.append(float(Read[3]))
    angY.append(float(Read[4]))
    angZ.append(float(Read[5]))

    yaw_degree.append(float(Read[6]))
   
File.close()

class MyNode(Node):
    count = 1
    
    def __init__(self):
        super().__init__("publisher")

        self.get_logger().info("Node is started now")
        
        # timer to call velocity publisher
        self.create_timer(1/30,self.imu_call)
        
        self.obj_pub=self.create_publisher(Imu,"zed2_imu",10)
            

    def imu_call(self):
        msg=Imu()
        msg.header.frame_id = "zed2_imu_link"
        msg.header.stamp = Node.get_clock(self).now().to_msg()
        
        if angZ[self.count] < 0.3:
            yaw = 0.00001
            z = 0.0001
        else:
            yaw = 1.0
            z = 1.0

        msg.linear_acceleration.x = accX[self.count]*9.80665
        msg.linear_acceleration.y = accY[self.count]*9.80665
        msg.linear_acceleration.z = accZ[self.count]*9.80665
        msg.linear_acceleration_covariance = [0.00001, 0.0, 0.0, 0.0, 0.00001, 0.0, 0.0, 0.0, 0.00001]

        msg.angular_velocity.x = angX[self.count]
        msg.angular_velocity.y = angY[self.count]
        msg.angular_velocity.z = angZ[self.count]
        msg.angular_velocity_covariance = [0.00001, 0.0, 0.0, 0.0, 0.00001, 0.0, 0.0, 0.0, z]

        msg.orientation = self.quaternion_from_euler(0,0,yaw_degree[self.count]*(np.pi/180))    
        msg.orientation_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, yaw]

        
        self.count += 1 
        self.obj_pub.publish(msg)
          
    def quaternion_from_euler(self, roll, pitch, yaw):
        qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
        qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
        qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
        qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)

def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()