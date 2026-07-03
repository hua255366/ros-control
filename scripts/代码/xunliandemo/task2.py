'''
project:task 2 yolo recognition
version:2-1
author:jiayu
date:2024.6.26
'''
#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
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

global outcome1
global init_num 
global left_num 
global num1 

outcome1 = 7
init_num = 0
left_num = 0
num1 = 7

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
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

    
    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))

        return frame
   
    
    # detect object
    def obj_detect(self, img):
        x=y=0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")
        
        t1 = time.time()
        
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]

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

        cv2.imshow("figure", img_ori)
        cv2.waitKey(50) 

        # Print time (inference-only)
        print("time: " + str(t2-t1) + "s")  

      
        if x+y > 0:
            return x, y,classes[0]
        else:
            return None

    def run(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.init_mycobot()

    

i = 0
detect = Detect_marker()
detect.run()
while i<4:
    cap = cv2.VideoCapture(2)
    #cap.open()
    #time.sleep(0.5)

    while True:
        # read camera
        retval, frame = cap.read()
        frame = cv2.flip(frame,0)
        frame = cv2.flip(frame,1)

        # get detect result
        detect_result = detect.obj_detect(frame)
        if detect_result is None:
            continue
        else:
            i+=1
            x, y,outcome1 = detect_result
            # calculate real coord between cube and mycobot, unit mm
            real_x, real_y = detect.get_position(x, y)
            # print(real_x, real_y)
            coords_now = basic.get_coords()
            if len(coords_now) == 6:
                coords = coords_now
            detect.move(real_x + grabParams.x_bias, real_y + grabParams.y_bias)
            #cap.close()
            break
            
    cap.release()
    cv2.destroyAllWindows()

    time.sleep(0.5)
    if init_num == 0:
        #zuo1
        angles = [-28, -34, -70, 25, -4, 58]
        mc.send_angles(angles,30)
        time.sleep(3)

        mc.set_gripper_value(255, 30)
        time.sleep(3)

        angles = [-28, -22, -70, 18, -4, 58]
        mc.send_angles(angles,30)
        time.sleep(1)

        angles = [11, -23, -39, -29, -3, 58]
        mc.send_angles(angles, 30)
        time.sleep(3)

        print('num1:',num1)
        print('outcome1:',outcome1)
        num1 = outcome1
        #x1=outcome1
        print('111111')
        print('num1:',num1)
        print('outcome1:',outcome1)
        #print('x1:',x1)
        left_num +=1
        init_num += 1
    elif init_num == 1:
        if num1 == outcome1:
            #zuo2
            angles = [-22, -69, 0, -6, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [-22, -60, 0, -10, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            print('222222')

            left_num += 1
            init_num += 1
        else:
            #you1
            angles = [63, -69, 4, -9, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [63, -60, 4, -13, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            print('3333333')

            init_num += 1
    elif init_num == 2:
        if num1 == outcome1:
            # zuo2
            angles = [-22, -69, 0, -6, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [-22, -60, 0, -10, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            left_num += 1
            init_num += 1
        elif left_num == 2:
            # you1
            angles = [63, -69, 4, -9, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [63, -60, 4, -13, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            init_num += 1
        else:
            # you2
            angles = [53, -69, 4, -9, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [53, -60, 4, -13, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(1)   

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            init_num += 1
    else:
        if left_num == 2:
            # you2
            angles = [53, -69, 4, -9, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [53, -60, 4, -13, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)
        else:
            # zuo2
            angles = [-22, -69, 0, -6, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [-22, -60, 0, -10, -4, 58]
            mc.send_angles(angles,30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

