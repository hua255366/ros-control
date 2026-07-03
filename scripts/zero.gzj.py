from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
#from geometry_msgs.msg import Twist  

import cv2  # OpenCV库，用于图像处理
import numpy as np  # NumPy库，用于数值计算
import time  # 时间模块，用于延时操作
import rospy  # ROS库，用于机器人操作系统
from pymycobot.mycobot import MyCobot  # MyCobot库，用于控制机械臂
from opencv_yolo import yolo  # YOLO库，用于目标检测
import math  # 数学模块，用于数学计算
from GrabParams import grabParams  # GrabParams模块，用于抓取参数
import basic  # basic模块，用于基本操作
import argparse  # argparse库，用于解析命令行参数
from geometry_msgs.msg import Twist  # geometry_msgs模块，用于发布速度消息
from actionlib.action_client import GoalManager  # actionlib模块，用于动作客户端
import actionlib  # actionlib库，用于动作服务器
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal  # move_base_msgs模块，用于导航动作
import re  # re模块，用于正则表达式
import time
from GrabParams import grabParams


mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
mc.set_color(0,0,255)#blue, arm is busy   

moveforward(3,0.3)