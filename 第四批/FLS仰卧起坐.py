# encoding:utf-8
import math
import time

import requests
import base64
import cv2  # pip install opencv-python
import threading
from aip import AipSpeech
import os

APP_ID = '26796512'
API_KEY = 'UYvZcmGzuwmCNbvmoFXGndno'
SECRET_KEY = 's4X4lViSGzeH0Y4At9rQOduO7GRX4WER'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# cv2图片转base64文本
def image_to_base64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


# 登录百度AI应用账号
def login_baidu_ai(ak, sk):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    response = requests.get(host)  # 访问网址
    return response.json()['access_token']


# 调用百度AI解析人体关键点图片
def analysis_pose(image_np, access_token):
    params = {"image": image_to_base64(image_np)}
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_analysis"
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    return response.json()


# 绘制结果到图像上
def draw_person(image, json):
    ss = 0.4  # 显示点的置信度阈值
    lines = [  # 需要绘制的连线列表
        'left_ear,left_eye,nose,right_eye,right_ear',
        'left_wrist,left_elbow,left_shoulder,neck,right_shoulder,right_elbow,right_wrist',
        'nose,neck',
        'left_hip,right_hip',
        'left_shoulder,left_hip,left_knee,left_ankle',
        'right_shoulder,right_hip,right_knee,right_ankle',
    ]
    for info in json['person_info']:  # 循环绘制每一个人
        bp = info['body_parts']
        for l in lines:
            ks = l.split(',')
            for i in range(len(ks) - 1):
                v1, v2 = bp[ks[i]], bp[ks[i + 1]]
                c1, c2 = (int(v1['x']), int(v1['y'])), (int(v2['x']), int(v2['y']))
                if v1['score'] > ss and v2['score'] > ss:  # 当两个点都存在时绘制中间的连线
                    cv2.line(image, c1, c2, (255, 120, 120), 3)  # 绘制中间连线
        for k in bp:  # 循环绘制每一个点
            v = bp[k]
            if v['score'] > ss:
                c = (int(v['x']), int(v['y']))
                cv2.circle(image, c, 5, (120, 255, 120), -1)  # 绘制一个点
    return image

lst = 0
# 树莓派播放MP3音频文件
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


# 程序从这里开始运行

# 登录百度AI， ak sk 在应用列表获取
ak = 'X4qM38UPj9EAEZRSX6Lv2YW7'
sk = 'qEg3HMuXoYhBZ9WnkIFEpdsAbozwiN99'
token = login_baidu_ai(ak, sk)  # 拿到登录后的凭证Token
print('Token:', token)

t = time.time()  # 记录开始运行的时间
result = 0  # 记录识别结果
#
#
# def dis(th,lh,lk):
#     # 左肩th 臀部lh 左膝lk
#     if ((lk["x"] < lh["x"]) and (lh["x"] < th["x"])) and (lk["y"] < lh["y"]):
#         return True


def check(arr):
    # 检查score
    for p in arr:
        if p['score'] < 0.2:
            return False
    return True


times = 0
state = 0
lk = None
flag = False

def update(frame):
    global a,b,c,times, state, result, lk, flag
    result = analysis_pose(frame, token)  # 通过百度云获取结果
    print(result)  # 输出结果
    if len(result['person_info']) == 0:
        return
    bp = result['person_info'][0]['body_parts']
    lw = bp['left_wrist']   # 手腕
    rw = bp['right_wrist']
    ls = bp["left_shoulder"]   # 肩膀
    lh = bp['left_hip']    # 臀部
    rh = bp['right_hip']
    lk = bp['left_knee']
    rk = bp['right_knee']
    le = bp['left_eye']
    re = bp['right_eye']

    if lh['score'] < 0.3 or ls['score'] < 0.3:
        print('关键点未拍摄全')
        return
    try:
        k = (lh['y'] - ls['y'])/(ls['x'] - lh['x'])
        if lk == None:
            lk = k
        print(k)
        if k > 3 or k < -3:
            print('检测到坐起')
            if state != 2:
                state = 2
                flag = True
                times += 1
                print('当前次数:' + str(times))
                speech('当前次数:' + str(times))
        elif 0.3 > k > -0.3:
            print('检测到躺下')
            if state != 0:
                state = 0
                flag = False
        else:
            print('动作过程中')
            if state != 1:
                state = 1
            if k < lk and not flag:
                print('动作不标准')
                speech('动作不标准')
        lk = k
    except:
        pass


cap = cv2.VideoCapture(0)  # 打开电脑摄像头 0指第一个
t = time.time()  # 记录开始运行s的时间
result = None

while True:  # 循环不断运行
    hasFrame, frame = cap.read()  # 获取摄像头画面
    if not hasFrame:  # 如果没有图像 跳过
        break

    if time.time() - t > 0.6:  # 每隔0.6秒更新画面
        threading.Thread(target=update, args=(frame,)).start()
        t = time.time()  # 更新结果时间
    cv2.imshow("Camera", frame)  # 显示运行结
    cv2.waitKey(10)
