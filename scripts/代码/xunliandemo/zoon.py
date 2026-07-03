#encoding: UTF-8
#!/usr/bin/env python2
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

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="True")
args = parser.parse_args()

height_bias = grabParams.height_bias
coords = grabParams.coords_ready
done = grabParams.done

CLASSES = ("apple", "clock", "banana","cat ","bird ") #[0,1,2,3,4]

class Detect_marker(object):

    def __init__(self):
        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on() 

        self.yolo = yolo()

        # parameters to calculate camera clipping parameters
        self.x1 = self.x2 = self.y1 = self.y2 = 0

        # use to calculate coord between cube and mycobot
        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0
        # The coordinates of the grab center point relative to the mycobot

        # The coordinates of the cube relative to the mycobot
        self.c_x, self.c_y = grabParams.IMG_SIZE/2, grabParams.IMG_SIZE/2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio


    # Grasping motion
    def move(self, x, y):
        global height_bias, done
        coords_target = [coords[0]+int(x), coords[1]+int(y), height_bias, coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(coords_target, grabParams.GRAB_MOVE_SPEED)
       

        basic.grap(True)

        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
        time.sleep(3)

        done = True
        print("Done")
        self.mc.set_color(0,255,0)#green, arm is free


    # init mycobot
    def init_mycobot(self): 
        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
        basic.grap(False)      
        time.sleep(1)         
        basic.move_to_target_coords(coords,grabParams.GRAB_MOVE_SPEED) 
 


    # calculate the coords between cube and mycobot
    def get_position(self, x, y):
        # print "self.ratio: ", self.ratio
        # return (-(x - self.c_x)*self.ratio), (-(y - self.c_y)*self.ratio)
        wx = wy = 0
        if grabParams.grab_direct == "front":
            wx = (self.c_y - y) * self.ratio
            wy = (self.c_x - x) * self.ratio
        elif grabParams.grab_direct == "right":
            wx = (self.c_x - x) * self.ratio
            wy = (y - self.c_y) * self.ratio
        return wx, wy
            


  

    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))

        return frame

    #图像处理，适配物体识别
    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))

        return frame
   
    
    # detect object
    def obj_detect(self, img):
        x=y=0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        #加载模型
        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")
        
        t1 = time.time()
        #输入数据处理
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        
        #推理
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]

        
        #获得识别结果
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)
        t2 = time.time()

        # img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if boxes is not None:
            boxes = boxes*5
            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])
            left, top, right, bottom = boxes[0]
            x = int((left+right)/2)
            y = int((top+bottom)/2)
            # print x, y

        self.show_image(img_ori)  

        # Print time (inference-only)
        print("time: " + str(t2-t1) + "s")  

      
        if x+y > 0:
            return x, y
        else:
            return None

    def run(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.init_mycobot()

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(50) 

if __name__ == "__main__":
    # 初始化检测器
    detect = Detect_marker()
    detect.run()

    # 初始化摄像头
    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5)

    # 用于存储识别到的物体名称的列表
    detected_objects = []

    # 循环直到退出条件满足
    init_num = 0
    nparams = 0
    num = 0
    miss = 0
    while cv2.waitKey(1) < 0 and not done:
        # 读取摄像头图像并翻转
        frame = cap.read()
        frame = cv2.flip(frame, 1)  # 水平翻转

        # 进行物体检测
        detect_result = detect.obj_detect(frame)

        # 如果检测到物体
        if detect_result is not None:
            x, y, detected_object = detect_result
            if detected_object:  # 如果检测到了物体
                # 使用 .format() 方法格式化字符串
                print("Detected object: {}".format(detected_object))
                detected_objects.append(detected_object)  # 将物体名称添加到列表

            # 计算实际坐标并执行抓取动作
            real_x, real_y = detect.get_position(x, y)
            detect.move(real_x + grabParams.x_bias, real_y + grabParams.y_bias)

    # 释放摄像头资源
    cap.release()
    # 销毁所有OpenCV窗口
    cv2.destroyAllWindows()

    # 打印所有检测到的物体名称
    print("All detected objects: {}".format(detected_objects))
                print(f"Detected object: {detected_object}")
                detected_objects.append(detected_object)  # 将物体名称添加到列表

            # 计算实际坐标并执行抓取动作
            real_x, real_y = detect.get_position(x, y)
            detect.move(real_x + grabParams.x_bias, real_y + grabParams.y_bias)

    # 释放摄像头资源
    cap.release()
    # 销毁所有OpenCV窗口
    cv2.destroyAllWindows()

    # 打印所有检测到的物体名称
    print("All detected objects:", detected_objects)

   
