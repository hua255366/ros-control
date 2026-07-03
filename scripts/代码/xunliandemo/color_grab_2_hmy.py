#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
# import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from pymycobot.genre import Coord
from VideoCapture import FastVideoCapture
import math
from GrabParams_hmy import grabParams  #获取了一些全局配置，如偏移量、图像大小、调试模式
import basic
import argparse  #解析命令行参数

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="True")
args = parser.parse_args()


y_bias = grabParams.y_bias 
x_bias = grabParams.x_bias 
height_bias = grabParams.height_bias

IMG_SIZE = grabParams.IMG_SIZE

cap_num = grabParams.cap_num

# show image and waitkey
debug = grabParams.debug 

coords = grabParams.coords_ready
done = grabParams.done

class Detect_marker(object):  #包含了机械臂控制和图像处理的逻辑
    def __init__(self):  #实例化了MyCobot对象并上电，初始化了YOLO对象检测模型，并设置了HSV颜色范围
        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()

        self.yolo = yolo()


        # choose place to set cube
        self.color = 0
        # parameters to calculate camera clipping parameters
        self.x1 = self.x2 = self.y1 = self.y2 = 0        
         # set color HSV
        self.HSV = {
            "yellow": [np.array([22, 93, 0]), np.array([45, 255, 255])],
            "red": [np.array([170, 120, 120]), np.array([180, 255, 255])],
            "green": [np.array([35, 43, 35]), np.array([90, 255, 255])],
            "blue": [np.array([90,43,46]), np.array([110,255,255])],
            "purple": [np.array([140, 150, 120]), np.array([160, 255, 255])],
        }
        # use to calculate coord between cube and mycobot
        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0
        # The coordinates of the cube relative to the mycobot
        self.c_x, self.c_y = IMG_SIZE/2, IMG_SIZE/2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio

    
    # Grasping motion  #原本固定的z用来做y，z坐便要用传进来的y
    def move(self, x, y):  #根据检测到物体的位置，计算机械臂目标坐标，并移动机械臂到该位置进行抓取，主要目标是计算出coords_target
        global height_bias, done  #声明了 height_bias 和 done 这两个变量是全局变量  height_bias 可能是一个用于调整机械臂目标坐标高度的偏置值  done 可能是一个标志变量，用于指示某个操作（如抓取）是否完成
        
        coords_target = [coords[0]+int(x), coords[1]+int(y), height_bias, coords[3], coords[4], coords[5]]
        #coords_target = [coords[1]+int(y), height_bias, -(coords[0])+int(x), coords[3], coords[4], coords[5]]
	#coords_target = [height_bias, coords[0]+int(x), coords[1]+int(y), coords[5], coords[3], coords[4]]
	#coords_target =[67.6, 145.1, 379.1, -89.51, -43.94, -1.83]
        print("coords_target:",coords_target)
        #basic.move_to_target_coords(coords_target, grabParams.GRAB_MOVE_SPEED)  #传入的分别是，目标点坐标，抓取移动速度
        basic.move_to_target_coords(coords_target,grabParams.GRAB_MOVE_SPEED) 

        basic.grap(True)  #True 来闭合夹爪，抓取物体

        angles = [0, 0, 0, 0, 0, 0]  
        self.mc.send_angles(angles,30)  #回退到安全位置，关节角度设置
        time.sleep(3)

        done = True  #将全局变量 done 设置为 True，表示抓取动作已经完成
        print("Done")
        self.mc.set_color(0,255,0)  #设置机械臂的颜色为绿色，表示机械臂当前是空闲状态


    # init mycobot
    def init_mycobot(self):   #初始化机械臂到一个起始位置，并设置夹爪为张开状态
        #angles = [97.17, -0.61, -0.52, -1.05, -0.7, -40.6]
	angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
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
   
    # detect cube color
    def color_detect(self, img):  #检测图像中物体的颜色和位置，使用颜色过滤和轮廓检测来识别特定颜色的物体
        # set the arrangement of color'HSV
        x = y = 0
        for mycolor, item in self.HSV.items():
            redLower = np.array(item[0])
            redUpper = np.array(item[1])
            # transfrom the img to model of gray
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # wipe off all color expect color in range
            mask = cv2.inRange(hsv, item[0], item[1])
            # a etching operation on a picture to remove edge roughness
            erosion = cv2.erode(mask, np.ones((1, 1), np.uint8), iterations=2)
            # the image for expansion operation, its role is to deepen the color depth in the picture
            dilation = cv2.dilate(erosion, np.ones(
                (1, 1), np.uint8), iterations=2)
            # adds pixels to the image
            target = cv2.bitwise_and(img, img, mask=dilation)
            # the filtered image is transformed into a binary image and placed in binary
            ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
            # get the contour coordinates of the image, where contours is the coordinate value, here only the contour is detected
            contours, hierarchy = cv2.findContours(
                dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                # do something about misidentification
                boxes = [
                    box
                    for box in [cv2.boundingRect(c) for c in contours]
                    if 70 < min(box[2], box[3]) and  max(box[2], box[3]) < 120
                    # if min(img.shape[0], img.shape[1]) / 10
                    # < min(box[2], box[3])
                    # < min(img.shape[0], img.shape[1]) / 1
                ]
                print(boxes)
                if boxes:
                    for box in boxes:
                        # print(box)
                        x, y, w, h = box
                        # if abs(w-h)>15:
                        #     return None
                    # find the largest object that fits the requirements
                    c = max(contours, key=cv2.contourArea)
                    # get the lower left and upper right points of the positioning object
                    x, y, w, h = cv2.boundingRect(c)
                    print(x, y, w, h)
                    # locate the target by drawing rectangle
                    cv2.rectangle(img, (x, y), (x+w, y+h), (130, 130, 0), 2)
                    # calculate the rectangle center
                    x, y = (x*2+w)/2, (y*2+h)/2
                    # calculate the real coordinates of mycobot relative to the target
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


if __name__ == "__main__":
    detect = Detect_marker() #在这个构造函数中，会初始化MyCobot机械臂、YOLO对象检测模型以及其他必要的设置
    detect.run()   #初始化机械臂到一个准备状态

    cap = FastVideoCapture(cap_num)  #用于从视频捕获设备（如摄像头）获取视频流的自定义类,cap来引用这个视频捕获对象，并调用它的方法来读取视频帧
    time.sleep(0.5) 
    

    init_num = 0
    nparams = 0
    num = 0
    miss = 0
    while cv2.waitKey(1) < 0 and not done:
        frame = cap.read()  # 从视频捕获对象cap中读取一帧图像
        #分别对图像在水平和垂直方向上进行翻转。这可能是为了调整图像的方向，以适应机械臂的视角
        frame = cv2.flip(frame,0)  
        frame = cv2.flip(frame,1)

        # deal img
        frame = detect.transform_frame(frame)  #处理图像，可能包括调整图像大小、应用YOLO模型进行对象检测


        # get detect result
        detect_result = detect.color_detect(frame)  #用color_detect方法检测图像中物体的颜色和位置
        detect.show_image(frame)  #显示当前处理后的图像

        if detect_result is None:   #为None，则使用continue跳过本次循环的剩余部分           
            continue
        else:            #不是None，说明检测到了物体，获取物体在图像中的位置(x, y)
            x, y = detect_result
            # calculate real coord between cube and mycobot, unit mm
            real_x, real_y = detect.get_position(x, y)  #根据物体在图像中的位置和一些预设的参数（如偏移量），计算机械臂需要到达的实际坐标
            print(real_x, real_y)
            coords_now = basic.get_coords()  #basic模块的get_coords函数来获取当前坐标信息
            if len(coords_now) == 6:
                coords = coords_now
            detect.move(real_x + x_bias, real_y + y_bias)
            print("Detected color:", detect.color)
            cap.close()

   
