# coding=utf-8
from aip import AipSpeech
from picamera import PiCamera
import base64
import time
import requests
import json


# 照相函数
def take_photo(path):
    camera = PiCamera()  # 定义一个摄像头对象
    camera.resolution = (1024, 768)  # 摄像界面为1024*768
    camera.start_preview()  # 开始摄像
    time.sleep(1)
    camera.capture(path)  # 拍照并保存
    camera.stop_preview()
    camera.close()


# 对图片的格式进行转换
def image_base64(path):
    f = open(path, 'rb')
    image = base64.b64encode(f.read())
    return image


# Baidu token
def get_token(api_key, secret_key):
    host = 'https://aip.baidubce.com/oauth/2.0/token' \
           '?grant_type=client_credentials' \
           '&client_id=' + api_key + \
           '&client_secret=' + secret_key
    response = requests.get(host)
    if response:
        return response.json()["access_token"]
    else:
        return ""


# Baidu interface request
def bd_request(img, token, interface, data={}):
    url = "https://aip.baidubce.com/rest/2.0/%s?access_token=%s" % (interface, token)
    headers = {'content-type': 'application/json'}
    data['image'] = img.decode()
    data['image_type'] = 'BASE64'
    data['max_face_num'] = 120
    data = json.dumps(data)
    # print(data)
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    return result


from pinpong.board import Board, Pin, ADC

Board("RPi").begin()

led = Pin(Pin.D20, Pin.OUT)
btn = Pin(Pin.D17, Pin.IN)
ding = Pin(Pin.D18, Pin.OUT)

def waitBtnClick():
    while btn.value() == 0:
        time.sleep(0.1)


from omxplayer.player import OMXPlayer
from pathlib import Path


# 树莓派播放MP3音频文件
def play(path_str):
    path = Path(path_str)
    OMXPlayer(path)


# 语音合成并播报
def speech(text):
    path = './temp.mp3'

    APP_ID = '26796512'
    API_KEY = 'UYvZcmGzuwmCNbvmoFXGndno'
    SECRET_KEY = 's4X4lViSGzeH0Y4At9rQOduO7GRX4WER'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(text, 'zh', 1, {'vol': 10, })

    # 识别正确返回语音二进制
    if not isinstance(result, dict):
        with open(path, 'wb') as f:
            f.write(result)
        time.sleep(0.2)
        play(path)
