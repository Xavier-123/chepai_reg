# -*- coding: utf-8 -*-

"""
Created 2023/06/7
@author: Xiaoaowen
describe: service
"""

import base64
import numpy as np
import cv2
from PIL import Image, ImageFont, ImageDraw

# 导入依赖包
from api_utils.result import Code
import hyperlpr3 as lpr3


def _b642cv(img_b64):
    # base64str转numpy
    img_b64 = img_b64.encode('ascii')
    img_base64 = base64.b64decode(img_b64)
    img_array = np.frombuffer(img_base64, np.uint8)
    img_cv = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    return img_cv


def _getB64strByFilepath(filepath):
    with open(filepath, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str


def draw_plate_on_image(img, box, text, font):
    x1, y1, x2, y2 = box
    cv2.rectangle(img, (x1, y1), (x2, y2), (139, 139, 102), 2, cv2.LINE_AA)
    cv2.rectangle(img, (x1, y1 - 20), (x2, y1), (139, 139, 102), -1)
    data = Image.fromarray(img)
    draw = ImageDraw.Draw(data)
    draw.text((x1 + 5, y1 - 20), text, (255, 255, 255), font=font)
    res = np.asarray(data)
    return res


def infer(imgbase64=None, draw=False):
    code = Code.OK
    results = []

    if (imgbase64 != None or (imgbase64) > 0):
        # 中文字体加载
        font_ch = ImageFont.truetype("../resource/font/platech.ttf", 20, 0)

        # 实例化识别对象
        catcher = lpr3.LicensePlateCatcher(detect_level=lpr3.DETECT_LEVEL_HIGH)

        # 获取图像
        img = _b642cv(imgbase64)

        # 执行识别算法
        results = catcher(img)

        if (results) == 0:
            return results, Code.Recognition_Error

        # 绘图并保存
        if draw:
            for number, confidence, type_idx, box in results:
                # 解析数据并绘制
                text = f"{number} - {confidence:.2f}"
                img = draw_plate_on_image(img, box, text, font=font_ch)
                # cv2.imshow("w", image)
                # cv2.waitKey(0)
            cv2.imwrite("reslut.jpg", img)

        return results, code

    else:
        code = Code.InvalidParameter
        return results, code


if __name__ == '__main__':
    path = "C:/Users/Xavier/Desktop/chepai_2.jpg"
    imgbase64 = _getB64strByFilepath(path)
    print(imgbase64)
    # results, code = infer(imgbase64, True)
    # print("results:", results)
    # print("code:", code)
