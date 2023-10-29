import time
import os
from aip import AipSpeech
APP_ID = '26796512'
API_KEY = 'UYvZcmGzuwmCNbvmoFXGndno'
SECRET_KEY = 's4X4lViSGzeH0Y4At9rQOduO7GRX4WER'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
lst = 0
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

speech("你好")