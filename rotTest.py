import cv2
import numpy as np
from math import *


def rotRandrom(img, factor, size,point_dict):
    """
    添加透视畸变

    img 输入图像
    factor 畸变的参数
    size 为图片的目标尺寸
    """
    shape = size
    pts1 = np.float32([[0, 0], [0, shape[0]], [shape[1], 0], [shape[1], shape[0]]])
    pts2 = np.float32([[r(factor), r(factor)], [r(factor), shape[0] - r(factor)], [shape[1] - r(factor), r(factor)],
                       [shape[1] - r(factor), shape[0] - r(factor)]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, size)
    rot_pointG = []
    rot_point = []
    for pointx4 in point_dict:
        for pt in pointx4:
            rot_p = retRotPoint(pt,M)
            rot_point.append(rot_p)
        rot_pointG.append(rot_point.copy())
        rot_point.clear()
    return dst, rot_pointG


def rot(img, angel, shape, max_angel,point_dict):
    """
    使图像轻微的畸变
    """
    size_o = [shape[1], shape[0]]

    size = (shape[1] + int(shape[0] * cos((float(max_angel) / 180) * 3.14)), shape[0])

    interval = abs(int(sin((float(angel) / 180) * 3.14) * shape[0]))

    pts1 = np.float32([[0, 0], [0, size_o[1]], [size_o[0], 0], [size_o[0], size_o[1]]])
    if (angel > 0):

        pts2 = np.float32([[interval, 0], [0, size[1]], [size[0], 0], [size[0] - interval, size_o[1]]])
    else:
        pts2 = np.float32([[0, 0], [interval, size[1]], [size[0] - interval, 0], [size[0], size_o[1]]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(img, M, size)

    # 转换坐标点
    rot_pointG = []
    rot_point = []
    for pointx4 in point_dict:

        for pt in pointx4:
            rot_p = retRotPoint(pt,M)
            rot_point.append(rot_p)
        rot_pointG.append(rot_point.copy())
        rot_point.clear()

    return dst, rot_pointG


def r(val):
    """
    生成0~val范围的随机数
    """
    return int(np.random.random() * val)


def retRotPoint(pt, rotM):
    """
    经过透视变换后的坐标点
    pt:原坐标点
    rotM:透视变换矩阵(3x3)
    """
    pt3D = np.array([[pt[0]], [pt[1]], [1]], dtype=float)
    ptM = rotM.dot(pt3D)
    ptx = ptM[0][0]
    pty = ptM[1][0]
    ptz = ptM[2][0]
    rotpt = (int(ptx / ptz), int(pty / ptz))
    return rotpt


p11 = [(43, 12),(81, 12),(43, 65),(81, 65)]
p22 = [(149, 11),(149,60),(156, 65),(180, 65)]
pdict = [[(43,12)]]
p1 = (43, 12)
p2 = (81, 12)
p3 = (43, 65)
p4 = (81, 65)
img00 = cv2.imread("plate/00.jpg")
print(img00.shape)
img01 = img00.copy()

for pp in pdict:
    for ptemp in pp:
        cv2.circle(img01, ptemp, 3, (255, 255, 255), 2)

cv2.imshow("00", img01)
img00,pointG = rotRandrom(img00, 10, (img00.shape[1], img00.shape[0]),pdict)
# img00, pointG = rot(img00, r(60) - 30, img00.shape, 30,pdict)
# pt1 = retRotPoint(p1, rotM)
# pt2 = retRotPoint(p2, rotM)
# pt3 = retRotPoint(p3, rotM)
# pt4 = retRotPoint(p4, rotM)
# print(pointG)
for pp in pointG:
    for ptemp in pp:
        cv2.circle(img00, ptemp, 3, (255, 255, 255), 2)

# cv2.circle(img00, pt2, 3, (255, 255, 255), 2)
# cv2.circle(img00, pt3, 3, (255, 255, 255), 2)
# cv2.circle(img00, pt4, 3, (255, 255, 255), 2)
cv2.imshow("01", img00)
cv2.waitKey(0)
