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

        self.img  = np.ones((240, 320, 3), np.uint8)


    counter = 0 
    kp2 = None
    kp1 = None
    x1=0
    y1=0
    x2=0
    y2=0
    def img_cb(self,message):
        # Initiate ORB detector
        orb = cv2.ORB_create()
        
        if self.counter < 2:
            self.cv2_img1 = bridge.imgmsg_to_cv2(message, "bgr8")
            #cv2.imwrite('saved_img.png', cv2_img)
            
            gray1 = cv2.cvtColor(self.cv2_img1,cv2.COLOR_BGR2GRAY)
            self.counter += 1

            # find the keypoints with ORB
            self.kp1 = orb.detect(gray1,None)

            
            # compute the descriptors with ORB
            self.kp1, self.des1 = orb.compute(gray1, self.kp1)
            
        elif self.counter == 2 :
            cv2_img2 = bridge.imgmsg_to_cv2(message, "bgr8")
            #cv2.imwrite('saved_img.png', cv2_img)
            
            gray2 = cv2.cvtColor(cv2_img2,cv2.COLOR_BGR2GRAY)
            
            # find the keypoints with ORB
            self.kp2 = orb.detect(gray2,None)
            
           
            # compute the descriptors with ORB
            self.kp2, des2 = orb.compute(gray2, self.kp2)
            self.counter += 1
            

        if self.counter == 3 and self.kp2 != None and self.kp1 != None:
            self.counter = 0

            
            # create BFMatcher object
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            # Match descriptors.
            if self.des1 is not None and des2 is not None:
                matches = bf.match(self.des1,des2)
                
                # Sort them in the order of their distance.
                matches = sorted(matches, key = lambda x:x.distance)
                
                # Draw first 10 matches.
                self.img = cv2.drawMatches(self.cv2_img1,self.kp1,cv2_img2,self.kp2,matches[:10],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

                list_kp1 = [self.kp1[mat.queryIdx].pt for mat in matches] 
                if len(list_kp1) > 0:
                    for x in range(len(list_kp1)):
                        self.x1 += list_kp1[x][0]
                        self.y1 += list_kp1[x][1]
                    self.x1 /= len(list_kp1)
                    self.y1 /= len(list_kp1) 
                list_kp2 = [self.kp2[mat.trainIdx].pt for mat in matches]
                if len(list_kp2) > 0:
                    for x in range(len(list_kp2)):
                        self.x2 += list_kp2[x][0]
                        self.y2 += list_kp2[x][1]
                    self.x2 /= len(list_kp2)
                    self.y2 /= len(list_kp2) 

            # concatanate image Horizontally
            #self.img = np.concatenate((self.cv2_img1, cv2_img2), axis=1)
            cv2.arrowedLine(self.img, (int(self.x2)+120,int(self.y2)),(int(self.x1)+120,int(self.y1)), (0,0,255), 5)
            

            if self.x1>self.x2 and (self.y2 -self.y1)<50:
                direction1 = "right"
            elif self.x1<self.x2 and (self.y2 -self.y1)<50:
                direction1 = "left"
            else:
                direction1 = "no turn"

            if self.y1>self.y2:
                direction2 = "down"
            else:
                direction2 = "up"
                
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.img, f"{direction1}", (10, 220), font, 1, (220, 120, 25), 2, cv2.FILLED)
            cv2.putText(self.img, f"{direction2}", (180, 220), font, 1, (220, 120, 25), 2, cv2.FILLED)   
        
        # concatanate image Horizontally
        cv2.imshow("image", self.img)
        cv2.waitKey(1)
          
def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()



