#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Copyright Niantic 2019. Patent Pending. All rights reserved.
#
# This software is licensed under the terms of the Monodepth2 licence
# which allows for non-commercial use only, the full terms of which are made
# available in the LICENSE file.

import os
import sys
import glob
import argparse
import numpy as np
import PIL.Image as pil
import matplotlib as mpl
import matplotlib.cm as cm
import cv2
import torch
from torchvision import transforms, datasets
import time
import networks
from layers import disp_to_depth
from utils import download_model_if_doesnt_exist
from evaluate_depth import STEREO_SCALE_FACTOR

# Instantiate CvBridge
bridge = CvBridge()

input_image_source = 1 # 0 --> Zed camera, 1 --> video camera

class MyNode(Node):
    def __init__(self):
        super().__init__("depth_node")
        self.get_logger().info("Node is started now")
        
        if input_image_source:
            self.create_timer(1/30,self.timer_call)
            self.vid = cv2.VideoCapture(0)
        else:
            self.create_subscription(Image,"/zed2/zed_node/rgb/image_rect_color",self.timer_call, rclpy.qos.qos_profile_sensor_data)

        self.obj_pub=self.create_publisher(Image,"depth_image",10)
        self.obj_pub1=self.create_publisher(Image,"original_image",10)
        
        """Function to predict for a single image or folder of images
        """
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

        download_model_if_doesnt_exist("mono+stereo_640x192")
        model_path = os.path.join("models", "mono+stereo_640x192")
        
        encoder_path = os.path.join(model_path, "encoder.pth")
        depth_decoder_path = os.path.join(model_path, "depth.pth")

        # LOADING PRETRAINED MODEL
        self.encoder = networks.ResnetEncoder(18, False)
        loaded_dict_enc = torch.load(encoder_path, map_location=self.device)

        # extract the height and width of image that this model was trained with
        self.feed_height = loaded_dict_enc['height']
        self.feed_width = loaded_dict_enc['width']
        filtered_dict_enc = {k: v for k, v in loaded_dict_enc.items() if k in self.encoder.state_dict()}
        self.encoder.load_state_dict(filtered_dict_enc)
        self.encoder.to(self.device)
        self.encoder.eval()

        self.depth_decoder = networks.DepthDecoder(
            num_ch_enc=self.encoder.num_ch_enc, scales=range(4))

        loaded_dict = torch.load(depth_decoder_path, map_location=self.device)
        self.depth_decoder.load_state_dict(loaded_dict)

        self.depth_decoder.to(self.device)
        self.depth_decoder.eval()
        


    def timer_call(self,message=None):
        t = time.time()
        if input_image_source:
            ret, cv2_img = self.vid.read()
        else:
            cv2_img = bridge.imgmsg_to_cv2(message, "bgr8")
        
        with torch.no_grad():
            # Load image and preprocess
            input_image = cv2_img
            original_width = input_image.shape[1]
            original_height = input_image.shape[0]
            input_image = cv2.resize(input_image,(self.feed_width, self.feed_height))
            input_image = transforms.ToTensor()(input_image).unsqueeze(0)

            # PREDICTION
            input_image = input_image.to(self.device)
            features = self.encoder(input_image)
            outputs = self.depth_decoder(features)

            disp = outputs[("disp", 0)]
            disp_resized = torch.nn.functional.interpolate(
                disp, (original_height, original_width), mode="bilinear", align_corners=False)

            # Saving numpy file
            output_name = os.path.splitext(os.path.basename("out.png"))[0]
            scaled_disp, depth = disp_to_depth(disp, 0.1, 100)
            
            name_dest_npy = os.path.join("", "{}_depth.npy".format(output_name))
            metric_depth = STEREO_SCALE_FACTOR * depth.cpu().numpy()
            np.save(name_dest_npy, metric_depth)
             
            # Saving colormapped depth image
            disp_resized_np = disp_resized.squeeze().cpu().numpy()
            vmax = np.percentile(disp_resized_np, 95)
            normalizer = mpl.colors.Normalize(vmin=disp_resized_np.min(), vmax=vmax)
            mapper = cm.ScalarMappable(norm=normalizer, cmap='magma')
            colormapped_im = (mapper.to_rgba(disp_resized_np)[:, :, :3] * 255).astype(np.uint8)
            im = pil.fromarray(colormapped_im)

            name_dest_im = os.path.join("", "{}_disp.jpeg".format(output_name))
            im.save(name_dest_im)
            

        msg=Image()
        msg.header.frame_id = "depth_frame"
        msg.header.stamp=Node.get_clock(self).now().to_msg()
        metric_depth=np.asarray(metric_depth)
        metric_depth=np.reshape(metric_depth,(192,640))
        metric_depth=metric_depth/4
        metric_depth=cv2.resize(metric_depth,None,fx=1,fy=1.875)
        metric_depth=bridge.cv2_to_imgmsg(metric_depth)
        msg=metric_depth
        
        msg1=Image()
        msg1.header.frame_id = "original_image_frame"
        msg1.header.stamp=Node.get_clock(self).now().to_msg()
        msg1=bridge.cv2_to_imgmsg(cv2_img)

        self.obj_pub.publish(msg)
        self.obj_pub1.publish(msg1)
        
        print(f"fps: {1/(time.time()-t)}")

def main(args=None):
    rclpy.init(args=args)
    node=MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()
