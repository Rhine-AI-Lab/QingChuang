# encoding:utf-8
import time

import requests
import base64
import cv2  # pip install opencv-python
import threading
import math
import numpy


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
    cv2.rectangle(image, [0, 0], [640, 480], (255, 255, 255), -1)
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


# 程序从这里开始运行

# 登录百度AI， ak sk 在应用列表获取
ak = 'msfO9QL6GQZRGa1Xgyt7xOWH'  # '0XWU2LjEjSYAoTEUGXGLZifY'
sk = 'gO8AL980bdkbnOb5614ARTMm7IP1fKjy'  # 'uq06vCyy4Bgjj68Y7KaGvVyOa5bvICx8'
token = login_baidu_ai(ak, sk)  # 拿到登录后的凭证Token print('Token:', token)

cap = cv2.VideoCapture(0)  # 打开电脑摄像头 0指第一个
t = time.time()  # 记录开始运行s的时间
result = None  # 记录识别结果


def dis(p1, p2):
    return math.sqrt((p1['x'] - p2['xs']) ** 2 + (p1['y'] - p2['y']) ** 2)


def update(frame):
    global result
    rr = analysis_pose(frame, token)  # 通过百度云获取结果
    # print('检测到人数：', rr['person_num'])
    if rr['person_num'] == 0:
        return
    result = rr
    bp = result['person_info'][0]['body_parts']
    print(bp)


while cv2.waitKey(100) < 0:  # 循环不断运行
    hasFrame, frame = cap.read()  # 获取摄像头画面
    if not hasFrame:  # 如果没有图像 跳过
        break

    if time.time() - t > 0.6:  # 每隔0.6秒更新画面
        threading.Thread(target=update, args=(frame,)).start()
        t = time.time()  # 更新结果时间
    if result:
        f = draw_person(frame.copy(), result)  # 绘制结果到图像
        cv2.imshow("POSE", f)  # 显示运行结


