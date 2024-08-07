import numpy as np
import cv2
import os
import random

###  Horizontal cutting & vertical stitching   #####
def V(img,num):
    #####其中一半拼成一副图
    for i in range(0, num, 2):
        if (i == 0):
            hei_0 = int(i * heigt / num)##每块的长度
            hei_1 = int((i + 1) * heigt / num)
            hei_2 = int((i + 2) * heigt / num)
            hei_3 = int((i + 3) * heigt / num)

            wid_0 = 0
            wid_1 = int(width)

            # 图片分块裁剪操作
            VroiImg = img[hei_0:hei_1, wid_0:wid_1]  # [0,1]
            # 图片分块裁剪操作
            VroiImg2 = img[hei_2:hei_3, wid_0:wid_1]  # [2,3]
            VroiImgd = np.vstack((VroiImg, VroiImg2))
        else:
            wid_0 = 0
            wid_1 = int(width)
            hei_x1 = int((i + 2) * heigt / num)
            hei_x2 = int((i + 3) * heigt / num)

            VroiImgx = img[hei_x1:hei_x2, wid_0:wid_1]  # [x1,x2]
            VroiImgd = np.vstack((VroiImgd, VroiImgx))

    #######另外一半的拼接成一幅图
    for j in range(0, num, 2):
        if (j == 0):
            hei_0 = int((j + 1) * heigt / num)
            hei_1 = int((j + 2) * heigt / num)
            hei_2 = int((j + 3) * heigt / num)
            hei_3 = int((j + 4) * heigt / num)

            wid_0 = 0
            wid_1 = int(width)

            # 图片分块裁剪操作
            VroiImg = img[hei_0:hei_1, wid_0:wid_1]  # [0,1]
            # 图片分块裁剪操作
            VroiImg2 = img[hei_2:hei_3, wid_0:wid_1]  # [2,3]

            VroiImgs = np.vstack((VroiImg, VroiImg2))
        else:
            wid_0 = 0
            wid_1 = int(width)
            hei_x11 = int((j + 3) * heigt / num)
            hei_x22 = int((j + 4) * heigt / num)

            VroiImgx2 = img[hei_x11:hei_x22, wid_0:wid_1]  # [x1,x2]
            VroiImgs = np.vstack((VroiImgs, VroiImgx2))
    return VroiImgs,VroiImgd


###  Vertical cutting & horizontal stitching   #####
def H(VImgcat,num):
    for i in range(0, num, 2):
        if(i==0):
            # print(i)
            # 调整裁剪区域像素位置
            hei_0 = 0
            hei_1 = int(heigt)

            wid_0 = int(i * width / num)
            wid_1 = int((i + 1) * width / num)
            wid_2 = int((i + 2) * width / num)
            wid_3 = int((i + 3) * width / num)
            # 图片分块裁剪操作
            HroiImg = VImgcat[hei_0:hei_1, wid_0:wid_1]
            # 图片分块裁剪操作
            HroiImg2 = VImgcat[hei_0:hei_1, wid_2:wid_3]
            HroiImgd = np.hstack((HroiImg, HroiImg2))
        else:
            # print(i)
            # 调整裁剪区域像素位置
            hei_0 = 0
            hei_1 = int(heigt)
            wid_x1 = int((i+2) * width / num)
            wid_x2 = int((i+3) * width / num)

            HroiImgx = VImgcat[hei_0:hei_1, wid_x1:wid_x2]
            HroiImgd = np.hstack((HroiImgd, HroiImgx))

    for j in range(0, num, 2):
        if(j==0):
            # print(j)
            hei_0 = 0
            hei_1 = int(heigt)
            wid_0 = int((j+1) * width / num)
            wid_1 = int((j + 2) * width / num)

            wid_2 = int((j + 3) * width / num)
            wid_3 = int((j + 4) * width / num)
            # 图片分块裁剪操作
            HroiImg = VImgcat[hei_0:hei_1, wid_0:wid_1]
            # 图片分块裁剪操作
            HroiImg2 =VImgcat[hei_0:hei_1, wid_2:wid_3]
            HroiImgs = np.hstack((HroiImg, HroiImg2))
        else:
            # print(j)
            hei_0 = 0
            hei_1 = int(heigt)
            wid_x11 = int((j+3) * width / num)
            wid_x22 = int((j+4) * width / num)

            HroiImgx2 = VImgcat[hei_0:hei_1, wid_x11:wid_x22]
            HroiImgs = np.hstack((HroiImgs, HroiImgx2))
    return HroiImgs,HroiImgd


# ############   single images   ################
img = cv2.resize(cv2.imread('pic.png'),(640,640))#读取单张图片的代码#读取单张图片的代码 640,428
# ############   single images   ################

# ############   batch images   ################
# path = os.path.expanduser("your path")
#
# for f in os.listdir(path):
#     path = "your path" + f.strip()
#     # img = cv2.resize(cv2.imread(path),(640,640))
#     img = cv2.imread(path)
# ############   batch images   ################

heigt = img.shape[0]
width = img.shape[1]
#
if(heigt>width):
    Vimg1,Vimg2 = V(img, int(heigt/4))
    VHimg1,VHimg2 = H(Vimg1, int(width/4))
    VHimg3,VHimg4 = H(Vimg2, int(width/16))
else:
    Himg1,Himg2 = H(img, int(width/4))
    VHimg1,VHimg2 = V(Himg1, int(heigt/8))
    VHimg3, VHimg4 = V(Himg2, int(heigt/16))

cv2.imshow('origin', img)
cv2.imshow('1', VHimg1)
cv2.imshow('2', VHimg2)
cv2.imshow('3', VHimg3)
cv2.imshow('4', VHimg4)
cv2.waitKey(0)

