#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/8 下午12:10
# @Author  : zyx
# @Email   : zhengyixiang2@qq.com
from genBigGreenPlate import GenBigGreenPlate
from genBlackConsulate import genBlackConsulate
from genBlackHKM import GenBlackHKM
from genBluePlate import GenBluePlates
from genWhitePolice import GenWhitePolice
from genGreenPlate import GenGreenPlate
from genYellowCoach import GenYellowCoach
from genYellowPlate import GenYellowPlates
from trnoise import *
from carPlateChars import *

bigGreen = 200  # 大型车新能源车牌
blackConsu = 30  # 领馆车牌
blackhkm = 50  # 港澳入境车牌
blueplate = 800  # 蓝色车牌
greenplate = 400  # 新能源车牌
whitepolice = 80  # 生成白色警用车牌
yellowcoach = 50  # 黄色教练车牌
yellowpale = 500  # 黄色车牌

G = GenBigGreenPlate("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
G.genBatch(bigGreen, "./plate", (420, 98))
G = genBlackConsulate("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
G.genBatch(blackConsu, "./plate", (390, 130))
G = GenBlackHKM("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
G.genBatch(blackhkm, "./plate", (390, 130))
G = GenBluePlates("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
G.genBatch(blueplate, "./plate", (390, 130))
G = GenGreenPlate("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
G.genBatch(greenplate, "./plate", (420, 98))
G = GenWhitePolice("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
G.genBatch(whitepolice, "./plate", (390, 130))
G = GenYellowCoach("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
G.genBatch(yellowcoach, "./plate", (390, 130))
G = GenYellowPlates("./font/platech.ttf", './font/platechar.ttf', "./NoPlates")
G.genBatch(yellowpale, "./plate", (390, 130))

newChars = {**chars, **chars2}
save_classes(newChars, "./plate/classes.txt")