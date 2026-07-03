#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse
from move_control import movement
from goto import read_goal, send_goal
from task4_place1 import task4_place1
from task4_place2 import task4_place2
from task3place import task3_place


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="True")
args = parser.parse_args()


y_bias = 85
x_bias = 24
height_bias = -20
y_shift = 40
GRAB_MOVE_SPEED = 50

IMG_SIZE = 640

cap_num = grabParams.cap_num

# show image and waitkey
debug = grabParams.debug

coords_1 = [63.4, 28.4, 363.2, -81.7, -46.4, -5.85]

pos_1 = [65.9, 71.9, 322.9, -80.13, -42.91, -8.14]

pos_2 = [65.9, 162.0, 322.9, -80.33, -42.91, -8.14]

done = grabParams.done

# yolo index
scores = 0
classes = None
CLASSES = ("apple", "clock", "banana","cat ","bird ") #[0,1,2,3,4]

class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()
        self.mv = movement()
        self.yolo = yolo()

        # choose place to set cube
        self.color = 0
        # parameters to calculate camera clipping parameters
        self.x1 = self.x2 = self.y1 = self.y2 = 0        
         # set color HSV
        self.HSV = {
            "yellow": [np.array([20, 43, 46]), np.array([26, 255, 255])],
            "red": [np.array([0, 43, 46]), np.array([10, 255, 255]), np.array([156, 43, 46]), np.array([180, 255, 255])],
            "green": [np.array([50, 43, 46]), np.array([65, 255, 255])],
            "blue": [np.array([100, 80, 46]), np.array([124, 255, 255])],
            "purple": [np.array([125, 43, 46]), np.array([155, 255, 255])],
        }
        # use to calculate coord between cube and mycobot
        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0
        # The coordinates of the cube relative to the mycobot
        self.c_x, self.c_y = IMG_SIZE/2, IMG_SIZE/2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio

    # Adding Head-up
    def grap(self):
        time.sleep(2)
        self.mc.send_angles([0,0,0,0,0,0],100)
        time.sleep(2)
        self.mc.send_coords([64.8,56.4,404.1,(-101.97),(-41.39),7.22],100,0)
        time.sleep(1)
        self.mc.send_coords([66,73.2,378.9,(-93.92),(-40.47),1.67],100,1)
        time.sleep(1)
        self.mc.send_coords([65.9,127.4,381.5,(-102.2),(-41.27),7.69],100,1)
        time.sleep(1)
        self.mc.send_coords([69.6,153.7,374,(-111.85),(-40.18),12.13],60,1)
        time.sleep(1)
        self.mc.set_gripper_state(1, 5)
        time.sleep(1)
        self.mc.send_coords([75.7,141.8,362.5,(-75.76),(-37.93),(-20.47)],100,1)
        time.sleep(1)
        self.mc.send_coords([75.7,70,362.5,(-75.76),(-37.93),(-20.47)],100,0)
        time.sleep(1)
        self.mc.send_coords([58.8, 1.0, 358.6, -26.11, -20.44, -30.38],100,0)
        time.sleep(1)
        self.mc.send_angles([(-45),0,0,0,0,(-39.55)],50)
        time.sleep(2)
        self.mc.send_angles([0,0,0,0,0,0],50)
        time.sleep(2)

    # Without Head-up
    def grap_original(self):
        time.sleep(2)
        self.mc.send_angles([0,0,0,0,0,0],100)
        time.sleep(2)
        self.mc.send_coords([64.8,56.4,404.1,(-101.97),(-41.39),7.22],100,0)
        time.sleep(1)
        self.mc.send_coords([66,73.2,378.9,(-93.92),(-40.47),1.67],100,1)
        time.sleep(1)
        self.mc.send_coords([65.9,127.4,381.5,(-102.2),(-41.27),7.69],100,1)
        time.sleep(1)
        self.mc.send_coords([69.6,153.7,374,(-111.85),(-40.18),12.13],60,1)
        time.sleep(1)
        self.mc.set_gripper_state(1, 5)
        time.sleep(1)
        self.mc.send_coords([75.7,141.8,362.5,(-75.76),(-37.93),(-20.47)],100,1)
        time.sleep(1)
        self.mc.send_coords([75.7,70,362.5,(-75.76),(-37.93),(-20.47)],100,0)
        time.sleep(1)
        self.mc.send_angles([(-45),0,0,0,0,(-39.55)],50)
        time.sleep(2)
        self.mc.send_angles([0,0,0,0,0,0],50)
        time.sleep(2)

    def re_ori(self):
        goal_end = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/goal_end.txt')
        goal_number = 1
        send_goal(goal_number, goal_end)
        return 'Finished.'

    def moblie_fetch_demo1(self):
        # goal_start = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/goal_start.txt')
        # goal_number = 1
        # send_goal(goal_number, goal_start)
        goal_med = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/goal_mid.txt')
        goal_number = 1
        send_goal(goal_number, goal_med)

        self.mv.rotate_to_right_speed(18,0.8)
        goal_end = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/goal_end.txt')
        goal_number = 1
        send_goal(goal_number, goal_end)
        time.sleep(1)
        return 'Finished.'

    def moblie_fetch_demo2(self):
        goal_med = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/goal_mid.txt')
        goal_number = 1
        send_goal(goal_number, goal_med)

        goal2_end = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/goal_end.txt')
        goal_number = 1
        send_goal(goal_number, goal2_end)
        return 'Finished.'
    def back_start(self):
        goal2_end = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/start.txt')
        goal_number = 1
        send_goal(goal_number, goal2_end)
        return 'Finished.'
    # Grasping motion
    def move(self, x=None, y=None):
        global height_bias, done

        basic.move_to_target_coords(pos_1, GRAB_MOVE_SPEED)
        time.sleep(1)
        basic.move_to_target_coords(pos_2, GRAB_MOVE_SPEED)
        time.sleep(1)
        basic.grap(True)
        time.sleep(1) 

        done = True
        print("Done")
        self.mc.set_color(0,255,0)#green, arm is free


    # init mycobot
    def init_mycobot(self): 
        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,80)       
        time.sleep(0.5)   
        basic.grap(False)      
        basic.move_to_target_coords(coords_1, GRAB_MOVE_SPEED)
        time.sleep(1) 
   

    def get_position(self, x, y):
        wx = wy = 0
        if grabParams.grab_direct == "front":
            wx = (self.c_y - y) * self.ratio
            wy = (self.c_x - x) * self.ratio
        elif grabParams.grab_direct == "right":
            wx = (self.c_x - x) * self.ratio
            wy = (y - self.c_y) * self.ratio
        return wx, wy
            


    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (IMG_SIZE, IMG_SIZE))

        return frame
   
    # detect cube color
    def color_detect(self, img):
        # set the arrangement of color'HSV
        x = y = 0
        for mycolor, item in self.HSV.items():
            # transfrom the img to model of gray
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # wipe off all color expect color in range
            mask = cv2.inRange(hsv, item[0], item[1])
            if len(item) == 4:
                mask += cv2.inRange(hsv, item[2], item[3])
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
                    if 110 < min(box[2], box[3]) and  max(box[2], box[3]) < 170
                    # if min(img.shape[0], img.shape[1]) / 10
                    # < min(box[2], box[3])
                    # < min(img.shape[0], img.shape[1]) / 1
                ]
                print(boxes)
                if boxes:
                    # find the largest object that fits the requirements
                    c = max(contours, key=cv2.contourArea)
                    # get the lower left and upper right points of the positioning object
                    x, y, w, h = cv2.boundingRect(c)
                    print(x, y, w, h)
                    # locate the target by drawing rectangle
                    cv2.rectangle(img, (x, y), (x+w, y+h), (153, 153, 0), 2)
                    cv2.circle(img, (x+w/2, y+h/2), 3, (0,0,255), -1)
                    x, y = (x*2+w)/2, (y*2+h)/2
                    # calculate the real coordinates of mycobot relative to the target
                    if mycolor == "yellow":
                        self.color = 1
                    elif mycolor == "red":
                        self.color = 0
                    else:
                        self.color = 1

        cv2.line(img, (0, self.c_y - y_shift), (IMG_SIZE, self.c_y - y_shift), (0,0,255), 2)
        cv2.line(img, (0, self.c_y + y_shift), (IMG_SIZE, self.c_y + y_shift), (0,0,255), 2)

        if abs(x) + abs(y) > 0:
            return x, y
        else:
            return None

    # yolo detector
    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))

        return frame

    def obj_detect(self, img):
        global scores
        global classes
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
            cv2.circle(img_ori, (x, y), 3, (0,0,255), -1)
        cv2.line(img_ori, (0, self.c_y - y_shift), (IMG_SIZE, self.c_y - y_shift), (0,0,255), 2)
        cv2.line(img_ori, (0, self.c_y + y_shift), (IMG_SIZE, self.c_y + y_shift), (0,0,255), 2)
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
        print(args.debug)
        if debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(25) 

    def show_binary_image(self, binary_img):
        if debug and args.debug:
            cv2.imshow("binary_figure", binary_img)
            cv2.waitKey(25) 

    def slow_rolling(self):
       self.mc.send_angle(6,190,20)
    def out_test1(self):
        self.mv.rotate_to_left_speed(2,0.4)
        self.mv.moveback_speed(4,0.06)
        self.mv.rotate_to_right_speed(2,0.4)
        self.mv.moveforward_speed(5,0.06)
        self.mv.rotate_to_right_speed(4.5,0.4)
        goal_temp = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/temp.txt')
        goal_number = 1
        send_goal(goal_number, goal_temp)

        self.mv.moveforward_speed(5,0.06)
        task4_place1()
        self.mv.moveback_speed(4,0.08)
        self.mv.rotate_to_right_speed(2,0.8)

    def out_test2(self):
        self.mv.rotate_to_left_speed(2,0.4)
        self.mv.moveback_speed(4,0.06)
        self.mv.rotate_to_right_speed(2,0.4)
        self.mv.moveforward_speed(5,0.06)
        self.mv.rotate_to_right_speed(4.5,0.4)

        goal_temp = read_goal('/home/robuster/my_work/src/my_robot_1/scripts/temp.txt')
        goal_number = 1
        send_goal(goal_number, goal_temp)

        self.mv.moveforward_speed(5,0.06)
        task4_place2()
        self.mv.moveback_speed(4,0.08)
        self.mv.rotate_to_left_speed(4.5,0.4)
def my_run(my_obj, ori):
    my_obj.run()
    cap = FastVideoCapture(cap_num)
    time.sleep(2) 

    init_num = 0
    nparams = 0
    num = 0
    miss = 0
    cnt_fast = 0
    cnt_slow = 0
    while cv2.waitKey(1) < 0 and not done:
        frame = cap.read()

        # deal img
        frame = my_obj.transform_frame(frame)
        # get detect result
        if ori==1:
            detect_result = my_obj.color_detect(frame)
            my_obj.show_image(frame)
        elif ori==0:
            detect_result = my_obj.obj_detect(frame)
        if detect_result is None:
            if ori == 1:
                my_obj.mv.moveforward_speed(1,0.03)
                cnt_fast = cnt_fast + 1
                time.sleep(0.1)
            elif ori == 0:
                my_obj.mv.moveback_speed(1,0.02)
                cnt_fast = cnt_fast - 1
                time.sleep(0.1)   

        
        else:     

            x, y = detect_result

            if IMG_SIZE / 2 - y_shift <= y <= IMG_SIZE / 2 + y_shift:
                print("ININININININININ")
                cap.close()
                cv2.destroyAllWindows()
                my_obj.grap()
                print(cnt_fast,cnt_slow)

                # while cnt_fast != 0:
                #     if cnt_fast > 0:
                #         my_obj.mv.moveback_speed(1,0.03)
                #         cnt_fast = cnt_fast-1
                #         continue
                #     elif cnt_fast < 0:
                #         my_obj.mv.moveforward_speed(1,0.03)
                #         cnt_fast = cnt_fast + 1
                #         continue

                # while cnt_slow != 0:
                #     if cnt_slow > 0:
                #         my_obj.mv.moveback_speed(1,0.01)
                #         cnt_slow = cnt_slow - 1
                #         continue
                #     elif cnt_slow < 0:
                #         my_obj.mv.moveforward_speed(1,0.01)
                #         cnt_slow = cnt_slow + 1
                #         continue
                break
            elif y > IMG_SIZE / 2 + y_shift:
                my_obj.mv.moveforward_speed(1,0.01)
                cnt_slow = cnt_slow + 1
            elif IMG_SIZE / 2 - y_shift > y:
                my_obj.mv.moveback_speed(1,0.01)
                cnt_slow = cnt_slow - 1
def main():
    detect = Detect_marker()
    result = detect.moblie_fetch_demo1()
    time.sleep(2)
    result = detect.re_ori()

    task3_place()
    detect.mv.moveback_speed(7,0.03)
    time.sleep(3)
    my_run(detect, 1)
    detect.mv.moveforward_speed(1,0.08)
    detect.out_test1()
    result =  detect.moblie_fetch_demo2()
    # # task4_improved.my_run(1,0.15,0.07,1)

    time.sleep(2)
    result = detect.re_ori()
    detect.mv.moveforward_speed(10,0.03)
    time.sleep(3)

    my_run(detect, 0)
    detect.mv.moveback_speed(1,0.08)
    detect.out_test2()
    result = detect.back_start()
def only_move():
    detect = Detect_marker()
    my_run(detect, 0)

if __name__ == "__main__":
    main()
    #only_move()


