from pymycobot.mycobot import MyCobot
import time
import color_grab_2
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

mc = MyCobot('/dev/ttyACM0',115200)

if __name__ == "__main__":
    while True:
        detect = Detect_marker()
        detect.run()
        
        cap = FastVideoCapture(cap_num)  # 确保这行缩进与下面的代码一致
        time.sleep(0.5)
        
        init_num = 0
        nparams = 0
        num = 0
        miss = 0
        
        while cv2.waitKey(1) < 0 and not done:  # 确保这个循环的代码块正确缩进
            frame = cap.read()
            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)
            
            # deal img
            frame = detect.transform_frame(frame)
            
            # get detect result
            detect_result = detect.color_detect(frame)
            detect.show_image(frame)
            if detect_result is None:            
                continue
            else:
                x, y = detect_result
                # calculate real coord between cube and mycobot, unit mm
                real_x, real_y = detect.get_position(x, y)
                # print(real_x, real_y)
                coords_now = basic.get_coords()
                if len(coords_now) == 6:
                    coords = coords_now
                    # 以下代码应该缩进到与上面的 if 相同级别
                    detect.move(real_x + x_bias, real_y + y_bias)
            
            # 注意：cap.close() 应该在循环外部，以确保摄像头只关闭一次
            cap.close()
