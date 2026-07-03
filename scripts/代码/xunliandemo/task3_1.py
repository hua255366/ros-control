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

rospy.init_node('movement', anonymous=True)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(20)  # 20hz
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

    file_to_read = open(filename)
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

def backward():
    print("backward...")
    move_cmd = Twist()
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

    count = 20
    rate = rospy.Rate(count)  # 20hz

    while count > 0:
        move_cmd.linear.x = -0.2
        pub.publish(move_cmd)
        rate.sleep()
        print("backward...")
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
        angles = [-90, -29, 0, 40, 0, -45]
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

goal1 = read_goal("goal_1.txt")
goal2 = read_goal("goal_2.txt")
goal3 = read_goal("goal_3.txt")

while i < 4:
    send_goal(i, goal1)
    rospy.loginfo(result)
    i += 1
    detect = Detect_marker()
    detect.run()

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
            if (real_x < 15 and real_x > -5) and (real_y > 20 and real_y < 35):
                break
            # cap.close()

    cap.release()
    cv2.destroyAllWindows()

    angles = [-90, -37, -12, 57, -2, -45]
    mc.send_angles(angles, 30)
    time.sleep(3)

    mc.set_gripper_value(40, 30)
    time.sleep(3)

    angles = [-90, 0, 0, 0, 0, -45]
    mc.send_angles(angles, 30)
    time.sleep(3)

    angles = [11, -23, -39, -29, -3, 58]
    mc.send_angles(angles, 30)
    time.sleep(3)

    mc.set_color(0, 255, 0)  # green, arm is free

    send_goal(i, goal2)
    rospy.loginfo(result)
    if init_num == 0:
        # zuo1
        angles = [-28, -34, -70, 25, -4, 58]
        mc.send_angles(angles, 30)
        time.sleep(3)

        mc.set_gripper_value(255, 30)
        time.sleep(3)

        angles = [-28, -22, -70, 18, -4, 58]
        mc.send_angles(angles, 30)
        time.sleep(1)

        angles = [11, -23, -39, -29, -3, 58]
        mc.send_angles(angles, 30)
        time.sleep(3)

        print('num1:', num1)
        print('outcome1:', outcome1)
        num1 = outcome1
        # x1=outcome1
        print('111111')
        print('num1:', num1)
        print('outcome1:', outcome1)
        # print('x1:',x1)
        left_num += 1
        init_num += 1
    elif init_num == 1:
        if num1 == outcome1:
            # zuo2
            angles = [-22, -69, 0, -6, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [-22, -60, 0, -10, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            print('222222')

            left_num += 1
            init_num += 1
        else:
            # you1
            angles = [63, -69, 4, -9, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [63, -60, 4, -13, -4, 58]
            mc.send_angles(angles, 30)
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
            mc.send_angles(angles, 30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [-22, -60, 0, -10, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            left_num += 1
            init_num += 1
        elif left_num == 2:
            # you1
            angles = [63, -69, 4, -9, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [63, -60, 4, -13, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            init_num += 1
        else:
            # you2
            angles = [53, -69, 4, -9, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [53, -60, 4, -13, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            init_num += 1
    else:
        if left_num == 2:
            # you2
            angles = [53, -69, 4, -9, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [53, -60, 4, -13, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)
        else:
            # zuo2
            angles = [-22, -69, 0, -6, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

            mc.set_gripper_value(255, 30)
            time.sleep(3)

            angles = [-22, -60, 0, -10, -4, 58]
            mc.send_angles(angles, 30)
            time.sleep(1)

            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 30)
            time.sleep(3)

    # send_goal(1,goal1)
    # send_goal(1,goal2)
