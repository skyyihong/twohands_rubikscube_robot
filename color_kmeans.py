import kociemba
import time
import io
from PIL import Image
import os
from pathlib import Path
import cv2
import socket
import numpy as np
from sklearn.cluster import KMeans

center_color = {'U': (87.02, 226.98, 128.06), 'R': (219.96, 96.96, 126.5), 'F': (221.14, 232.86, 157.94),
                'D': (18.68, 136.22, 238.96), 'L': (255.0, 180.0, 162.0), 'B': (216.38, 242.5, 237.24)}

test_color = (33.82, 70.54, 216.07)
color_list = [center_color[i] for i in center_color]
color_list.append(test_color)
print(color_list)
colors = np.array(color_list, dtype='int')
kmeans = KMeans(n_clusters=6, n_init="auto")
kmeans.fit(colors)
print(kmeans.labels_)
#
# # 对数据进行预处理和特征提取

# #
# # # 取出聚类中心，作为颜色识别结果
# colors = np.array(kmeans.cluster_centers_, dtype='int')
# print(colors)
# print(kmeans.labels_[0:500])

# print(np.array((10, 20, 30), dtype='int'))
