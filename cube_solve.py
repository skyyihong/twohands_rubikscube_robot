import kociemba
import time
import io
import os
from PIL import Image
import cv2
from sklearn.cluster import KMeans
import numpy as np
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PIC_DIR = os.path.join(BASE_DIR, 'pic/')

# 存储6个面中心块的RGB值
center_color_dic = {
    "U": [],
    "R": [],
    "F": [],
    "D": [],
    "L": [],
    "B": []
}

# 自定义6个面的处理顺序
img_list = ["U", "R", "F", "D", "L", "B"]

#
final_solve_str = []

total_execute_list = []


def cut_each_cube_size():
    """
    从摄像头拍到的图片切割去除图片周边内网，图片只存放魔方6个面的，保存为如F.png图片
    """
    cut_img_map = {
        "R": (205, 498, 255, 551),
        "F": (205, 502, 258, 548),
        "L": (192, 507, 242, 546),
        "B": (194, 502, 260, 562),
        "U": (219, 508, 261, 556),
        "D": (210, 504, 261, 550),
    }

    for i in cut_img_map:
        # i = PIC_DIR + i
        img = cv2.imread('{}full_size_{}.png'.format(PIC_DIR, i))
        cropped_image = img[cut_img_map[i][0]:cut_img_map[i][1], cut_img_map[i][2]:cut_img_map[i][3]]
        cv2.imwrite("{}{}.png".format(PIC_DIR, i), cropped_image)


# 定义每个面和每个面9个方块的色块取值的区域
each_facelet_color_position = {
    "U": ([24, 55, 24, 58, 0], [28, 57, 129, 162, 0], [26, 55, 225, 256, 0], [124, 153, 25, 57, 0],
          [128, 158, 130, 161, 0], [123, 152, 225, 256, 0], [226, 256, 27, 60, 0], [213, 236, 131, 164, 0],
          [218, 253, 226, 266, 0]),
    "R": ([35, 67, 27, 61, 0], [23, 60, 121, 159, 0], [24, 63, 223, 264, 0], [123, 176, 56, 80, 1],
          [129, 163, 131, 167, 0], [128, 166, 224, 269, 0], [229, 265, 29, 71, 0], [214, 245, 179, 184, 1],
          [222, 260, 229, 266, 0]),
    "F": ([26, 57, 22, 56, 0], [30, 65, 118, 156, 0], [38, 72, 221, 255, 0], [122, 169, 66, 73, 0],
          [134, 169, 118, 156, 0], [137, 167, 219, 255, 0], [231, 267, 17, 55, 0], [232, 266, 119, 154, 0],
          [234, 268, 219, 257, 0]),
    "D": ([30, 62, 23, 58, 0], [29, 62, 120, 156, 0], [28, 62, 220, 258, 0], [130, 162, 19, 55, 0],
          [130, 160, 124, 155, 0], [125, 156, 224, 260, 0], [224, 254, 28, 59, 0], [218, 245, 127, 159, 0],
          [227, 253, 226, 255, 0]),
    "L": ([40, 72, 31, 62, 0], [41, 75, 130, 165, 0], [36, 70, 232, 268, 0], [128, 166, 78, 86, 0],
          [141, 170, 138, 167, 0], [139, 171, 237, 271, 0], [238, 275, 27, 67, 0], [224, 255, 182, 188, 1],
          [237, 271, 236, 269, 0]),
    "B": ([36, 69, 28, 63, 0], [38, 71, 130, 165, 0], [39, 70, 227, 261, 0], [127, 177, 53, 73, 0],
          [133, 165, 132, 164, 0], [139, 173, 229, 266, 0], [234, 265, 28, 59, 0], [238, 270, 128, 164, 0],
          [240, 273, 228, 261, 0])
}


# 重写获取中心点颜色的方法
def handle_center_color():
    for i in img_list:
        j = PIC_DIR + i
        x1, x2, y1, y2, flag = each_facelet_color_position[i][4]
        echo_size_img = cv2.imread('{}.png'.format(j))
        center_image = echo_size_img[x1:x2, y1:y2]
        k = PIC_DIR + "center_" + i
        cv2.imwrite("{}.png".format(k), center_image)
        center_image = cv2.cvtColor(center_image, cv2.COLOR_BGR2RGB)
        center_image_reshape = center_image.reshape((-1, 3))
        colors = np.array(center_image_reshape, dtype='int')
        kmeans = KMeans(n_clusters=1, n_init="auto")
        kmeans.fit(colors)
        color_r, color_g, color_b = np.array(kmeans.cluster_centers_, dtype='int')[0]
        center_color_dic[i].append((color_r, color_g, color_b))
    print(center_color_dic)


def lm_center_color_dic():
    """
    将所有设别到颜色的RGB放到队列里面，后续设别时对同颜色队列里的数值做一次平均值后，再做为中心色块的颜色值
    """
    global center_color_dic
    tmp_center_color_dic = {}
    for i in center_color_dic:
        colors = np.array(center_color_dic[i], dtype='int')
        kmeans = KMeans(n_clusters=1, n_init="auto")
        kmeans.fit(colors)
        color_r, color_g, color_b = np.array(kmeans.cluster_centers_, dtype='int')[0]
        tmp_center_color_dic[i] = (color_r, color_g, color_b)
    return tmp_center_color_dic


def match_center_size(color):
    """
    识别色块与6个面的那个中心块颜色最接近
    """
    new_center_color_dic = lm_center_color_dic()
    color_size = [i for i in new_center_color_dic]  # 把key拿出来
    color_list = [new_center_color_dic[i] for i in new_center_color_dic]  # 把item值拿出来
    tmp_color = color
    color_list.append(color)
    colors = np.array(color_list, dtype='int')
    kmeans = KMeans(n_clusters=6, n_init="auto")
    kmeans.fit(colors)
    sort_list = [j for j in kmeans.labels_]
    order_num = sort_list.index(sort_list[-1])
    if order_num == 6:
        print(colors, sort_list, sort_list.index(sort_list[-1]))
        return None
    else:
        center_color_dic[color_size[order_num]].append(tmp_color)
        return color_size[order_num]


def handle_echo_size_str():
    cube_str = []
    for i in img_list:
        j = PIC_DIR + i
        echo_size_img = cv2.imread('{}.png'.format(j))
        for index in range(0, 9):
            x1, x2, y1, y2, flag = each_facelet_color_position[i][index]
            block_img = echo_size_img[x1:x2, y1:y2]
            k = PIC_DIR + "block_" + i + "_" + str(index)
            cv2.imwrite("{}.png".format(k), block_img)
            block_img = cv2.cvtColor(block_img, cv2.COLOR_BGR2RGB)
            block_img_reshape = block_img.reshape((-1, 3))
            colors = np.array(block_img_reshape, dtype='int')
            if flag:
                kmeans = KMeans(n_clusters=2, n_init="auto")
                kmeans.fit(colors)
                print("-----------------------")
                print(np.array(kmeans.cluster_centers_, dtype='int'))
                avg_color_r1, avg_color_g1, avg_color_b1 = np.array(kmeans.cluster_centers_, dtype='int')[0]
                avg_color_r2, avg_color_g2, avg_color_b2 = np.array(kmeans.cluster_centers_, dtype='int')[1]
                if avg_color_r1 + avg_color_g1 + avg_color_b1 > avg_color_r2 + avg_color_g2 + avg_color_b2:
                    avg_color_r, avg_color_g, avg_color_b = avg_color_r1, avg_color_g1, avg_color_b1
                else:
                    avg_color_r, avg_color_g, avg_color_b = avg_color_r2, avg_color_g2, avg_color_b2
            else:
                kmeans = KMeans(n_clusters=1, n_init="auto")
                kmeans.fit(colors)
                avg_color_r, avg_color_g, avg_color_b = np.array(kmeans.cluster_centers_, dtype='int')[0]
            block_size_str = match_center_size((avg_color_r, avg_color_g, avg_color_b))
            if block_size_str is None:
                error_info = "size:{}-{},({},{},{})".format(i, index, avg_color_r, avg_color_g,
                                                            avg_color_b)
                print(cube_str)
                raise Exception(f"颜色识别错误，位置为 {error_info}")
            cube_str.append(block_size_str)
    return cube_str


def handle_solve_str(solve_content):
    """
        kociemba函数获取到内容，转化为('R', -90)这样的表现形式
    """
    solve_str_list = []
    tmp = solve_content.split(" ")
    for i in tmp:
        turn_degree = 90
        if len(i) == 1:
            turn_degree = 90 * 1
        elif "'" in i:
            turn_degree = turn_degree * -1
        else:
            turn_degree = 180
        solve_str_list.append((i[0], turn_degree))
    return solve_str_list


def get_total_execute_list():
    """
    获取最终上位机的执行逻辑脚本数据
    """
    global final_solve_str
    total_execute_list = []
    F_L_B_R = ["L", "B", "R", "F"]
    U_D = ["U", "D"]

    def get_rotate_degree(size):
        """
            实时获取各个面旋转后的到各个面的状态数据
        """
        nonlocal F_L_B_R, U_D

        if size in F_L_B_R:
            for i, j in enumerate(F_L_B_R):
                # print(i, j)
                if j == size:
                    if i == 0:
                        return 2, 0
                    end = F_L_B_R[0:i]
                    start = F_L_B_R[i:]
                    F_L_B_R = start + end
                    tmp_degree = -90 if 90 * i == 270 else 90 * i
                    return 2, tmp_degree
        else:
            # 上下
            if size == U_D[0]:
                tmp_u = U_D[0]
                tmp_l = F_L_B_R[1]
                U_D[0] = U_D[1]
                U_D[1] = tmp_u
                F_L_B_R[1] = F_L_B_R[3]
                F_L_B_R[3] = tmp_l
                return 1, 180
            return 1, 0

    for direct, degree in final_solve_str:
        ret = get_rotate_degree(direct)
        if direct in F_L_B_R:
            total_execute_list.append([ret, (1, degree)])
        else:
            total_execute_list.append([ret, (2, degree)])
    return total_execute_list


def change_degree(current, change):
    """
    根据当前的角度和将要选择的角度，返回实际旋转角度,防止电线缠绕
    """
    total = current + change
    if change == 270:
        # 转270只是一个标示，暗示手柄松口时，正反转90度结果为一致
        change = 90
        total = current + change
        if total >= 270:
            return current - 90, 90 * -1
    elif change == 180:
        if total >= 360:
            return current - change, change * -1
    return current + change, change


def upper_exec_str(execute_list):
    """
    获取最终上位机的执行物理脚本数据
    """
    # 手柄0为关，1为开
    hand_status = {
        1: 0,
        2: 0
    }

    # 水平状态为180或0度
    robot_degree = {
        1: 180,
        2: 180
    }
    tmp_list = []
    for i, data in enumerate(execute_list):
        group1, group2 = data
        # 对应选择的手柄，其另外一只手柄需要松口
        servo_group1, degree_group1 = group1
        if degree_group1 != 0:
            num_group1 = 1 if servo_group1 == 2 else 2
            if hand_status[num_group1] != 1:
                if hand_status[servo_group1] != 0:
                    # 松口手柄时，判断另一只手柄是否是加紧状态
                    tmp_list.append(("hand" + str(servo_group1), 0))
                    hand_status[servo_group1] = 0
                tmp_list.append(("hand" + str(num_group1), 1))
                hand_status[num_group1] = 1

            if robot_degree[num_group1] % 180 != 0:
                current_degree, ret_degree = change_degree(robot_degree[num_group1], 270)
                tmp_list.append(("servo" + str(num_group1), ret_degree))
                robot_degree[num_group1] = current_degree

            # robot1 转动
            current_degree, ret_degree = change_degree(robot_degree[servo_group1], degree_group1)
            tmp_list.append(("servo" + str(servo_group1), ret_degree))
            robot_degree[servo_group1] = current_degree

        print("1", hand_status, robot_degree, end="--")
        print(" ")
        # 对应选择的手柄，其另外一只手柄需要紧闭
        servo_group2, degree_group2 = group2
        num_group2 = 1 if servo_group2 == 2 else 2

        # 旋转的另一只手柄需要在0或180度的位置
        if robot_degree[num_group2] % 180 != 0:
            if hand_status[num_group2] != 1:
                if hand_status[servo_group2] != 0:
                    tmp_list.append(("hand" + str(servo_group2), 0))
                    hand_status[servo_group2] = 0
                tmp_list.append(("hand" + str(num_group2), 1))
                hand_status[num_group2] = 1
            current_degree, ret_degree = change_degree(robot_degree[num_group2], 270)
            tmp_list.append(("servo" + str(num_group2), ret_degree))
            robot_degree[num_group2] = current_degree
        # 两只手柄都关闭
        for n in hand_status:
            if hand_status[n] == 1:
                tmp_list.append(("hand" + str(n), 0))
                hand_status[n] = 0
        current_degree, ret_degree = change_degree(robot_degree[servo_group2], degree_group2)
        tmp_list.append(("servo" + str(servo_group2), ret_degree))
        robot_degree[servo_group2] = current_degree
    return tmp_list


def cube_step():
    global final_solve_str
    cut_each_cube_size()
    handle_center_color()
    ret1 = handle_echo_size_str()
    print("".join(ret1))
    solve = kociemba.solve("".join(ret1))
    solve = kociemba.solve("DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD")
    # solve = kociemba.solve("RBURURLDDBDRBRLLBUUBLUFRDDUFFBLDULFFBUFULFDFRBLDDBLRRF")
    # 'UUFRUFDFR DRLLRBULB RDFBFDBUF URRLDBBBD FDBFLUUUL DFLDBLLRR'
    # RBURURLDD BDRBRLLBU UBLUFRDDU FFBLDULFF BUFULFDDR BLDDBLRRF
    # RBURURLDD BDRBRLLBU UBLUFRDDU FFBLDULFF BUFULFDDR BLDDBLRRF
    # RBURURLDD BDRBRLLUU UBLUFRDDU FFBLDULFF BUFULFDFR BLDDBLRRF
    # RBURURLDD BDRBRLLBU UBLUFRDDU FFBLDULFF BUFULFDUR BLDDBLRRF
    # RBURURLDD BDRBRLLBU UBLUFRDDU FFBLDULFF BUFULFDUR BLDDBLRRF
    final_solve_str = handle_solve_str(solve)
    final_execute_list = get_total_execute_list()
    result = upper_exec_str(final_execute_list)
    return {"result": result}


if __name__ == '__main__':
    ret = cube_step()
    print(len(ret["result"]), ret)
