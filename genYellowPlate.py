#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/10 20:22
# @Author  : zyx
# @Email   : zhengyixiang2@qq.com
# @File    : genYellowPlate.py

from trnoise import *
import os

chars = {0: "京", 1: "沪", 2: "津", 3: "渝", 4: "冀", 5: "晋", 6: "蒙", 7: "辽", 8: "吉", 9: "黑", 10: "苏",
         11: "浙", 12: "皖", 13: "闽", 14: "赣", 15: "鲁", 16: "豫", 17: "鄂", 18: "湘", 19: "粤", 20: "桂",
         21: "琼", 22: "川", 23: "贵", 24: "云", 25: "藏", 26: "陕", 27: "甘", 28: "青", 29: "宁", 30: "新",
         31: "0", 32: "1", 33: "2", 34: "3", 35: "4", 36: "5", 37: "6", 38: "7", 39: "8", 40: "9",
         41: "A", 42: "B", 43: "C", 44: "D", 45: "E", 46: "F", 47: "G", 48: "H", 49: "J", 50: "K",
         51: "L", 52: "M", 53: "N", 54: "P", 55: "Q", 56: "R", 57: "S", 58: "T", 59: "U", 60: "V",
         61: "W", 62: "X", 63: "Y", 64: "Z"}


def genPlateString(pos, val):
    """
    生成车牌号码string
    """
    plateStr = ""
    box = [0, 0, 0, 0, 0, 0, 0]
    if pos != -1:
        box[pos] = 1
    for unit, cpos in zip(box, range(len(box))):
        if unit == 1:
            plateStr += val
        else:
            if cpos == 0:
                plateStr += chars[r(31)]
            elif cpos == 1:
                plateStr += chars[41 + r(24)]
            else:
                plateStr += chars[31 + r(34)]

    return plateStr


class GenYellowPlates:
    def __init__(self, fontCh, fontEng, NoPlates):
        self.fontC = ImageFont.truetype(fontCh, 43, 0)  # 中文字体
        self.fontE = ImageFont.truetype(fontEng, 60, 0)  # 英文字体
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))  # 空白图片
        self.bg = cv2.resize(cv2.imread("./images/y1.bmp"), (226, 70))  # 车牌背景图片
        self.smu = cv2.imread("./images/smu2.jpg")
        self.noplates_path = []
        # 将NoPlates目录下的图片加入列表noplates_path
        for parent, parent_folder, filenames in os.walk(NoPlates):
            for filename in filenames:
                path = parent + "/" + filename
                self.noplates_path.append(path)

    def draw_string(self, text):
        """
        画出车牌字符
        text 车牌号码str
        return img
        """
        offset = 2
        # 调整字符间的间距
        self.img[0:70, offset + 8:offset + 8 + 23] = GenCh(self.fontC, text[0])
        self.img[0:70, offset + 8 + 23 + 6:offset + 8 + 23 + 6 + 23] = GenCh1(self.fontE, text[1])
        for i in range(5):
            base = offset + 8 + 23 + 6 + 23 + 17 + i * 23 + i * 6
            self.img[0:70, base: base + 23] = GenCh1(self.fontE, text[i + 2])
        # cv2.imshow("img",self.img)
        # cv2.waitKey(0)

        return self.img

    def getPlateImg(self, text):
        """
        生成车牌图片

        text 车牌号码str
        """
        if len(text) == 7:
            fg = self.draw_string(text.encode('utf-8').decode(encoding="utf-8"))
            # # 白色字体
            # fg = cv2.bitwise_not(fg)
            # plate_img = cv2.bitwise_or(fg, self.bg)  # 加入背景
            # 黑色字体
            cv2.imshow("1",fg)
            plate_img = cv2.bitwise_and(fg,self.bg)

            # 形态学变
            plate_img = rot(plate_img, r(60) - 30, plate_img.shape, 30)
            # plate_img = rotRandrom(plate_img, 10, (plate_img.shape[1], plate_img.shape[0]))
            # plate_img = tfactor(plate_img)
            # plate_img = random_envirment(plate_img, self.noplates_path)
            # plate_img = AddGauss(plate_img, 1 + r(4))
            # plate_img = addNoise(plate_img)
            # cv2.imshow("2",plate_img)
            # cv2.waitKey(0)
            return plate_img

    def genBatch(self, batchSize, outputPath, size):
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        for i in range(batchSize):
            plateStr = genPlateString(-1, -1)
            img = self.getPlateImg(plateStr)
            img = cv2.resize(img, size)
            # cv2.imwrite(outputPath + "/" + str(plateStr) + ".jpg", img)
            # cv2.imencode(".jpg", img)[1].tofile(outputPath + "/" + str(plateStr) + ".jpg")
            cv2.imwrite(outputPath + "/" + str(i).zfill(2) + ".jpg", img)


def test():
    G = GenYellowPlates("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
    G.genBatch(1, "./plate", (272, 72))


if __name__ == '__main__':
    test()