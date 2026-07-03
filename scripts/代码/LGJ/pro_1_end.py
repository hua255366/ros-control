#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from pymycobot.genre import Coord
from VideoCapture import FastVideoCapture
import math
from GrabParams_hmy_2 import grabParams  #获取了一些全局配置，如偏移量、图像大小、调试模式
import basic
import argparse  #解析命令行参数
from geometry_msgs.msg import Twist
from actionlib.action_client import GoalManager
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import re

parser = argparse.ArgumentParser(description='manual to this script')

parser.add_argument("--debug", type=bool, default="True")

args = parser.parse_args()

y_bias = grabParams.y_bias 

x_bias = grabParams.x_bias 

height_bias = grabParams.height_bias

IMG_SIZE = grabParams.IMG_SIZE

cap_num = grabParams.cap_num

debug = grabParams.debug 

coords = grabParams.coords_ready

done = grabParams.done

rospy.init_node('movement', anonymous=True)

pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(20)

move_cmd = Twist()

global motion_num

class Detect_marker(object):  #包含了机械臂控制和图像处理的逻辑

    def __init__(self):  #实例化了MyCobot对象并上电，初始化了YOLO对象检测模型，并设置了HSV颜色范围

        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

        self.mc.power_on()

        self.yolo = yolo()

        self.color = 0
       
        self.x1 = self.x2 = self.y1 = self.y2 = 0        
        
        self.HSV = {

            "yellow": [np.array([22, 93, 0]), np.array([45, 255, 255])],

            "red": [np.array([170, 120, 120]), np.array([180, 255, 255])],

            "green": [np.array([35, 43, 35]), np.array([90, 255, 255])],

            "blue": [np.array([90,43,46]), np.array([110,255,255])],

            "purple": [np.array([120, 43, 46]), np.array([200, 255, 255])],

            "orange": [np.array([11, 43, 46]), np.array([25, 255, 255])],

        }

        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0

        self.c_x, self.c_y = IMG_SIZE/2, IMG_SIZE/2

        self.ratio = grabParams.ratio

    def move(self, x, y):  #根据检测到物体的位置，计算机械臂目标坐标，并移动机械臂到该位置进行抓取，主要目标是计算出coords_target

        global height_bias, done  #声明了 height_bias 和 done 这两个变量是全局变量  height_bias 可能是一个用于调整机械臂目标坐标高度的偏置值  done 可能是一个标志变量，用于指示某个操作（如抓取）是否完成
        
        coords_target = [coords[0]+int(x), coords[1]+int(y), height_bias, coords[3], coords[4], coords[5]]

        print("coords_target:",coords_target)

        basic.move_to_target_coords(coords_target,grabParams.GRAB_MOVE_SPEED) 

        basic.grap(True)  #True 来闭合夹爪，抓取物体

        angles = [-50.97, 49.39, -86.74, 48.42, -36.65, 136.49]  

        self.mc.send_angles(angles,30)  #回退到安全位置，关节角度设置

        time.sleep(3)

        done = True  #将全局变量 done 设置为 True，表示抓取动作已经完成

        print("Done")

        self.mc.set_color(0,255,0)  #设置机械臂的颜色为绿色，表示机械臂当前是空闲状态

    def init_mycobot(self):   #初始化机械臂到一个起始位置，并设置夹爪为张开状态

        basic.grap(False)    

        time.sleep(1) 

        basic.move_to_target_coords(coords,grabParams.GRAB_MOVE_SPEED)       
 
    def get_position(self, x, y):  #根据物体在图像中的位置和预设的抓取方向，计算机械臂需要移动的实际坐标。

        wx = wy = 0

        if grabParams.grab_direct == "front":

            wx = (self.c_y - y) * self.ratio

            wy = (self.c_x - x) * self.ratio

        elif grabParams.grab_direct == "right":

            wx = (self.c_x - x) * self.ratio

            wy = (y - self.c_y) * self.ratio

        return wx, wy

    def transform_frame(self, frame):  #使用YOLO模型对输入的图像帧进行处理，以适应模型的输入尺寸

        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (IMG_SIZE, IMG_SIZE))

        return frame
   
    def color_detect(self, img):  #检测图像中物体的颜色和位置，使用颜色过滤和轮廓检测来识别特定颜色的物体

        x = y = 0

        for mycolor, item in self.HSV.items():

            redLower = np.array(item[0])

            redUpper = np.array(item[1])
            
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            mask = cv2.inRange(hsv, item[0], item[1])
            
            erosion = cv2.erode(mask, np.ones((1, 1), np.uint8), iterations=2)
            
            dilation = cv2.dilate(erosion, np.ones(

                (1, 1), np.uint8), iterations=2)

            target = cv2.bitwise_and(img, img, mask=dilation)

            ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)

            contours, hierarchy = cv2.findContours(

                dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
              
                boxes = [

                    box

                    for box in [cv2.boundingRect(c) for c in contours]

                    if 70 < min(box[2], box[3]) and  max(box[2], box[3]) < 120

                ]

                print(boxes)

                if boxes:

                    for box in boxes:

                        x, y, w, h = box

                    c = max(contours, key=cv2.contourArea)

                    x, y, w, h = cv2.boundingRect(c)

                    print(x, y, w, h)

                    cv2.rectangle(img, (x, y), (x+w, y+h), (130, 130, 0), 2)

                    x, y = (x*2+w)/2, (y*2+h)/2
 
                    if mycolor == "yellow":  #根据检测到的物体颜色，设置 self.color 变量，这可能用于后续逻辑，例如根据物体颜色选择不同的处理方式

                        self.color = 1

                    elif mycolor == "red":

                        self.color = 0

                    else:

                        self.color = 3

        if abs(x) + abs(y) > 0:  #如果检测到物体，则返回物体的中心坐标 (x, y)；如果没有检测到物体，则返回 None。

            return x, y

        else:

            return None

    def run(self):  #初始化机械臂的状态，设置为忙碌，并调用init_mycobot方法

        self.mc.set_color(0,0,255)#blue, arm is busy

        self.init_mycobot()
        
    def show_image(self, img):  #如果调试模式开启，则显示当前处理后的图像

        print(args.debug)

        if debug and args.debug:

            cv2.imshow("figure", img)

            cv2.waitKey(50) 

detect = Detect_marker() #在这个构造函数中，会初始化MyCobot机械臂、YOLO对象检测模型以及其他必要的设置

detect.run()   #初始化机械臂到一个准备状态

cap = cv2.VideoCapture(2)

time.sleep(0.5) 

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

i=0

init_num = 0

nparams = 0

num = 0

miss = 0

while True:

    move_cmd.linear.x = 0.02  # m/s

    move_cmd.linear.z = 0  # m/s

    pub.publish(move_cmd)

    retval,frame = cap.read()  # 从视频捕获对象cap中读取一帧图像

    frame = cv2.flip(frame,0)  

    frame = cv2.flip(frame,1)

    frame = detect.transform_frame(frame)  #处理图像，可能包括调整图像大小、应用YOLO模型进行对象检测

    detect_result = detect.color_detect(frame)  #用color_detect方法检测图像中物体的颜色和位置

    detect.show_image(frame)  #显示当前处理后的图像

    if detect_result is None:   #为None，则使用continue跳过本次循环的剩余部分    

        continue

    else:            #不是None，说明检测到了物体，获取物体在图像中的位置(x, y)

        x, y = detect_result

        real_x, real_y = detect.get_position(x, y)  #根据物体在图像中的位置和一些预设的参数（如偏移量），计算机械臂需要到达的实际坐标

        print("real_x, real_y:",real_x, real_y)

        if real_y<=3 or real_x>40 or real_y>50 :

            continue

        coords_now = basic.get_coords()  #basic模块的get_coords函数来获取当前坐标信息

        if len(coords_now) == 6:

            coords = coords_now

        print("coords:",coords)

        move_cmd.linear.x = 0.02  # m/s

        move_cmd.linear.z = 0  # m/s

        pub.publish(move_cmd)

        time.sleep(0.5)

        detect.move(real_x + x_bias, real_y + y_bias)

        print("Detected color:", detect.color)

        cap.release()

        cv2.destroyAllWindows()

        break

move_cmd.linear.x = 0.02  # m/s

move_cmd.linear.z = 0  # m/s

pub.publish(move_cmd)

time.sleep(0.5)
        
angles = [-90, 50, -150, 110, 0, -45]#xia

mc.send_angles(angles, 30)

time.sleep(3)

angles = [-87.45, -10.01, -104.85, 128.14, -0.61, -46.14]#xia_jing

mc.send_angles(angles, 30)

time.sleep(3)

mc.set_gripper_value(255, 30)

time.sleep(3)

angles = [-87.09, 36.82, -148.18, 123.31, -1.14, -45.52]#xia_tui

mc.send_angles(angles, 30)

time.sleep(2)

angles = [-87.62, 55.63, -134.64, 119.44, -1.31, -44.12]#xia_tai

mc.send_angles(angles, 30)

time.sleep(1)

angles = [-89.73, -0.61, -0.87, -0.96, -0.35, 129.37]#shang

mc.send_angles(angles, 30)

time.sleep(2)