# encoding: UTF-8
# !/usr/bin/env python2
import cv2
import os
import numpy as np
import time
# import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse
import rospy
from move_control import movement
#from 0705task3_nav import DirectNavigator
import tf
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Quaternion, Twist
from _0816sonor import listen_for_distance

# m_speed = movement_speed()


# def moveback(self, time_seconds,speed):
#     print("backward...")
#     count = 20*time_seconds
#     move_cmd = Twist()
#     while count > 0:
#         move_cmd.linear.x = -speed #m/s (0.05)
#         self.pub.publish(move_cmd)
#         self.rate.sleep()
#         count -= 1

# if __name__ == "__main__":
#     try:
#         m_speed.moveback(0.10, 0.2)
#     except rospy.ROSInterruptException:
#         pass

def move_backward(time=1.0, speed=0.2):
    # 初始化节点
    rospy.init_node('move_backward_node', anonymous=True)
    
    # 创建发布者
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10Hz
    
    # 创建Twist消息
    move_cmd = Twist()
    move_cmd.linear.x = -speed  # 负值表示后退
    
    # 记录开始时间
    start_time = rospy.Time.now().to_sec()
    
    # 发布后退命令
    while (rospy.Time.now().to_sec() - start_time) < time:
        pub.publish(move_cmd)
        rate.sleep()
    
    # 停止机器人
    move_cmd.linear.x = 0
    pub.publish(move_cmd)
    print("后退完成")

# 调用后退函数
if __name__ == "__main__":
    try:
        move_backward(time=2.0, speed=0.15)  # 后退2秒，速度0.15m/s
    except rospy.ROSInterruptException:
        pass