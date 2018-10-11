# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import qrcode
from PIL import Image

# 复杂的生成二维码
def make_code(text):
    #  version是二维码的尺寸，数字大小决定二维码的密度 ,值为1~40的整数（最小值是1，是个12×12的矩阵）。 如果想让程序自动确定，将值设置为 None 并使用 fit 参数即可。
    #  error_correction：是指误差
        # ERROR_CORRECT_L：大约7 % 或更少的错误能被纠正。
        # ERROR_CORRECT_M（默认）：大约15 % 或更少的错误能被纠正。
        # ROR_CORRECT_H：大约30 % 或更少的错误能被纠正。
    # box_size:参数用来控制二维码的每个单元(box)格有多少像素点
    # border: 控制边框（二维码与图片边界的距离）包含的格子数（默认为4，是相关标准规定的最小值）。
    qr = qrcode.QRCode(version=5,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4,
                       )
    # 添加数据
    qr.add_data(text)
    # 生成二维码
    qr.make(fit=True)
    img = qr.make_image()
    img.show()


def make_easy_code(text):
    image=qrcode.make(text)
    return image

def make_icon_code(text,icon):
    img = qrcode.make(text)
    img = img.convert("RGBA")
    icon = Image.open(icon)
    #二维码大小
    img_w, img_h = img.size
    factor = 5
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    #icon大小
    icon_w, icon_h = icon.size
    # if icon_w > size_w:
    icon_w = size_w
    # if icon_h > size_h:
    icon_h = size_h
    #重设icon大小
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    #icon的粘贴位置
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h),icon)
    return img
# make_easy_code("https://www.pengllrn.xyz")
# make_easy_code("pln://f20kfajoAj394DJIsdJDJ38hfedJIjMjdjDCojdwqi")
# make_code("pln://f20kfajoAj394DJIsdJDJ38hfedJIjMjdjDCojdwqi")
# make_icon_code("pln://f20kfajoAj394DJIsdJDJ38hfedJIjMjdjDCojdwqi","D:/MyWorkDoc/favicon.png")