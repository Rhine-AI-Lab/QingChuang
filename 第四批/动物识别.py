import base64
import time

import requests
from aip import AipSpeech
from picamera import PiCamera


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


# Baidu interface request
def bd_request(token, interface, data={}):
    url = "https://aip.baidubce.com/rest/2.0/%s?access_token=%s" % (interface, token)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    return result


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


yiji = ["蜂猴", "倭蜂猴", "台湾猴", "北豚尾猴", "喜马拉雅灰叶猴", "印支灰叶猴", "黑叶猴", "菲氏叶猴", "戴帽乌叶猴",
        "白头叶猴", "肖氏乌叶猴", "滇金丝猴", "黔金丝猴", " 川金丝猴", "怒江金丝猴", "西白眉长臂猿", "金丝猴",
        "东白眉长臂猿", "天行长臂猿", "白掌长臂猿", "西黑冠长臂猿", "东部黑冠长臂猿", "海南长臂猿", "白颊长臂猿",
        "印度穿山甲", "马来亚穿山甲", "中华穿山甲", "豺", "马来熊", "大熊猫", "紫貂", "貂熊", "大斑灵猫", "大灵猫",
        "小灵猫", "熊狸", "小齿狸", "缟灵猫", "荒漠猫", "丛林猫", "金猫", "云豹", "豹", "虎", "雪豹", "亚洲象",
        "普氏野马", "蒙古野驴", "西藏野驴", "野骆驼", " 威氏鼷鹿", "安徽麝", "林麝", "马麝", "黑麝", "喜马拉雅麝",
        "原麝", "黑麂", "豚鹿", "梅花鹿", "西藏马鹿", "塔里木马鹿", "坡鹿", "白唇鹿", "麋鹿", "驼鹿", "野牛",
        "爪哇野牛", "野牦牛", "蒙原羚", "普氏原羚", "藏羚羊", "高鼻羚羊", "秦岭羚牛", "四川羚牛", "不丹羚牛",
        "贡山羚牛", "赤斑羚", "喜马拉雅斑羚", "塔尔羊", "西藏盘羊", "台湾鬣羚", "喜马拉雅鬣羚", "河狸", "四川山鹧鸪",
        "海南山鹧鸪", "斑尾榛鸡", "黑嘴松鸡", "黑琴鸡", "红喉雉鹑", "黄喉雉鹑", "黑头角雉", "红胸角雉", "灰腹角雉",
        "黄腹角雉", "棕尾虹雉", "白尾梢虹雉", "绿尾虹雉", "蓝腹鹇", "褐马鸡", "白颈长尾雉", "黑颈长尾雉", "黑长尾雉",
        "白冠长尾雉", ]
erji = ["短尾猴", "熊猴", "白颊猕猴", " 猕猴", " 藏南猕猴", " 藏酋猴", "灰狼", "金豺", "貉", "沙狐", "藏狐", "赤狐",
        "懒熊", "棕熊", "黑熊", "小熊猫", "黄喉貂", "石貂", "椰子猫", "斑林狸", "野猫", "渔猫", "兔狲", "猞猁", "云猫",
        "豹猫", "獐", "贡山麂", "海南麂", "水鹿", "马鹿", "毛冠鹿", "藏原羚", "鹅喉羚", "长尾斑羚", "缅甸斑羚",
        "中华斑羚", "北山羊", "岩羊", "阿尔泰盘羊", "哈萨克盘羊", "戈壁盘羊", "天山盘羊", "帕米尔盘羊", "中华鬣羚",
        "红鬣羚", "巨松鼠", "贺兰山鼠兔", "伊犁鼠兔", "粗毛兔", "海南兔", "雪兔", "塔里木兔", "环颈山鹧鸪",
        "红喉山鹧鸪", "白眉山鹧鸪", "白颊山鹧鸪", "褐胸山鹧鸪", "红胸山鹧鸪", "台湾山鹧鸪", "绿脚树鹧鸪", "花尾榛鸡",
        "镰翅鸡", "松鸡", "岩雷鸟", "柳雷鸟", "暗腹雪鸡", "藏雪鸡", "阿尔泰雪鸡", "大石鸡", "血雉", "红腹角雉", "勺鸡",
        "红原鸡", "黑鹇", "白鹇", "白马鸡", "藏马鸡", "蓝马鸡"]


if __name__ == "__main__":
    token = get_token("r0fMHhGGuR5A5fYicM9R89uE", "lsLxfz1pG5eFtGVlNflIiFzowirKBxVN")
    path = './temp.jpg'
    record = {}
    while True:
        take_photo(path)
        img = image_base64(path)
        result = bd_request(token, "image-classify/v1/animal", {"image": img})
        print(result)
        if result['result'] and len(result['result']) > 0:
            name = result['result'][0]['name']
            if name == "非动物":
                print('识别无结果')
                continue
            print('识别结果:', name)
            record[name] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open("record.txt", "w") as f:
                lines = []
                for k in record:
                    lines.append(record[k] + ' ' + k)
                f.write("\n".join(lines))
        else:
            print('识别无结果')
