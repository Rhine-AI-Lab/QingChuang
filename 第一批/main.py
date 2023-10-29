# coding=utf-8
from aip import AipSpeech
import time


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
        # play(path)

speech('你当前情绪不好，不适合开车，请注意行车安全')
