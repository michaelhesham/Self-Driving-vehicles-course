import numpy as np
import cv2

X = np.load('assets/carkyo1_depth.npy', mmap_mode='r')

y = cv2.imread('assets/carkyo1_disp.jpeg')
x = np.reshape(X,(192,640)) 
print(X)
print(x)
print(y.shape)
