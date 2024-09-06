# encoding=utf-8

from PIL import Image
from pyocr import tesseract
from pyocr import builders
from PIL import Image, ImageEnhance, ImageFilter

def test_text(image_file, lang='eng'):
    print image_file

    return tesseract.image_to_string(
            Image.open(image_file),
            lang=lang,
            builder=tesseract.DigitBuilder())


print test_text('./123.png')

print Image.open('./123.png')
print tesseract.image_to_string(Image.open('./11.jpg'),
                                lang='eng')
image_name = "./123.png"
im = Image.open(image_name)
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
#im.show()
                #all by pixel
s = 12          #start postion of first number
w = 10          #width of each number
h = 15          #end postion from top
t = 2           #start postion of top

im_new = []
#split four numbers in the picture
for i in range(4):
    im1 = im.crop((s+w*i+i*2,t,s+w*(i+1)+i*2,h))
    im_new.append(im1)

f = file("data.txt","a")
for k in range(4):
    l = []
    #im_new[k].show()
    for i in range(13):
        for j in range(10):
            if (im_new[k].getpixel((j,i)) == 255):
                l.append(0)
            else:
                l.append(1)

    f.write("l=[")

    n = 0
    for i in l:
        if (n%10==0):
            f.write("\n")
        f.write(str(i)+",")
        n+=1
    f.write("]\n")


import Data

DEBUG = False

def d_print(*msg):
    global DEBUG
    if DEBUG:
        for i in msg:
            print i,
        print
    else:
        pass


def Get_Num(l=[]):
    min1 = []
    min2 = []
    for n in Data.N:
        count1=count2=count3=count4=0
        if (len(l) != len(n)):
            print "Wrong pic"
            exit()
        for i in range(len(l)):
            if (l[i] == 1):
                count1+=1
                if (n[i] == 1):
                    count2+=1
        for i in range(len(l)):
            if (n[i] == 1):
                count3+=1
                if (l[i] == 1):
                    count4+=1
        d_print(count1,count2,count3,count4)

        min1.append(count1-count2)
        min2.append(count3-count4)
    d_print(min1,"\n",min2)
    for i in range(10):
        if (min1[i] <= 2 or min2[i] <= 2):
            if ((abs(min1[i] - min2[i])) <10):
                return i
    for i in range(10):
        if (min1[i] <= 4 or min2[i] <= 4):
            if (abs(min1[i] - min2[i]) <= 2):
                return i

    for i in range(10):
        flag = False
        if (min1[i] <= 3 or min2[i] <= 3):
            for j in range(10):
                if (j != i and (min1[j] <5 or min2[j] <= 5)):
                    flag = True
                else:
                    pass
            if (not flag):
                return i
    for i in range(10):
        if (min1[i] <= 5 or min2[i] <= 5):
            if (abs(min1[i] - min2[i]) <= 10):
                return i
    for i in range(10):
        if (min1[i] <= 10 or min2[i] <= 10):
            if (abs(min1[i] - min2[i]) <= 3):
                return i

#end of function Get_Num

def Pic_Reg(image_name=None):
    im = Image.open(image_name)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.show()
                    #all by pixel
    s = 12          #start postion of first number
    w = 10          #width of each number
    h = 15          #end postion from top
    t = 2           #start postion of top
    im_new = []
    #split four numbers in the picture
    for i in range(4):
        im1 = im.crop((s+w*i+i*2,t,s+w*(i+1)+i*2,h))
        im_new.append(im1)

    s = ""
    for k in range(4):
        l = []
        #im_new[k].show()
        for i in range(13):
            for j in range(10):
                if (im_new[k].getpixel((j,i)) == 255):
                    l.append(0)
                else:
                    l.append(1)

        s+=str(Get_Num(l))
    return s
print Pic_Reg("./123.png")








# from PIL import Image, ImageEnhance, ImageFilter
# import sys
#
# image_name = "./123.png"
#
# 去处 干扰点
# im = Image.open(image_name)
# im = im.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(im)
# im = enhancer.enhance(2)
# im = im.convert('1')
#
# im.show() #测试查看
#
# s = 12  # 启始 切割点 x
# t = 2  # 启始 切割点 y
#
# w = 10  # 切割 宽 +y
# h = 15  # 切割 长 +x
#
# im_new = []
# for i in range(4):  # 验证码切割
#     im1 = im.crop((s + w * i + i * 2, t, s + w * (i + 1) + i * 2, h))
#     im_new.append(im1)
#
# im_new[0].show()#测试查看
#
# xsize, ysize = im_new[0].size
# gd = []
# for i in range(ysize):
#     tmp = []
#     for j in range(xsize):
#         if (im_new[0].getpixel((j, i)) == 255):
#             tmp.append(1)
#         else:
#             tmp.append(0)
#     gd.append(tmp)
#
# 看效果
# for i in range(ysize):
#     print gd[i]
