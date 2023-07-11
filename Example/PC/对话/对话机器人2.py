# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 23:48:39 2020

@author: hwfen
"""

import speech_recognition as sr
import os
import pyaudio
from aip import AipSpeech


r = sr.Recognizer()

harvard = sr.AudioFile('../../../第一批/recording.wav')
with harvard as source:
    audio = r.record(source)

# text=r.recognize_google(audio)
# print( r.recognize_google(audio))

def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("../../../第一批/recording.wav", "wb") as f:
        # print(audio.get_wav_data())
        f.write(audio.get_wav_data())


# 读取文件
def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


# 识别本地文件


def Gettokent():
    baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
    grant_type = "client_credentials"

    client_id = "vkGlpLlECrbqESVnvzYRL2eG"
    client_secret = "kIYoG0T4mzYiXROTYeVm4mLhu9sxzPtq"

    # 拼url
    url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        client_id, client_secret)
    # print(url)
    # 获取token
    res = requests.post(url)
    # print(res.text)
    token = json.loads(res.text)["access_token"]
    print(token)


# 向远程服务上传整段语音进行识别
def baidu_speech():
    APP_ID = '25543588'
    API_KEY = 'vkGlpLlECrbqESVnvzYRL2eG'
    SECRET_KEY = 'kIYoG0T4mzYiXROTYeVm4mLhu9sxzPtq'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # .wav文件转.pcm文件
    os.system('ffmpeg -y  -i recording.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 recording.pcm')

    result = client.asr(get_file_content('recording.pcm'), 'pcm', 16000, {'dev_pid': 1537, })
    # result = client.asr(get_file_content('recording.wav'), 'wav', 16000, {'dev_pid': 1537, })
    print(result["result"][0][:-1])
    # 默认1537（普通话 输入法模型），dev_pid参数见本节开头的表格
    return result["result"][0][:-1]


import requests
import json

TURING_KEY = "1b2e00efe9824719954db3218703253c"
URL = "http://openapi.tuling123.com/openapi/api/v2"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}
data = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": ""
        },
        "selfInfo": {
            "location": {
                "city": "上海",
                "street": "邯郸路"
            }
        }
    },
    "userInfo": {
        "apiKey": TURING_KEY,
        "userId": "starky"
    }
}


def robot(text=""):
    data["perception"]["inputText"]["text"] = text
    response = requests.request("post", URL, json=data, headers=HEADERS)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("the AI said: " + result)
    return result


from aip import AipSpeech


# 百度AI应用列表中对应应用名称为语音识别的 系统分配给用户的一些信息

def synth(text):
    APP_ID = '25543588'
    API_KEY = 'vkGlpLlECrbqESVnvzYRL2eG'
    SECRET_KEY = 'kIYoG0T4mzYiXROTYeVm4mLhu9sxzPtq'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(text, 'zh', 1, {'vol': 10, })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('regresult1.mp3', 'wb') as f:
            f.write(result)
            f.close()


'''
import pyaudio
import wave

filename = 'auido.mp3'


chunk = 1024   
wf = wave.open(filename, 'rb')
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

data = wf.readframes(chunk)

while data != '':
    stream.write(data)
    data = wf.readframes(chunk)

stream.close()
p.terminate()
'''

from playsound import playsound

if __name__ == '__main__':
    rec()
    c = r.recognize_sphinx(audio, language='zh-cn')
    print(c)
    text = baidu_speech()
    # text=robot("今天几号")

    synth(text)

    playsound('regresult1.mp3')
