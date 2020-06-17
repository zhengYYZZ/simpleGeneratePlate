#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/10 15:54
# @Author  : zyx
# @Email   : zhengyixiang2@qq.com
# @File    : trnoise.py

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import cv2
import numpy as np
import copy
import random
from math import *


def rot(img, angel, shape, max_angel,point_dict):
    """
    仿射变换
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


def retRotPoint(pt, rotM):
    """
    经过透视变换后的坐标点
    :param pt: 原坐标点
    :param rotM: 透视变换矩阵(3x3)
    :return: 透视变换后的坐标
    """
    pt3D = np.array([[pt[0]], [pt[1]], [1]], dtype=float)
    ptM = rotM.dot(pt3D)
    ptx = ptM[0][0]
    pty = ptM[1][0]
    ptz = ptM[2][0]
    rotpt = (int(ptx / ptz), int(pty / ptz))
    return rotpt


def tfactor(img):
    """
    添加饱和度光照的噪声
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 0] = hsv[:, :, 0] * (0.8 + np.random.random() * 0.2)
    hsv[:, :, 1] = hsv[:, :, 1] * (0.3 + np.random.random() * 0.7)
    hsv[:, :, 2] = hsv[:, :, 2] * (0.2 + np.random.random() * 0.8)
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return img


def random_envirment(img, data_set):
    """
    添加自然环境的噪声
    """
    index = r(len(data_set))
    env = cv2.imread(data_set[index])

    env = cv2.resize(env, (img.shape[1], img.shape[0]))

    bak = (img == 0)
    bak = bak.astype(np.uint8) * 255
    inv = cv2.bitwise_and(bak, env)
    img = cv2.bitwise_or(inv, img)
    return img


def GenCh(f, val):
    """
    生成中文字符
    :param f: 字体
    :param val: 字符
    :return: 单个字符图片
    """
    img = Image.new("RGB", (45, 70), (255, 255, 255))  #"RGB"模式，(45,70)文件大小,(255,255,255)背景颜色
    draw = ImageDraw.Draw(img)
    draw.text((0, 3), val, (0, 0, 0), font=f)
    img = img.resize((23, 70))
    A = np.array(img)

    return A


def GenCh1(f, val):
    """
    生成英文字符和数字
    :param f: 字体
    :param val: 字符
    :return: 单个字符图片
    """
    img = Image.new("RGB", (23, 70), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 2), val.encode('utf-8').decode('utf-8'), (0, 0, 0), font=f)
    A = np.array(img)
    return A


def AddGauss(img, level):
    """
    添加高斯模糊
    """
    return cv2.blur(img, (level * 2 + 1, level * 2 + 1))


def r(val):
    """
    生成0~val范围的随机数
    """
    return int(np.random.random() * val)


def AddNoiseSingleChannel(single):
    """
    添加高斯噪声
    """
    diff = 255 - single.max()
    noise = np.random.normal(0, 1 + r(6), single.shape)
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    noise = diff * noise
    noise = noise.astype(np.uint8)
    dst = single + noise
    return dst


def addNoise(img, sdev=0.5, avg=10):
    """
    高斯噪声
    """
    img[:, :, 0] = AddNoiseSingleChannel(img[:, :, 0])
    img[:, :, 1] = AddNoiseSingleChannel(img[:, :, 1])
    img[:, :, 2] = AddNoiseSingleChannel(img[:, :, 2])
    return img


def edgeFill(img,pointG,fill_size=0):
    """
    图像边缘填充
    :param img:图像
    :param pointG: 坐标点
    :param fill_size: 填充边缘大小
    :return: 填充图像，坐标点
    """

    top_fill = fill_size + random.randint(0,10)
    bottom_fill = fill_size + random.randint(0,10)
    left_fill = fill_size + random.randint(0,10)
    right_fill = fill_size + random.randint(0,10)
    img = cv2.copyMakeBorder(img,top_fill,bottom_fill,left_fill,right_fill,cv2.BORDER_CONSTANT,value=(0,0,0))

    # 转换点坐标
    fill_pointG = []
    fill_point = []
    for pointx4 in pointG:
        for pt in pointx4:
            temp = (pt[0]+left_fill,pt[1]+top_fill)
            fill_point.append(temp)
        fill_pointG.append(fill_point.copy())
        fill_point.clear()

    return img,fill_pointG

def convert(size, box):
    """
    坐标转换为yolo可训练的txt坐标
    :param size:图像大小
    :param box:矩形坐标
    :return:yolo坐标
    """
    # print(f'box={box}')
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    # print(f'x={x},y={y},w={w},h={h}')
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    # print(f't2,,x={x},y={y},w={w},h={h}')
    return x, y, w, h


def drawpoint(imgoo, pointG, str):
    """
    画出坐标点
    :param imgoo:图像
    :param pointG:点坐标集
    :param str:
    :return:
    """
    img = copy.deepcopy(imgoo)
    for pp in pointG:
        for ptemp in pp:
            cv2.circle(img, ptemp, 3, (0, 255, 0), 2)
    cv2.imshow(str, img)
    cv2.waitKey(0)


def rectangle_vertex(pointA,pointB,pointC,pointD):
    """
    矩形框坐标
    :param pointA:左上角点
    :param pointB: 右上角点
    :param pointC: 左下角点
    :param pointD: 右下角点
    :return: 矩形框的左上角坐标和右下角坐标
    """
    left_point = (pointA[0]+pointC[0])/2
    top_point = (pointA[1]+pointB[1])/2
    right_point = (pointB[0]+pointD[0])/2
    bottom_point = (pointC[1]+pointD[1])/2
    point_A = (int(left_point),int(top_point))
    point_D = (int(right_point),int(bottom_point))
    roi_rect = [point_A,point_D]
    return roi_rect


def Roi_Correct(rect,img):
    """
    对矩形区修正，防止图片越界
    :param rect: 矩形框的左上角坐标和右下角坐标
    :param img: 图像
    :return:
    """
    if rect[0]<0:
        rect[0] = 0
    if rect[1]<0:
        rect[1] = 0
    if rect[1]<img.shape[1]:
        pass


def get_dict_key(dicts, value):
    '''
    根据dict值获取键
    :param dicts: dict
    :param value: dict->value
    :return: dict->key
    '''
    temp = None
    for k, v in dicts.items():
        if v == value:
            temp = k
    return temp


def save_classes(dicts, fileName):
    '''
    保存label.data
    :param dicts: 车牌字符dict
    :param fileName: 文件名
    :return: None
    '''
    with open(fileName, 'w') as f:
        for k, v in dicts.items():
            f.write(v + '\n')