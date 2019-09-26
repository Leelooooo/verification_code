# -*- coding: utf-8 -*-
"""
Created on 2019/9/25 10:17
@Author:lilu
@Desc: 
"""
import os
import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import shutil

# 字体的位置
font_path = 'E:/python/vertification_code/fonts/arial.ttf'
# 生成几位数的验证码
number = 4
# 生成验证码图片的高度和宽度
size = (100, 30)
# 背景颜色，默认为白色
bgcolor = (255, 255, 255)
# 字体颜色，默认为蓝色
fontcolor = (0, 0, 255)
# 干扰线颜色，默认为红色
linecolor = (255, 0, 0)
# 是否要加入干扰线
draw_line = True
# 加入干扰线条数的上下限
line_number = (1, 5)


def gen_text():
    """随机生成一个字符串"""
    source = list(string.ascii_letters)
    for index in range(0, 10):
        source.append(str(index))
    return ''.join(random.sample(source, number))  # number是生成验证码的位数


def gen_line(draw, width, height):
    """绘制干扰线"""
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)


def gen_code(num):
    """生成验证码"""

    while num > 0:
        width, height = size  # 宽和高
        image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片
        font = ImageFont.truetype(font_path, 25)  # 验证码的字体
        draw = ImageDraw.Draw(image)  # 创建画笔
        text = gen_text()  # 生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / number, (height - font_height) / number), text, font=font,
                  fill=fontcolor)  # 填充字符串
        if draw_line:
            gen_line(draw, width, height)
        # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
        image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0),
                                Image.BILINEAR)  # 创建扭曲
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
        save_code(image, num)
        num -= 1


def save_code(image, num):
    image.save('./gen_imgs/code' + str(num) + '.png')  # 保存验证码图片


def remove_folder():
    shutil.rmtree('./gen_imgs')
    os.mkdir('./gen_imgs')


if __name__ == "__main__":
    remove_folder()
    print("gen_imgs文件夹已清空...")
    num = input("请输入生成的验证码的个数：")
    gen_code(int(num))
