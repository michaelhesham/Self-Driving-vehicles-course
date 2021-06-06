#!/usr/bin/env python3

import rclpy
import numpy as np
import math
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2
import time

# Instantiate CvBridge
bridge = CvBridge()

class my_node (Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Image,"/intel_realsense_d435_depth/image_raw",self.img_cb, rclpy.qos.qos_profile_sensor_data)
        
        self.get_logger().info("subscriber is started")


        
    def img_cb(self,message):
        cv2_img = bridge.imgmsg_to_cv2(message, "bgr8")
        #cv2.imwrite('saved_img.png', cv2_img)
        img  = np.ones((cv2_img.shape[0], cv2_img.shape[1], 3), np.uint8)
        
        gray = cv2.cvtColor(cv2_img,cv2.COLOR_BGR2GRAY)
        t1 = time.time()
        corners = cv2.goodFeaturesToTrack(gray,50,0.01,10,useHarrisDetector=False)
        corners = np.int0(corners)
        t2 = time.time()
        for i in corners:
            x,y = i.ravel()
            cv2.circle(img,(x,y),1,(0,0,255),thickness=1)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"{t2-t1}", (10, 220), font, 1, (220, 120, 25), 2, cv2.FILLED)   
        # concatanate image Horizontally
        Hori = np.concatenate((cv2_img, img), axis=1)
        cv2.imshow("imgage", Hori)
        cv2.waitKey(1)
          
def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()


