#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/10 15:48
# @Author  : zyx
# @Email   : zhengyixiang2@qq.com
# @File    : genBluePlate.py

from trnoise import *
import os

chars = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
         10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'J', 19: 'K',
         20: 'L', 21: 'M', 22: 'N', 23: 'P', 24: 'Q', 25: 'R', 26: 'S', 27: 'T', 28: 'U', 29: 'V',
         30: 'W', 31: 'X', 32: 'Y', 33: 'Z', 34: '京', 35: '沪', 36: '津', 37: '渝', 38: '冀', 39: '晋',
         40: '蒙', 41: '辽', 42: '吉', 43: '黑', 44: '苏', 45: '浙', 46: '皖', 47: '闽', 48: '赣', 49: '鲁',
         50: '豫', 51: '鄂', 52: '湘', 53: '粤', 54: '桂', 55: '琼', 56: '川', 57: '贵', 58: '云', 59: '藏',
         60: '陕', 61: '甘', 62: '青', 63: '宁', 64: '新'}


class GenBluePlates:
    def __init__(self, fontCh, fontEng, NoPlates):
        self.fontC = ImageFont.truetype(fontCh, 43, 0)  # 中文字体
        self.fontE = ImageFont.truetype(fontEng, 60, 0)  # 英文字体
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))  # 空白图片
        self.bg = cv2.resize(cv2.imread("./images/b1.bmp"), (226, 70))  # 车牌背景图片
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
        self.img[0:70, offset + 8 + 23 + 6:offset + 8 + 23 + 6 + 23] = GenCh1(self.fontE, text[1])
        self.pointG.append([(offset + 8 + 23 + 6 - 1, 8), (offset + 8 + 23 + 6 + 23 + 1, 8),
                            (offset + 8 + 23 + 6 - 1, 62), (offset + 8 + 23 + 6 + 23 + 1, 62)])
        # 后面五个字符
        for i in range(5):
            base = offset + 8 + 23 + 6 + 23 + 17 + i * 23 + i * 6
            self.img[0:70, base: base + 23] = GenCh1(self.fontE, text[i + 2])
            self.pointG.append([(base - 1, 8), (base + 23 + 1, 8),
                                (base - 1, 62), (base + 23 + 1, 62)])
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
                else:
                    temp = r(34)
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
            fg = cv2.bitwise_not(fg)
            plate_img = cv2.bitwise_or(fg, self.bg)
            plate_img, self.pointG = edgeFill(plate_img, self.pointG)

            # 形态学变换
            # cv2.imshow("start",plate_img)
            plate_img, self.pointG = rot(plate_img, r(60) - 30, plate_img.shape, 30, self.pointG)
            # print(self.pointG)
            # drawpoint(plate_img,self.pointG,"rot")
            plate_img, self.pointG = rotRandrom(plate_img, 10, (plate_img.shape[1], plate_img.shape[0]), self.pointG)
            # drawpoint(plate_img, self.pointG, "rotrandrom")
            # print(self.pointG)
            plate_img = tfactor(plate_img)
            plate_img = random_envirment(plate_img, self.noplates_path)
            plate_img = AddGauss(plate_img, 1 + r(4))
            plate_img = addNoise(plate_img)
            # cv2.imshow("o",plate_img)
            # cv2.waitKey(0)

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
        for i in range(batchSize):
            plateStr, plateKey = self.genPlateString(-1, -1)
            img = self.getPlateImg(plateStr)
            # img = cv2.resize(img, size)
            # cv2.imwrite(outputPath + "/" + str(plateStr) + ".jpg", img)
            # cv2.imencode(".jpg", img)[1].tofile(outputPath + "/" + str(plateStr) + ".jpg")
            cv2.imwrite(outputPath + "/" + str(i).zfill(2) + ".jpg", img)
            str_rect = []
            for x, y in zip(self.pointG, plateKey):
                str_rect.append([y, rectangle_vertex(x[0], x[1], x[2], x[3])])
            self.yoloLabelWrite(str_rect, img.shape, outputPath + "/" + str(i).zfill(2) + ".txt")
            str_rect.clear()
            self.pointG.clear()


def test():
    G = GenBluePlates("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
    G.genBatch(10, "./plate", (390, 130))
    save_classes(chars, "./plate/classes.txt")


if __name__ == '__main__':
    test()
