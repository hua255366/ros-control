'''
project:task 3 yolo recognition
version:3-1
author:jiayu
date:2024.6.30
'''
# encoding: UTF-8
# !/usr/bin/env python2
import cv2
import numpy as np
import time
import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
import math
from GrabParams import grabParams
import basic
import argparse
from geometry_msgs.msg import Twist
from actionlib.action_client import GoalManager
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import re

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="True")
args = parser.parse_args()

#rospy.init_node('movement', anonymous=True)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
#rate = rospy.Rate(20)  # 20hz
move_cmd = Twist()

height_bias = grabParams.height_bias
coords = grabParams.coords_ready
done = grabParams.done

CLASSES = ("apple", "clock", "banana", "cat ", "bird ")  # [0,1,2,3,4]

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

rospy.init_node('send_goals_python', anonymous=True)

global outcome1
global init_num
global left_num
global num1

outcome1 = 7
init_num = 0
left_num = 0
num1 = 7

def send_goal(goal_number, goal):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    client.send_goal(goal)
    str_log = "Send NO. %s Goal !!!" % str(goal_number)
    rospy.loginfo(str_log)

    wait = client.wait_for_result(rospy.Duration.from_sec(60.0))
    if not wait:
        str_log = "The NO. %s Goal Planning Failed for some reasons" % str(goal_number)
        rospy.loginfo(str_log)
    else:
        str_log = "The NO. %s Goal achieved success !!!" % str(goal_number)
        rospy.loginfo(str_log)

def read_goal(filename):
    goal = MoveBaseGoal()

    # file_to_read = open(filename)
    index = 0
    for line in file_to_read.readlines():
        line = line.strip()
        index += 1
        if index == 2:
            pattern = re.compile(r"(?<=\[).*?(?=\])")
            query = pattern.search(line)
            listFromLine = query.group().split(',')
            goal.target_pose.pose.position.x = float(listFromLine[0])
            goal.target_pose.pose.position.y = float(listFromLine[1])
        if index == 3:
            pattern = re.compile(r"(?<=\[).*?(?=\])")
            query = pattern.search(line)
            listFromLine = query.group().split(',')
            goal.target_pose.pose.orientation.z = float(listFromLine[2])
            goal.target_pose.pose.orientation.w = float(listFromLine[3])

    print(goal.target_pose.pose)

    return goal

count = 20
rate = rospy.Rate(count)  # 20hz

def moveback1(time_seconds,speed):
    print("backward...")
    count = 20*time_seconds
    move_cmd = Twist()

    while count > 0:
        move_cmd.linear.x = speed #m/s
        pub.publish(move_cmd)
        rate.sleep()
        count -= 1

def moveforward1(time_seconds,speed):      
    print("forward...")
    count = 20*time_seconds
    move_cmd = Twist()

    while count > 0:
        move_cmd.linear.x = speed #m/s
        pub.publish(move_cmd)
        rate.sleep()
        count -= 1


def rotate_to_right1(time_seconds):
    print("rotate_to_right...")
    count = 20*time_seconds
    move_cmd = Twist()

    while count > 0:
        move_cmd.angular.z = -1 #rad/s
        pub.publish(move_cmd)
        rate.sleep()
        count -= 1


def rotate_to_left1(time_seconds,speed):
    print("rotate_to_left...")
    count = 20*time_seconds
    move_cmd = Twist()

    while count > 0:
        move_cmd.angular.z = speed #rad/s
        pub.publish(move_cmd)
        rate.sleep()            
        count -= 1

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
        self.c_x, self.c_y = grabParams.IMG_SIZE / 2, grabParams.IMG_SIZE / 2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio

    # init mycobot
    def init_mycobot(self):

        angles = [-90, 0, 0, 0, 0, -45]
        self.mc.send_angles(angles, 30)
        basic.grap(False)
        time.sleep(3)
        # basic.move_to_target_coords(coords,grabParams.GRAB_MOVE_SPEED)

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
        x = y = 0
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
            boxes = boxes * 5
            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])
            left, top, right, bottom = boxes[0]
            x = int((left + right) / 2)
            y = int((top + bottom) / 2)
            # print x, y

        cv2.imshow("figure", img_ori)
        cv2.waitKey(2)

        # Print time (inference-only)
        print("time: " + str(t2 - t1) + "s")

        if x + y > 0:
            return x, y, classes[0]
        else:
            return None

    def run(self):
        self.mc.set_color(0, 0, 255)  # blue, arm is busy
        self.init_mycobot()


i = 0

# goal1 = read_goal("goal_right_center.txt")
goal2 = read_goal("goal_right_dingwei.txt")
goal3 = read_goal("goal_right_end.txt")

while i < 4:
    if i == 0 :
        #send_goal(i, goal1)
        time.sleep(2)
        #rotate_to_left1(3,0.4)
        time.sleep(1)
        #send_goal(i, goal2)
        time.sleep(2)
        detect = Detect_marker()
        detect.run()
        time.sleep(2)
        moveforward1(5.5,0.2)  #go1
        time.sleep(1)

        #rotate_to_right1(1.3)
        #time.sleep(1)
        #moveback1(0.34,-0.3)
        #time.sleep(1)
        #rotate_to_right1(1.3)
        #time.sleep(1)

        rotate_to_left1(1.3,1)
        time.sleep(1)
        moveforward1(1,0.3)
        time.sleep(1)
        rotate_to_left1(1.3,1)
        time.sleep(1)


        '''
        rotate_to_right1(0.3)
        #rotate_to_left1(1.4)
        time.sleep(1)
        moveforward1(0.6,0.4)
        time.sleep(1)
        rotate_to_left1(1,0.5)
        time.sleep(1)
        moveback1(1,-0.22)
        time.sleep(1)
        '''
    
    #rospy.loginfo(result)
    i += 1
    

    angles = [-90, -29, 0, 40, 0, -45]
    mc.send_angles(angles, 30)
    time.sleep(3)
    
    cap = cv2.VideoCapture(2)
    while True:
        move_cmd.linear.x = 0.02  # m/s
        move_cmd.linear.z = 0  # m/s
        pub.publish(move_cmd)

        retval, frame = cap.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)

        # get detect result
        detect_result = detect.obj_detect(frame)
        if detect_result is None:
            continue
        else:
            x, y, outcome1 = detect_result
            # calculate real coord between cube and mycobot, unit mm
            real_x, real_y = detect.get_position(x, y)
            print(real_x, real_y)
            if (real_x < 20 and real_x > -10) and (real_y > 0 and real_y < 50):
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # cap.close()

    cap.release()
    cv2.destroyAllWindows()



    angles = [-94.92, -50.44, 68.46, -19.33, 3.86, -45.96]
    mc.send_angles(angles, 30)
    time.sleep(3)

    angles = [-87.27, -29.79, -40.95, 142.11, -4.21, -48.25]
    mc.send_angles(angles, 30)
    time.sleep(3)

    angles = [-90.87, -25.22, -41.13, 69.16, -0.08, -48.51]
    mc.send_angles(angles, 30)
    time.sleep(3)

    mc.set_gripper_value(40, 30)
    time.sleep(1.5)

    angles = [-90, 0, 0, 0, 0, -45]
    mc.send_angles(angles, 50)
    time.sleep(1.5)

    angles = [0, 0, 0, 0, 0, 0]
    mc.send_angles(angles, 50)
    time.sleep(3)

    angles = [11, -23, -39, -29, -3, 58]
    mc.send_angles(angles, 50)
    time.sleep(1.5)

    #moveback1(0.8,-0.22)
    #time.sleep(1)
    #rotate_to_left1(0.2,1)
    #time.sleep(1)
    if i==1:
        #moveback1(0.1,-0.1)
        time.sleep(1)
    elif i==2:
        moveback1(0.5,-0.1)
        time.sleep(1)
    elif i==3:
        moveback1(2,-0.1)
        time.sleep(1)
    elif i==4:
        moveback1(3.2,-0.1)
        time.sleep(1)

    rotate_to_right1(1.3)
    time.sleep(1)

    moveback1(2.7,-0.2)
    time.sleep(2)

    #send_goal(i, goal1)

    #time.sleep(1)
    #rotate_to_left1(1.3,1)
    #time.sleep(1)
    #moveback1(0.7,-0.22)
    #time.sleep(1)

    #rospy.loginfo(result)
    if init_num == 0:
        # zuo1   
        angles = [-152, -64, 6, -13, -3, 58]
        mc.send_angles(angles,30)
        time.sleep(3)

        mc.set_gripper_value(255, 30)
        time.sleep(3)

        angles = [11, -23, -39, -29, -3, 58]
        mc.send_angles(angles, 30)
        time.sleep(3)

        num1 = outcome1
        left_num += 1
        init_num += 1
    elif init_num == 1:
        if num1 == outcome1:
            # zuo2           
            angles = [-140, -64, 6, -13, -3, 58]
            mc.send_angles(angles,40)
            time.sleep(2)

            mc.set_gripper_value(255, 40)
            time.sleep(2)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)
            time.sleep(2)

            print('222222')

            left_num += 1
            init_num += 1
        else:
            # you1
            angles = [163, -64, 6, -13, -3, 58]
            mc.send_angles(angles,40)
            time.sleep(2)  

            mc.set_gripper_value(255, 40)
            time.sleep(2)   

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)
            time.sleep(2)

            print('3333333')

            init_num += 1
    elif init_num == 2:
        if num1 == outcome1:
            # zuo2
            angles = [-140, -64, 6, -13, -3, 58]
            mc.send_angles(angles,40)
            time.sleep(2)

            mc.set_gripper_value(255, 40)
            time.sleep(2)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)
            time.sleep(2)

            left_num += 1
            init_num += 1
        elif left_num == 2:
            # you1
            angles = [163, -64, 6, -13, -3, 58]
            mc.send_angles(angles,40)
            time.sleep(2) 

            mc.set_gripper_value(255, 40)
            time.sleep(2)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)
            time.sleep(2)

            init_num += 1
        else:
            # you2
            angles = [170.15, -91.31, 4.83, 40.42, -10.72, 66.7]
            mc.send_angles(angles,40)
            time.sleep(2)

            mc.set_gripper_value(255, 40)
            time.sleep(2)

            angles = [167.6, -37.26, 3.77, -21.88, 3.07, 28.74]
            mc.send_angles(angles,40)
            time.sleep(2)
            

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)
            time.sleep(2)

            init_num += 1
    else:
        if left_num == 2:
            # you2
            angles = [170.15, -91.31, 4.83, 40.42, -10.72, 66.7]
            mc.send_angles(angles,40)
            time.sleep(2) 

            mc.set_gripper_value(255, 40)
            time.sleep(2)

            angles = [167.6, -37.26, 3.77, -21.88, 3.07, 28.74]
            mc.send_angles(angles,40)
            time.sleep(2)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)
            time.sleep(2)
        else:
            # zuo2
            angles = [-140, -64, 6, -13, -3, 58]
            mc.send_angles(angles,40)
            time.sleep(2)

            mc.set_gripper_value(255, 40)
            time.sleep(2)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)
            time.sleep(2)
    #moveforward1(0.6,0.3)
    #time.sleep(1)

    angles = [-90, -29, 0, 40, 0, -45]
    mc.send_angles(angles, 40)
    time.sleep(2)

    #xia yi ci
    if i<4:
        moveforward1(2.68,0.2)
        time.sleep(3)

        if i<1:
            rotate_to_left1(3.32,0.5)
            time.sleep(2)
        else:
            rotate_to_left1(3.18,0.5)
            time.sleep(2)

    


mc.set_color(0, 255, 0)  # green, arm is free

angles = [-83.23, -140.53, 140.97, 58.71, -127.61, 5.71]
mc.send_angles(angles, 40)
time.sleep(3)

moveforward1(0.9,0.2)
time.sleep(3)

rotate_to_left1(3.15,0.5)
time.sleep(2)

moveforward1(8,0.2)  #go1
time.sleep(1)

rotate_to_left1(0.85,0.5)
time.sleep(2)

moveforward1(5,0.2)  #go1
time.sleep(1)

#send_goal(1, goal3)