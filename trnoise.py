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
from math import *


def rot(img, angel, shape, max_angel):
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

    return dst


def rotRandrom(img, factor, size):
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
    return dst


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
    """生成中文字符

    f 字体
    val 字符
    return 单个字符图片
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

    f 字体
    val 字符
    return 单个字符图片
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