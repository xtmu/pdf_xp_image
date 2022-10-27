#! C:\Users\init\miniconda3\envs\pdf_xp_image\python.exe
# -*- coding: UTF-8 -*-

import fitz
import os
import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import askyesno


# 选择多文件
def select_files():
    # 选取多个文件
    file_path_list = askopenfilenames(title='选择多个文件')

    if file_path_list == '':
        quit()

    # 获取文件列表
    dirlist = []
    filenamelist = []
    extlist = []
    for i in range(len(file_path_list)):
        (dir, filefullname) = os.path.split(file_path_list[i])
        filename, ext = os.path.splitext(filefullname)
        dirlist.append(dir)
        filenamelist.append(filename)
        extlist.append(ext)

    return file_path_list, dirlist, filenamelist, extlist


def func(pdf_path, image_dir):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        imglist = doc.getPageImageList(i)
        for j, img in enumerate(imglist):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)  # make pixmap from image
            if pix.n - pix.alpha < 4:  # can be saved as PNG
                # pix.writePNG("p%s-%s.png" % (i + 1, j + 1))
                output_path = image_dir + '\\' + "p%s-%s.png" % (i + 1, j + 1)
                pix.writePNG(output_path)
            else:  # CMYK: must convert first
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                # pix0.writePNG("p%s-%s.png" % (i + 1, j + 1))
                output_path = image_dir + '\\' + "p%s-%s.png" % (i + 1, j + 1)
                pix0.writePNG(output_path)
                pix0 = None  # free Pixmap resources
            pix = None  # free Pixmap resources


def main():
    # dl 为目录列表， fl 为文件名列表，el 为拓展名列表
    (pl, dl, fl, el) = select_files()

    # print(100*'=')
    # print("使用说明：绿色转化成功，白色未转化，红色转化失败。\n转化中,请等待...")
    # print(100*'=')
    for i in range(len(pl)):
        # 获得 pdf 路径
        input_path = pl[i]

        # 检查输入合法性
        if el[i] == '.pdf':
            # 输入合法，以下处理输出

            # 获得图片目录
            output_dir = dl[i] + os.sep + "[IMG] " + fl[i]

            # 检查图片目录
            if os.path.exists(output_dir):
                # 已存在输出，跳过转化
                print("\033[0;37m[%s]\033[0m" % input_path)
                continue

            # 初始化图片目录
            os.mkdir(output_dir)

            # 将 pdf 中的图片输出到图片目录
            print("\033[0;32m[%s]\033[0m" % input_path)
            func(pdf_path=input_path, image_dir=output_dir)  # input the path of pdf file

            # 打开输出文件夹
            # os.startfile(output_dir)
        else:
            # 非法输入
            print("\033[0;31m[%s]\033[0m" % input_path)
    # print(100*'=')
    # print("转化结束！")
    # print(100*'=')


if __name__ == "__main__":
    main()
