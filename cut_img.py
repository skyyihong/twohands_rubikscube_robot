import os
import cv2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PIC_DIR = os.path.join(BASE_DIR, 'pic/')

img_list = ["R", "F", "L", "B", "U", "D"]


def cut_img():
    img = cv2.imread(PIC_DIR + "full_size_" + 'D.png')
    roi = cv2.selectROI(windowName="original", img=img, showCrosshair=True, fromCenter=False)
    x, y, w, h = roi
    print(roi)

    # 显示ROI并保存图片
    if roi != (0, 0, 0, 0):
        crop = img[y:y + h, x:x + w]
        print('{}:{},{}:{}'.format(y, y + h, x, x + w))

    # 退出
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cut_block_img():
    img = cv2.imread(PIC_DIR + "full_size_" + 'D.png')
    roi = cv2.selectROI(windowName="original", img=img, showCrosshair=True, fromCenter=False)
    x, y, w, h = roi
    print(roi)

    # 显示ROI并保存图片
    if roi != (0, 0, 0, 0):
        crop = img[y:y + h, x:x + w]
        print('{}:{},{}:{}'.format(y, y + h, x, x + w))

    # 退出
    cv2.waitKey(0)
    cv2.destroyAllWindows()


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


def center_color():
    for i in img_list:
        img = cv2.imread(PIC_DIR + f'{i}.png')
        roi = cv2.selectROI(windowName=i, img=img, showCrosshair=True, fromCenter=False)
        x, y, w, h = roi
        print(roi)

        # 显示ROI并保存图片
        if roi != (0, 0, 0, 0):
            crop = img[y:y + h, x:x + w]
            print('{}:{},{}:{}'.format(y, y + h, x, x + w))

        # 退出
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def each_block_color():
    for i in ["L"]:
        for j in range(8):
            img = cv2.imread(PIC_DIR + f'{i}.png')
            roi = cv2.selectROI(windowName=i, img=img, showCrosshair=True, fromCenter=False)
            x, y, w, h = roi
            print(roi)

            # 显示ROI并保存图片
            if roi != (0, 0, 0, 0):
                crop = img[y:y + h, x:x + w]
                print('{}:{},{}:{}'.format(y, y + h, x, x + w))

            # 退出
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    # cut_each_cube_size()
    # cut_img()

    # center_color()
    each_block_color()
