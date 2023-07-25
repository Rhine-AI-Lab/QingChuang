# encoding:utf-8
import time

import requests
import base64
import cv2  # pip install opencv-python
import threading
from picamera import PiCamera
from aip import AipSpeech
import os
import time
from pinpong.board import Board,Pin

client = AipSpeech('26796512', 'UYvZcmGzuwmCNbvmoFXGndno', 's4X4lViSGzeH0Y4At9rQOduO7GRX4WER')

Board("RPi").begin()
led = Pin(Pin.D16, Pin.OUT) #引脚初始化为电平输出

# cv2图片转base64文本
def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


# 登录百度AI应用账号
def login_baidu_ai(ak, sk):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    response = requests.get(host)  # 访问网址
    return response.json()['access_token']


# 调用百度AI解析人体关键点图片
def analysis_detect(image_np, access_token):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"image": image_to_base64(image_np),
              "image_type": "BASE64",
              "face_field": "faceshape,facetype,age,beauty,gender"}
    response = requests.post(request_url, data=params, headers=headers)
    return response.json()


# 树莓派播放MP3音频文件
def play(path_str):
    os.system('ffplay %s -nodisp -autoexit -loglevel quiet' % path_str)

lst = 0
# 语音合成并播报
def speech(text):
    global lst
    if time.time() - lst < 3:
        return
    lst = time.time()
    path = './temp.mp3'
    result = client.synthesis(text, 'zh', 1, {'vol': 10, })

    # 识别正确返回语音二进制
    if not isinstance(result, dict):
        with open(path, 'wb') as f:
            f.write(result)
        time.sleep(0.2)
        play(path)


# 程序从这里开始运行

# 登录百度AI， ak sk 在应用列表获取
token = login_baidu_ai('4fzSz3rE4S5r7K0IcCBfU4vF', 'Cezx9bInkN2T8UTkiTTmAjfW9rMMNj27')  # 拿到登录后的凭证Token
print('Token:', token)

cap = cv2.VideoCapture(0)  # 打开电脑摄像头 0指第一个
t = time.time()  # 记录开始运行s的时间
result = None


def update(frame):
    global result
    rr = analysis_detect(frame, token)  # 通过百度云获取结果
    print(rr)
    erc = rr['error_code']
    if erc == 222202:
        print("画面中没有人")
    elif erc == 0:
        print("有人")
        speech("有人在门口，请查看是否需要开门")
        for i in range(2):
            led.value(1)
            time.sleep(0.5)
            led.value(0)
            time.sleep(0.5)
    else:
        print("检测错误")


while True:  # 循环不断运行
    hasFrame, frame = cap.read()  # 获取摄像头画面
    if not hasFrame:  # 如果没有图像 跳过
        break

    if time.time() - t > 0.6:  # 每隔0.6秒更新画面
        threading.Thread(target=update, args=(frame,)).start()
        t = time.time()  # 更新结果时间
    cv2.imshow("Camera", frame)  # 显示运行结
    cv2.waitKey(10)

