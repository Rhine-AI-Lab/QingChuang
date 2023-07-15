# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

out_pin = 13
in_pin = 19


GPIO.setmode(GPIO.BCM)
GPIO.setup(out_pin, GPIO.OUT, initial=GPIO.LOW)  # 第3号针，GPIO2
GPIO.setup(in_pin, GPIO.IN)  # 第5号针，GPIO3


def check_dis():
    # 发出触发信号
    GPIO.output(out_pin, GPIO.HIGH)
    # 保持10us以上（我选择15us）
    time.sleep(0.000015)
    GPIO.output(out_pin, GPIO.LOW)
    while not GPIO.input(in_pin):
        pass
    # 发现高电平时开时计时
    t1 = time.time()
    while GPIO.input(in_pin):
        pass
    t2 = time.time()
    result = (t2 - t1) * 340 / 2
    if result > 20:
        return ""
    return "%.2fm" % result

time.sleep(2)
try:
    while True:
        print(f'Distance: {check_dis()}')
        time.sleep(0.5)
except:
    GPIO.cleanup()
