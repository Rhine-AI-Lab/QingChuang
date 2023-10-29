import os
import time
import requests
import base64
from picamera import PiCamera
from datetime import datetime
from aip import AipSpeech


def login_baidu_ai(ak, sk):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    response = requests.get(host)  # 访问网址
    return response.json()['access_token']

# 登录百度AI， ak sk 在应用列表获取
ak = 'V5I3IusDUtATm7ZIzDp6Bx7Y'
sk = 'OS9gaC0L4KMg6x9kGmBiGqThrk7wDnto'
token = login_baidu_ai(ak, sk)  # 拿到登录后的凭证Token
print('Token:', token)
lst = 0
'''
通用文字识别（高精度版）
'''
APP_ID = '26796512'
API_KEY = 'UYvZcmGzuwmCNbvmoFXGndno'
SECRET_KEY = 's4X4lViSGzeH0Y4At9rQOduO7GRX4WER'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
def play(path_str):
    global lst
    if time.time() - lst < 3:
        return
    lst = time.time()
    os.system('ffplay %s -nodisp -autoexit -loglevel quiet' % path_str)


# 语音合成并播报
def speech(text):
    path = './temp.mp3'
    result = client.synthesis(text, 'zh', 1, {'vol': 10, })

    # 识别正确返回语音二进制
    if not isinstance(result, dict):
        with open(path, 'wb') as f:
            f.write(result)
        time.sleep(0.1)
        play(path)

o_words = [["语文","数学","英语"],["语文","数学","英语"],["数学","英语","科学"],["历史","科学","语文"],["数学","科学","语文"]]


path = 'temp.jpg'

def take_photo(path):
    camera = PiCamera()  # 定义一个摄像头对象
    camera.resolution = (1024, 768)  # 摄像界面为1024*768
    camera.start_preview()  # 开始摄像
    print("2秒后开始拍照")
    time.sleep(2)
    # input("按住回车开始拍照")

    camera.capture(path)  # 拍照并保存
    camera.stop_preview()
    camera.close()

def image_base64(path):
    f = open(path, 'rb')
    image = base64.b64encode(f.read())
    return image

today = datetime.today().weekday()-5
today1 = o_words[today]
o_words_s = set(o_words[today])
n_words = []
speech("今天是周"+str(today)+"需要带"+o_words[today][0]+o_words[today][1]+o_words[today][2])
speech("请拿资料袋对准摄像头")

while 1:  # 循环不断运行
    # print("现在缺少",list(set(o_words)-set(n_words)))
    time.sleep(1)
    print("请拿资料袋对准摄像头")
    speech("继续检测")
    time.sleep(1)
    take_photo(path)

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    # 二进制方式打开图片文件
    f = open(path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = token
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        try:
            words = response.json()["words_result"][0]["words"]

            print("检测到", words)

            if words in o_words[today]:
                n_words.append(words)
                speech("检测到"+ words)
                time.sleep(2)
                print("还缺少" + today1.remove(words))
                speech("还缺少" + today1.remove(words))

            n_words_s = set(n_words)
            c = (o_words_s&n_words_s)

            if len(c) == 3:
                print("检测完毕，东西全都带齐")
                time.sleep(3)
                speech("检测完毕，东西全都带齐")

                break
        except:
            continue





