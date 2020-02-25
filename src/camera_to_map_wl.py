import numpy as np
import cv2
import glob
import math

def map_point(px, py):

    #mtx = camera parameter
    #cp = camera point
    #tp = tracker point
    #op = object point

    #camera parameterの読み込み
    mtx = np.load('distmtx_wl.npy')
    mtx_i = np.load('distmtx_i_wl.npy')

    #VIVE Trackerの画像上での位置
    origin_pixel = np.array([[446],[789],[1]])

    #VIVE　Trackerの画像上での位置をカメラ座標系に変換
    s = (mtx[0][0] * 1.7072 + mtx[1][1] * 1.7072)/2
    origin_cp = np.matmul(mtx_i,origin_pixel*s)/1000
    origin_cp = np.array([origin_cp[1],origin_cp[0],origin_cp[2]])
    #print(origin_cp)

    #並進ベクトル（VIVE座標系でのVIVE Trackerの座標）
    origin_tp = np.array([[-1.20],[1.00]])

    #画像座標系からVIVE座標系（地図座標系）に変換
    pixel = np.array([[px],[py],[1]])
    cp = np.matmul(mtx_i, pixel*s)/1000
    cp = np.array([cp[1],cp[0],cp[2]])
    #print(cp)
    op = cp - origin_cp
    op = np.array([op[0],op[1]])

    #回転行列によって軸の傾きを修正
    theta = -math.pi/360
    R = np.array([[math.cos(theta), -math.sin(theta)],[math.sin(theta), math.cos(theta)]])
    tp = np.matmul(R,op) + origin_tp

    return tp
