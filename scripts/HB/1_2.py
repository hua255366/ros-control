# -*- coding: utf-8 -*-
"""
project: The initial point of task 1 is on the left
version:   1-1-silk
author:    jiayu
date:      2024.6.26
optimise:  2025.09.27 -- 删冗余、速度100、到位等待，其余原坐标/逻辑不动
"""
import cv2
import numpy as np
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
import basic
from GrabParams_2 import grabParams
import math
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('movement', anonymous=True)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(20)
move_cmd = Twist()

motion_num = 0
mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

# ---------------- 颜色阈值 ----------------
lower_blue   = np.array([100,  43,  46])
upper_blue   = np.array([124, 255, 255])
lower_red    = np.array([170, 120, 120])
upper_red    = np.array([180, 255, 255])
lower_yellow = np.array([22 , 93,   0])
upper_yellow = np.array([34 , 255, 255])
lower_green  = np.array([35 , 43,  35])
upper_green  = np.array([90 , 255, 255])
lower_purple = np.array([120,  43,  46])
upper_purple = np.array([200, 255, 255])
lower_orange = np.array([11 , 43,  46])
upper_orange = np.array([25 , 255, 255])
# -----------------------------------------

def wait_move_done():
    """非阻塞到位等待"""
    while mc.is_moving_done() == 0:
        time.sleep(0.05)

while True:
    mc.set_color(0, 0, 255)          #  Busy

    # 1. 张开夹子 → 前往拍照位
    mc.set_gripper_value(255, 100)   # 全开
    wait_move_done()
    angles = [-95.8, -42.27, 62.57, -9.84, 10.98, -50.0]
    mc.send_angles(angles, 100)      # 拍照位
    wait_move_done()

    # 2. 视觉检测（小车前进）
    cap = cv2.VideoCapture(2)
    while True:
        move_cmd.linear.x = 0.05     # 稍快
        pub.publish(move_cmd)

        ret, frame = cap.read()
        flag = 0
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for color_lower, color_upper in ((lower_red, upper_red),
                                         (lower_yellow, upper_yellow),
                                         (lower_blue, upper_blue),
                                         (lower_green, upper_green),
                                         (lower_purple, upper_purple),
                                         (lower_orange, upper_orange)):
            mask = cv2.inRange(hsv, color_lower, color_upper)
            cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for c in cnts:
                area = cv2.contourArea(c)
                if area < 3000:               # 最小面积过滤
                    continue
                x, y, w, h = cv2.boundingRect(c)
                if 300 < x < 450 and 140 < y < 200:  # ROI
                    flag = 1
                    break
            if flag:
                break

        if flag:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    move_cmd.linear.x = 0
    pub.publish(move_cmd)
    cap.release()
    cv2.destroyAllWindows()

    # 3. 抓取（保留你原坐标，只留关键 3 帧）
    # ① 过渡
    angles = [-90.08, -3.25, -51.67, 117.59, 7.55, -48.25]
    mc.send_angles(angles, 100)
    wait_move_done()
    # ② 下压
    angles = [-90.35, 5, -65, 68, 5.97, -45.79]
    mc.send_angles(angles, 100)
    wait_move_done()
    mc.set_gripper_value(35, 100)  # 合爪
    wait_move_done()

    # 4. 放置（保留你原坐标，最简 3 帧）
    angles = [-84.72, -11.16, -103.44, 119.61, 1.23, -48.77]
    mc.send_angles(angles, 100)
    wait_move_done()
    mc.set_gripper_value(255, 100)  # 放开
    wait_move_done()

    # 5. 回待机位
    angles = [-92.9, 8.96, 37.26, -40.86, 13.44, -47.63]
    mc.send_angles(angles, 100)
    wait_move_done()

    mc.set_color(0, 255, 0)  # Free
    motion_num += 1
    if motion_num == 3:
        break

# 最后回到初始姿态
angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles, 100)
wait_move_done()