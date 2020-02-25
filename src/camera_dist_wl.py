import numpy as np
import cv2
from imageio import imread

def camera_dist(img):

    mtx = np.load('mtx_wl.npy')
    dist = np.load('dist_wl.npy')
    newcameramtx = np.load('distmtx_wl.npy')

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    return dst
