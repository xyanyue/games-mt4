import os
import time
import pytesseract
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imagehash


def PATH(p): return os.path.abspath(p)


XY = [
    '130 248',  # 主任务
    '1289 646',  # 提交任务
    '1048 562',  # 点击穿戴
    '1375 80', #跳过剧情
]

PicHash = {}

path = PATH(os.getcwd() + "/screenshot")

def init():
    PicHash['tijiao'] = hash('/right_tijiao.png')
    PicHash['jineng'] = hash('/right_jineng.png')
    PicHash['jiaoliu'] = hash('/right_jiaoliu.png')
    # os.remove(path+"/tmp.png")

def screenshot():
    os.popen("adb shell rm /sdcard/tmp.png")
    
    timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    os.popen("adb wait-for-device")
    os.popen("adb shell screencap -p /sdcard/tmp.png")
    if not os.path.isdir(PATH(os.getcwd() + "/screenshot")):
        os.makedirs(path)
    os.popen("adb pull /sdcard/tmp.png " + PATH(path + "/tmp.png"))
    
    # print("success")


def clickMainCron(num):
    os.popen("adb shell input tap "+XY[num])


def click():
    for x in XY:
        os.popen("adb shell input tap "+x)


def cropImages():
    
    img = Image.open(path+'/tmp.png')
    x, y = img.size
    

    right_box = [int(img.size[0]/4*3),int(img.size[1]/2),img.size[0],img.size[1]]
    
    cropImg = img.crop(right_box)
    
    cropImg.save(path+'/right_tmp.png')
   




def hash(im1):
    path = PATH(os.getcwd() + "/screenshot")
    hash_size = 12
    hash1 = imagehash.dhash(Image.open(path+im1),hash_size=hash_size)
    return hash1
    
def likeit(hash1,hash2):
    return (1 - (hash1 - hash2)/len(hash1.hash)**2)

def fileDone():
    if not os.path.exists(path+"/tmp.png"):
        print('等待截图就位...')
        time.sleep(1)
        fileDone()

def cactionDone(x):
    if x == 'tijiao':
        print("提交任务按钮 ~")
        clickMainCron(1)
        clickMainCron(0)
    if x == 'jineng':
        print('pass ~')
        clickMainCron(0)
    if x== 'jiaoliu':
        print('瞎BB ~')
        # clickMainCron(3)
        for x in range(1,3):
            time.sleep(0.5)
            clickMainCron(0)



if __name__ == "__main__":
    # if os.path.exists(path+"/tmp.png"):
    #     os.remove(path+"/tmp.png")
    # screenshot()
    # fileDone()
    # cropImages()

    init()
    while True:
        if os.path.exists(path+"/tmp.png"):
            os.remove(path+"/tmp.png")
        if os.path.exists(path+"/right_tmp.png"):
            os.remove(path+"/right_tmp.png")
        screenshot()
        fileDone()
        cropImages()
        hash2 = hash("/right_tmp.png")
        maxHash = 0
        action = ''
        for x in PicHash:
            # print(PicHash[x])
            v = likeit(PicHash[x],hash2) 
            if v > maxHash:
                maxHash = v
                action = x
        # print(maxHash,action)
        cactionDone(action)
        time.sleep(3)


