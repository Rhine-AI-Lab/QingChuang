import base64
import urllib
import wave
import pyaudio
import requests
import json
# import sounddevice as sr
import os

API_KEY1 = "CZezNc44QipcGu9jKRmXGx4y"
SECRET_KEY1 = "0GQ3v18CIp1F6CAc7vrLclZe7snmWMLS"


# def rec(rate=16000):
#     r = sr.Recognizer()
#     with sr.Microphone(sample_rate=rate) as source:
#         print("please say something")
#         audio = r.listen(source)
#
#     with open("recording.wav", "wb") as f:
#         # print(audio.get_wav_data())
#         f.write(audio.get_wav_data())



def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


input_filename = "./name.wav"               # 麦克风采集的语音输入
in_path = input_filename

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY1, "client_secret": SECRET_KEY1}
    return str(requests.post(url, params=params).json().get("access_token"))


def yuyin():
    size = os.path.getsize("./name.wav")

    url = "https://vop.baidu.com/server_api"

    # speech 可以通过 get_file_content_as_base64("C:\fakepath\name.wav",False) 方法获取
    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "ci92rmo5SKXhMw9TiVy1kv80BpCUu9by",
        "token": get_access_token(),
        "speech": get_file_content_as_base64("./name.wav", False),
        "len": size
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json()["result"][0])

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials",
              "client_id": API_KEY1, "client_secret": SECRET_KEY1}
    return str(requests.post(url, params=params).json().get("access_token"))


def get_audio(filepath):
    # aa = str(input("是否开始录音？   （是/否）"))
    # if aa == str("是") :
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1                # 声道数
    RATE = 16000               # 采样率
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = filepath
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("*"*10, "开始录音：请输入语音")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("*"*10, "录音结束\n")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def main():
    url = "https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=" + get_access_token()

    payload = json.dumps({
        "group_id_list": "shuren",
        "image": get_file_content_as_base64('./1.jpg', urlencoded=False),
        "image_type": "BASE64"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    try :
        ul = response.json()['result']['user_list']
        name = ul[0]['user_id']
        print('你是:', name)
    except:
        print('是陌生人')
        get_audio(in_path)
        yuyin()

    # print('没有人')


if __name__ == '__main__':
    main()
