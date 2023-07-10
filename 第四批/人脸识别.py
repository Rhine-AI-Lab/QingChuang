import base64
import urllib
import requests
import json
import sounddevice as sd
import os

API_KEY = "CZezNc44QipcGu9jKRmXGx4y"
SECRET_KEY = "0GQ3v18CIp1F6CAc7vrLclZe7snmWMLS"


def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:
        # print(audio.get_wav_data())
        f.write(audio.get_wav_data())

def main():
    url = "https://aip.baidubce.com/rest/2.0/face/v3/search?access_token=" + get_access_token()

    payload = json.dumps({
        "group_id_list": "shuren",
        "image": get_file_content_as_base64('老爸照片.jpg', urlencoded=False),
        "image_type": "BASE64"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    result = json.loads(response.text)
    print(result)
    ul = result['result']['user_list']
    if len(ul) > 0:
        if ul[0]['score'] < 80:
            print('是陌生人')
        else:
            name = ul[0]['user_id']
            print('你是:', name)
    else:
        print('没有人')


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


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()
