#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/4 上午10:56
# @Author  : zyx
# @Email   : zhengyixiang2@qq.com

from trnoise_black import *
import os
from tqdm import tqdm
from carPlateChars import *

"""
生成白色警用车牌
"""


class GenWhitePolice:
    def __init__(self, fontCh, fontEng, NoPlates):
        self.fontC = ImageFont.truetype(fontCh, 43, 0)  # 中文字体
        self.fontE = ImageFont.truetype(fontEng, 58, 0)  # 英文字体
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))  # 空白图片
        self.bg = cv2.resize(cv2.imread("./images/new/white_140.PNG"), (226, 70))  # 车牌背景图片
        self.smu = cv2.imread("./images/smu2.jpg")
        self.noplates_path = []
        self.pointG = []
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
        # 第一个汉字
        self.img[0:70, offset + 8:offset + 8 + 23] = GenCh(self.fontC, text[0])
        self.pointG.append([(offset + 8 - 1, 8), (offset + 8 + 23 + 1, 8),
                            (offset + 8 - 1, 62), (offset + 8 + 23 + 1, 62)])  # p1(x,y),p2(x,y)...
        # 第二个字符
        self.img[0:70, offset + 8 + 23 + 6 + 13:offset + 8 + 23 + 6 + 23 + 13] = GenCh1(self.fontE, text[1])
        self.pointG.append([(offset + 8 + 23 + 6 + 13 - 1, 8), (offset + 8 + 23 + 6 + 23 + 13 + 1, 8),
                            (offset + 8 + 23 + 6 + 13 - 1, 62), (offset + 8 + 23 + 6 + 23 + 13 + 1, 62)])
        base = offset + 8 + 23 + 6 + 13
        add_space = 23 + 6
        self.img[0:70, base + add_space:base + 23 + add_space] = GenCh1(self.fontE, text[2])
        self.pointG.append([(base + add_space - 1, 8), (base + 23 + add_space + 1, 8),
                            (base + add_space - 1, 62), (base + 23 + add_space + 1, 62)])
        base = base + add_space
        self.img[0:70, base + add_space:base + 23 + add_space] = GenCh1(self.fontE, text[3])
        self.pointG.append([(base + add_space - 1, 8), (base + 23 + add_space + 1, 8),
                            (base + add_space - 1, 62), (base + 23 + add_space + 1, 62)])
        base = base + add_space
        self.img[0:70, base + add_space:base + 23 + add_space] = GenCh1(self.fontE, text[4])
        self.pointG.append([(base + add_space - 1, 8), (base + 23 + add_space + 1, 8),
                            (base + add_space - 1, 62), (base + 23 + add_space + 1, 62)])
        base = base + add_space
        self.img[0:70, base + add_space:base + 23 + add_space] = GenCh1(self.fontE, text[5])
        self.pointG.append([(base + add_space - 1, 8), (base + 23 + add_space + 1, 8),
                            (base + add_space - 1, 62), (base + 23 + add_space + 1, 62)])
        base = base + add_space
        self.img[0:70, base + add_space:base + 23 + add_space] = GenCh_red(self.fontC, text[6])
        self.pointG.append([(base + add_space - 1, 8), (base + 23 + add_space + 1, 8),
                            (base + add_space - 1, 62), (base + 23 + add_space + 1, 62)])

        # for pp in self.pointG:
        #     for ptemp in pp:
        #         cv2.circle(self.img, ptemp, 3, (0, 255, 0), 2)
        # cv2.imshow("img", self.img)
        # cv2.waitKey(0)
        # print(self.pointG)

        return self.img

    def genPlateString(self, pos, val):
        """
        生成车牌号码string
        """
        plateStr = ""
        plateKey = []
        box = [0, 0, 0, 0, 0, 0, 0]
        if pos != -1:
            box[pos] = 1
        for unit, cpos in zip(box, range(len(box))):
            if unit == 1:
                plateStr += val
                plateKey += val
            else:
                if cpos == 0:
                    temp = 34 + r(31)
                    plateStr += chars[temp]
                    plateKey.append(get_dict_key(chars, chars[temp]))
                elif cpos == 1:
                    temp = 10 + r(24)
                    plateStr += chars[temp]
                    plateKey.append(get_dict_key(chars, chars[temp]))
                elif cpos == 2:
                    temp = r(34)
                    plateStr += chars[temp]
                    plateKey.append(get_dict_key(chars, chars[temp]))
                elif cpos == 6:
                    tempstr = '警'
                    plateStr += tempstr
                    plateKey.append(get_dict_key(chars2,tempstr))
                else:
                    temp = r(10)
                    plateStr += chars[temp]
                    plateKey.append(get_dict_key(chars, chars[temp]))
        # print('str=' + plateStr)
        # print(plateKey)
        return plateStr, plateKey

    def getPlateImg(self, text):
        """
        生成车牌图片
        text 车牌号码str
        """
        if len(text) == 7:
            fg = self.draw_string(text.encode('utf-8').decode(encoding="utf-8"))
            # 白色字体
            # fg = cv2.bitwise_not(fg)
            # plate_img = cv2.bitwise_or(fg, self.bg)
            plate_img = cv2.bitwise_and(fg,self.bg)
            plate_img, self.pointG = edgeFill(plate_img, self.pointG)

            # # 形态学变换
            # # cv2.imshow("start",plate_img)
            # plate_img, self.pointG = rot(plate_img, r(60) - 30, plate_img.shape, 30, self.pointG)
            # # print(self.pointG)
            # # drawpoint(plate_img,self.pointG,"rot")
            # plate_img, self.pointG = rotRandrom(plate_img, 10, (plate_img.shape[1], plate_img.shape[0]), self.pointG)
            # # drawpoint(plate_img, self.pointG, "rotrandrom")
            # # print(self.pointG)
            # # cv2.imshow('sst',plate_img)
            # # cv2.waitKey(0)
            # plate_img = random_envirment(plate_img, self.noplates_path)
            # plate_img = tfactor(plate_img)        # 饱和度光照的噪声
            # # cv2.imshow('sst',plate_img)
            # # cv2.waitKey(0)
            # plate_img = AddGauss(plate_img, 1 + r(4))   # 高斯模糊
            # plate_img = addNoise(plate_img)             # 添加噪声
            # # cv2.imshow("o",plate_img)
            # # cv2.waitKey(0)

            return plate_img

    def yoloLabelWrite(self, anno_infos, img_shape, yolo_label_txt):
        """
        生成label文件(txt)
        :param anno_infos:标签信息
        :param img_shape: 图像形状
        :param yolo_label_txt: 保存目录
        :return:
        """
        height, width, _ = img_shape
        label_file = open(yolo_label_txt, 'w')
        for anno_info in anno_infos:
            target_id, rect = anno_info
            temp = (float(rect[0][0]), float(rect[1][0]),
                    float(rect[0][1]), float(rect[1][1]))
            yolo_temp = convert((width, height), temp)
            label_file.write(str(target_id) + " " + " ".join([str(a) for a in yolo_temp]) + '\n')

    def genBatch(self, batchSize, outputPath, size):
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        for i in tqdm(range(batchSize)):
            plateStr, plateKey = self.genPlateString(-1, -1)
            img = self.getPlateImg(plateStr)
            #cv2.imshow("img",img)
            #cv2.waitKey(0)
            # img = cv2.resize(img, size)
            # cv2.imwrite(outputPath + "/" + str(plateStr) + ".jpg", img)
            # cv2.imencode(".jpg", img)[1].tofile(outputPath + "/" + str(plateStr) + ".jpg")
            cv2.imwrite(outputPath + "/" + str('pol') + str(i).zfill(2) + ".jpg", img)
            str_rect = []
            for x, y in zip(self.pointG, plateKey):
                str_rect.append([y, rectangle_vertex(x[0], x[1], x[2], x[3])])
            self.yoloLabelWrite(str_rect, img.shape, outputPath + "/" + str('pol') + str(i).zfill(2) + ".txt")
            str_rect.clear()
            self.pointG.clear()


def test():
    G = GenWhitePolice("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
    G.genBatch(10, "./plate", (390, 130))


if __name__ == '__main__':
    test()