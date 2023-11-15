import os

import kociemba
import time
import io
from PIL import Image

import cv2
import socket
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PIC_DIR = os.path.join(BASE_DIR, 'pic/')


def snap_full_pic(size):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    s.bind(("0.0.0.0", 9090))
    img_list = ["L", "F", "R", "B", "U", "D"]
    for i in range(2):
        data, _ = s.recvfrom(90000)
    bytes_stream = io.BytesIO(data)
    image = Image.open(bytes_stream)
    img = np.asarray(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）
    cv2.imwrite(f"{PIC_DIR}full_{size}.png", img)


def cam():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    s.bind(("0.0.0.0", 9090))
    img_list = ["R", "F", "L", "B", "U", "D"]
    index = 0
    while True:
        data, _ = s.recvfrom(90000)
        bytes_stream = io.BytesIO(data)
        image = Image.open(bytes_stream)
        img = np.asarray(image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # ESP32采集的是RGB格式，要转换为BGR（opencv的格式）
        cv2.imshow("ESP32 CAM-1", img)
        print("position:", img_list[index])
        key = cv2.waitKey(10)
        # print(key)
        if key & 0xFF == ord('n'):
            cv2.imwrite("{}_tmp.png".format(img_list[index]), img)
            index = index + 1
        elif key & 0xFF == ord('q'):
            break


# url = "rtsp://admin:admin@10.255.255.135:554/stream1"
# cap = cv2.VideoCapture(url)
# ret, frame = cap.read()
# while ret:
#     ret, frame = cap.read()
#     cv2.imshow("frame", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         cv2.imwrite("{}_tmp.png".format("D"), frame)
#         break
#     # time.sleep(0.1)
# cv2.destroyAllWindows()
# cap.release()

# img = cv2.imread('F_tmp.png')
# img = cv2.imread(PIC_DIR + 'R.png')
# roi = cv2.selectROI(windowName="original", img=img, showCrosshair=True, fromCenter=False)
# x, y, w, h = roi
# print(roi)
#
# # 显示ROI并保存图片
# if roi != (0, 0, 0, 0):
#     crop = img[y:y + h, x:x + w]
#     print('{}:{},{}:{}'.format(y, y + h, x, x + w))
#
# # 退出
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#############
# echo_size_img = cv2.imread('{}.png'.format(j))
# center_image = echo_size_img[x1:x2, y1:y2]
# # print(center_image)
# cv2.imwrite("{}_center.png".format(j), center_image)
# center_image = cv2.cvtColor(center_image, cv2.COLOR_BGR2RGB)
# center_image = center_image.reshape((center_image.shape[0] * center_image.shape[1], 3))
# # print(center_image)
# colors = np.array(center_image, dtype='int')
# kmeans = KMeans(n_clusters=1, n_init="auto")
# kmeans.fit(colors)
# color_r, color_g, color_b = np.array(kmeans.cluster_centers_, dtype='int')[0]
# # print(color_r, color_g, color_b)
# center_color_dic[i].append((color_r, color_g, color_b))
#        if ((clt.cluster_centers_[i][0] < 110) and (clt.cluster_centers_[i][1] < 105) and (
#                 clt.cluster_centers_[i][2] < 95)):  # 颜色为黑色，舍去

# img = cv2.imread(PIC_DIR + 'R.png')
# cropped_image = img[139:262, 132:263]
# # print(cropped_image)
# # cv2.imshow("new", cropped_image)
# # cv2.waitKey()
# image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
#
# rgb_data = image.reshape((-1, 3))
# # rgb_data2 = image.reshape((image.shape[0] * image.shape[1], 3))
# print(rgb_data)
# #
# # # # 对数据进行预处理和特征提取
# kmeans = KMeans(n_clusters=2)
# kmeans.fit(rgb_data)
# #
# # # 取出聚类中心，作为颜色识别结果
# colors = np.array(kmeans.cluster_centers_, dtype='int')
# print(colors)
# print(kmeans.labels_[0:500])

######


# img = cv2.imread('B.png')

# img = cv2.resize(img1, (0, 0), None, 0.4, 0.4)
# img = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
# frame_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
# lower = np.array([29, 86, 6])  # 下界,
# print(lower)
# upper = np.array([64, 255, 255])  # 上界
# hsv_mask = cv2.inRange(frame_hsv, lower, upper)
# cv2.imshow("origal", img)
# cv2.imshow("video", frame_hsv)
# cv2.imshow("mask", hsv_mask)n
# cv2.waitKey()
#
#

##########
if __name__ == '__main__':
    cam()
    # snap_full_pic()
