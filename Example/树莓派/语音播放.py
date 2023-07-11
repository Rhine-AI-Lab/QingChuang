# encoding:utf-8
import time

import requests
import base64
import cv2  # pip install opencv-python
import threading
from picamera import PiCamera
from aip import AipSpeech
import os

client = AipSpeech('26796512', 'UYvZcmGzuwmCNbvmoFXGndno', 's4X4lViSGzeH0Y4At9rQOduO7GRX4WER')
lst = 0


def play(path_str):
    os.system('ffplay %s -nodisp -autoexit -loglevel quiet' % path_str)


# 语音合成并播报
def speech(text, path = './temp.mp3'):
    global lst
    if time.time() - lst < 3:
        return
    lst = time.time()
    result = client.synthesis(text, 'zh', 1, {'vol': 10, })

    # 识别正确返回语音二进制
    if not isinstance(result, dict):
        with open(path, 'wb') as f:
            f.write(result)
        time.sleep(0.2)
        # play(path)


speech('你好')
