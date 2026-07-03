#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
import rospy
from geometry_msgs.msg import Twist
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse
import subprocess
import actionlib
import yaml
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from grabParams_zyt3 import grabParams_zyt3
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="False")
args = parser.parse_args()

done = grabParams_zyt3.done


# 前进后退
def going(self, dist):
    # 单位为cm
    # if self.direction:
    # go_count = int(dist + grabParams.move_power_high_left + 0.5)
    # else:
    # go_count = int(dist + grabParams.move_power_high_right + 0.5)
    go_count = int(dist * grabParams_zyt3.dist_bias)
    count = 0
    move_cmd = Twist()
    time.sleep(0.5)
    if go_count >= 0:
        while True:
            move_cmd.linear.x = 0.1
            move_cmd.angular.z = 0.0
            if go_count - count < 2:
                move_cmd.linear.x = 0.05
                move_cmd.angular.z = 0
            self.pub.publish(move_cmd)
            count += 1
            if count >= go_count:
                break
            self.rate.sleep()
    else:
        go_count = -1 * go_count
        while True:
            move_cmd.linear.x = -0.1
            move_cmd.angular.z = 0.0
            if go_count - count < 2:
                move_cmd.linear.x = 0.05
                move_cmd.angular.z = 0
            self.pub.publish(move_cmd)
            count += 1
            if count >= go_count:
                break
            self.rate.sleep()
    # 当循环结束时，手动停止机器人运动
    move_cmd.linear.x = 0
    move_cmd.angular.z = 0
    self.pub.publish(move_cmd)

# 转弯
def going2(self, dist):
    # 单位为cm
    # if self.direction:
    # go_count = int(dist + grabParams.move_power_high_left + 0.5)
    # else:
    # go_count = int(dist + grabParams.move_power_high_right + 0.5)
    go_count = int(dist * grabParams_zyt3.dist_bias)
    count = 0
    move_cmd = Twist()
    time.sleep(0.5)
    if go_count >= 0:
        while True:
            move_cmd.linear.x = 0.0
            move_cmd.angular.z = 0.2
            if go_count - count < 2:
                move_cmd.linear.x = 0.05
                move_cmd.angular.z = 0
            self.pub.publish(move_cmd)
            count += 1
            if count >= go_count:
                break
            self.rate.sleep()
    else:
        go_count = -1 * go_count
        while True:
            move_cmd.linear.x = 0.0
            move_cmd.angular.z = -0.1
            if go_count - count < 2:
                move_cmd.linear.x = 0.05
                move_cmd.angular.z = 0
            self.pub.publish(move_cmd)
            count += 1
            if count >= go_count:
                break
            self.rate.sleep()
    # 当循环结束时，手动停止机器人运动
    move_cmd.linear.x = 0
    move_cmd.angular.z = 0
    self.pub.publish(move_cmd)


    
going(5)
going2(60)
    #os.system("python /home/robuster/RoboCom/navigation/BackNavigation.py")
