import kociemba
import time
import io
from PIL import Image
import os
from pathlib import Path
import cv2
import socket
import numpy as np
import webcolors
from sklearn.cluster import KMeans

img_list = ["U", "R", "F", "D", "L", "B"]
title = "HSV阈值调整器"
imgHSV_list = {}
for i in img_list:
    pic = '{}.png'.format(i)
    tmp_img = cv2.imread(pic)
    cv2.resize(tmp_img, None, fx=2, fy=2)
    cv2.imshow(pic, tmp_img)
    imgHSV_list[i] = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2HSV)


# 回调函数必须要写
def empty(i):
    # 提取滑动条的数值 共6个
    hue_min = cv2.getTrackbarPos("Hue Min", title)
    hue_max = cv2.getTrackbarPos("Hue Max", title)
    sat_min = cv2.getTrackbarPos("Sat Min", title)
    sat_max = cv2.getTrackbarPos("Sat Max", title)
    val_min = cv2.getTrackbarPos("Val Min", title)
    val_max = cv2.getTrackbarPos("Val Max", title)
    # 颜色空间阈值
    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])
    # 根据颜色空间阈值生成掩膜
    for j in img_list:
        imgMASK_tmp = cv2.inRange(imgHSV_list[j], lower, upper)
        cv2.imshow(j + ".png " + "Mask", imgMASK_tmp)

    print('{}: low:{} upper:{}'.format(pic, lower, upper))


def get_hsv():
    # 参数(‘窗口标题’,默认参数)
    cv2.namedWindow(title)
    # 设置窗口大小

    # 第一个参数时滑动条的名字，
    # 第二个参数是滑动条被放置的窗口的名字，
    # 第三个参数是滑动条默认值，
    # 第四个参数时滑动条的最大值，
    # 第五个参数时回调函数，每次滑动都会调用回调函数。
    cv2.createTrackbar("Hue Min", title, 0, 179, empty)
    cv2.createTrackbar("Hue Max", title, 179, 179, empty)
    cv2.createTrackbar("Sat Min", title, 0, 255, empty)
    cv2.createTrackbar("Sat Max", title, 255, 255, empty)
    cv2.createTrackbar("Val Min", title, 0, 255, empty)
    cv2.createTrackbar("Val Max", title, 255, 255, empty)
    cv2.resizeWindow(title, 1640, 1640)


# cv2.imshow("HSV", imgHSV)
get_hsv()
# 调用函数
empty(0)

while True:
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    # 按任意键关闭
