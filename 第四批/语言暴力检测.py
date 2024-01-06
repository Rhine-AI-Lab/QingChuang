import base64
import urllib
import wave
import pyaudio
import requests
import json
import os


API_KEY = "CZezNc44QipcGu9jKRmXGx4y"
SECRET_KEY = "0GQ3v18CIp1F6CAc7vrLclZe7snmWMLS"
AUDIO_FILE = "./record.wav"


def get_file_content_as_base64(path, urlencoded=False):
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def recognize(path):
    size = os.path.getsize(path)
    url = "https://vop.baidu.com/server_api"

    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "ci92rmo5SKXhMw9TiVy1kv80BpCUu9by",
        "token": get_access_token(),
        "speech": get_file_content_as_base64(path, False),
        "len": size
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json()["result"][0])


def get_audio(path):
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1               # 声道数
    RATE = 16000               # 采样率
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = path

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    print("开始录音...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("录音结束\n")
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
   get_audio(AUDIO_FILE)
   recognize(AUDIO_FILE)


if __name__ == '__main__':
    main()
