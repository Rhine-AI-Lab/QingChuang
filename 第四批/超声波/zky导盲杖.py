import requests
import base64
import cv2
import time
from aip import AipSpeech
import os

import RPi.GPIO as GPIO
import time

out_pin = 13
in_pin = 19


GPIO.setmode(GPIO.BCM)
GPIO.setup(out_pin, GPIO.OUT, initial=GPIO.LOW)  # 第3号针，GPIO2
GPIO.setup(in_pin, GPIO.IN)  # 第5号针，GPIO3


def check_dis():
    # 发出触发信号
    GPIO.output(out_pin, GPIO.HIGH)
    # 保持10us以上（我选择15us）
    time.sleep(0.000015)
    GPIO.output(out_pin, GPIO.LOW)
    while not GPIO.input(in_pin):
        pass
    # 发现高电平时开时计时
    t1 = time.time()
    while GPIO.input(in_pin):
        pass
    t2 = time.time()
    result = (t2 - t1) * 340 / 2
    if result > 20:
        return ""
    return result

APP_ID = '26796512'
API_KEY = 'UYvZcmGzuwmCNbvmoFXGndno'
SECRET_KEY = 's4X4lViSGzeH0Y4At9rQOduO7GRX4WER'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
obstacles = ["自行车", "饮料瓶", "隔离墩", "警示锥", "告示牌", "隔热砖"]


def login_baidu_ai(ak, sk):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    response = requests.get(host)  # 访问网址
    return response.json()['access_token']


# 登录百度AI， ak sk 在应用列表获取
ak = 'KSGNvyay0tWeGEqMN7Y9B8AQ'
sk = '23S8tEevR5jO96KcjGDn9SkF1WkGRsw2'
token = login_baidu_ai(ak, sk)  # 拿到登录后的凭证Token
print('Token:', token)

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"

def play(path_str):
    global lst
    if time.time() - lst < 3:
        return
    lst = time.time()
    os.system('ffplay %s -nodisp -autoexit -loglevel quiet' % path_str)

def speech(text):
    path = './temp.mp3'
    result = client.synthesis(text, 'zh', 1, {'vol': 10, })

    # 识别正确返回语音二进制
    if not isinstance(result, dict):
        with open(path, 'wb') as f:
            f.write(result)
        time.sleep(0.2)
        play(path)


cap = cv2.VideoCapture("3.mp4")
lst = 0
while True:
    ret, frame = cap.read()
    if time.time() - lst > 1:
        lst = 0
        cv2.imwrite("temp.jpg", frame)

        # 二进制方式打开图片文件
        f = open('temp.jpg', 'rb')
        img = base64.b64encode(f.read())

        params = {"image": img}
        access_token = token
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.text)
            for i in range(len(obstacles)):
                if response.text.find(obstacles[i]) != -1:
                    dis = check_dis()
                    if dis != "":
                        speech("检测到障碍物，" + obstacles[i] + ', 距离: ' + str(dis))
                else:
                    print("")

    # cv2.imshow("Capture_Paizhao", frame)
