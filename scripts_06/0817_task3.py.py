# encoding: UTF-8
# !/usr/bin/env python2
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
import rospy
from move_control import movement
#from 0705task3_nav import DirectNavigator
import tf
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Quaternion, Twist
from _0816sonor import listen_for_distance


parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="True")
args = parser.parse_args()
cap = FastVideoCapture(grabParams.cap_num)
CLASSES = ("apple", "clock", "banana", "cat ", "bird ")  # [0,1,2,3,4]
mc = MyCobot("/dev/arm", 115200)
m = movement()

# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx
# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx  map_choice!!! NOTICE!!! notice!!!

map_choice = -1 # if(red_left), map_choice = 1;  if(blue_right), map_choice= -1
# if(red_left), map_choice = 1;  
# if(blue_right), map_choice= -1 

obstacle_side = 0 # if obstacle on left side, obstacle_side = 0; elif on right side, obstacle_side = 7

# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx  map_choice!!! NOTICE!!! notice!!!
# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx

# 扫描坐标
angles_top_ready = [(map_choice * 90.0), 5.36, -2.9, -6, 0, -45]

# 准备坐标
angles_ready_grab = [(map_choice * 90.0), -65.56, 103.53, -30.45, 0, -45]

# 抓取坐标
angles_grab = [(map_choice * 90.0), -65.56, 44.12, 30, 0, -45]


# 抬起坐标
angles_raise = [0, -30, 30, 69.43, -13.62, 0]

# 放下坐标
angles_putdown = [0, -90, 30, 15, 0, -45]


Speed = 90
# height_bias = 150
# # coords = [229.0, -35.2, 231.5, -179.48, 1.29, -132.79]
# coords = [173.0, -68.0, 281.0, -170.78, 2.79, -134.93]
# done = grabParams.done
# speed_robot = 50
# speed_robot_line = 40

class movement_speed(object):

    def __init__(self):
        super(movement_speed, self).__init__()

        rospy.init_node('movement', anonymous=True)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(20) # 20hz

    #小车后退
    def moveback(self, time_seconds,speed):
        print("backward...")
        count = 20*time_seconds
        move_cmd = Twist()
        while count > 0:
            move_cmd.linear.x = -speed #m/s (0.05)
            self.pub.publish(move_cmd)
            self.rate.sleep()
            count -= 1

    def moveforward(self, time_seconds, speed):        
        print("forward...")
        count = 20*time_seconds
        move_cmd = Twist()
        while count > 0:
            move_cmd.linear.x = speed #m/s
            self.pub.publish(move_cmd)
            self.rate.sleep()
            count -= 1

# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx
    
    #小车右转
    def rotate_to_right(self, time_seconds,speed):
        if map_choice == 1: # red_left
            m_speed.rotate_to_right_2(time_seconds, speed)
        elif map_choice == -1: # blue_right
            m_speed.rotate_to_left_2(time_seconds, speed)
    #小车左转
    def rotate_to_left(self, time_seconds,speed):
        if map_choice == 1: # red_left
            m_speed.rotate_to_left_2(time_seconds, speed)
        elif map_choice == -1: # blue_right
            m_speed.rotate_to_right_2(time_seconds, speed)

    #小车右转
    def rotate_to_right_2(self, time_seconds,speed):
        print("rotate_to_right...")
        count = 20*time_seconds
        move_cmd = Twist()
        while count > 0:
            move_cmd.angular.z = -speed #rad/s  (0.2)
            self.pub.publish(move_cmd)
            self.rate.sleep()
            count -= 1

    #小车左转
    def rotate_to_left_2(self, time_seconds,speed):
        print("rotate_to_left...")
        count = 20*time_seconds
        move_cmd = Twist()
        while count > 0:
            move_cmd.angular.z = speed #rad/s 
            self.pub.publish(move_cmd)
            self.rate.sleep()            
            count -= 1

# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx


m_speed = movement_speed()

class DirectNavigator:
    def __init__(self):
        # rospy.init_node('direct_navigator', anonymous=True)

        # Set up the action client for move_base
        self.move_base_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.move_base_client.wait_for_server()

        rospy.loginfo("Direct Navigator ready to send goals")
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    def spin_and_scan(self, duration=8, cycles=2):
        """原地旋转扫描"""
        move_cmd = Twist()

        for _ in range(cycles):
            start_time = time.time()
            move_cmd.linear.x = 0.0
            move_cmd.angular.z = 0.4  # 设置旋转速度

            while time.time() - start_time < duration:
                self.cmd_vel_pub.publish(move_cmd)
                rospy.sleep(0.1)

            # 结束旋转后停止
            move_cmd.angular.z = 0.0
            self.cmd_vel_pub.publish(move_cmd)
            time.sleep(0.7)  # 旋转间歇，可根据需要调整

    def navigate_to_goal(self, x, y, yaw):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        # Set the goal position and orientation
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        quaternion = tf.transformations.quaternion_from_euler(0, 0, yaw)
        goal.target_pose.pose.orientation = Quaternion(*quaternion)

        rospy.loginfo("Sending goal to move_base: x=%f, y=%f, yaw=%f", x, y, yaw)

        self.move_base_client.send_goal(goal)

        success = self.move_base_client.wait_for_result()

        if not success:
            rospy.logerr("Failed to reach the goal")
        else:
            state = self.move_base_client.get_state()
            if state == actionlib.GoalStatus.SUCCEEDED:
                rospy.loginfo("Successfully reached the goal")
            elif state == actionlib.GoalStatus.ABORTED:
                rospy.logwarn(
                    "Goal aborted. Possible reasons: Obstacle blocking the path, path planning failure, or configuration issues.")
            else:
                rospy.logwarn("Reached the goal with status: %s", state)



    def run(self,(x1, y1, z1)):
        # 原地旋转扫描
        self.spin_and_scan()

        # Example coordinates to navigate to (modify these values as needed)
        target_x = x1
        target_y = y1
        target_yaw = z1  # 90 degrees in radians


        self.navigate_to_goal(target_x, target_y, target_yaw)
        rospy.loginfo("Finished navigation.")

    def run2(self,(x1, y1, z1)):
        # 原地旋转扫描
        #self.spin_and_scan()

        # Example coordinates to navigate to (modify these values as needed)
        target_x = x1
        target_y = y1
        target_yaw = z1  # 90 degrees in radians


        self.navigate_to_goal(target_x, target_y, target_yaw)
        rospy.loginfo("Finished navigation.")


# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx
# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx
    # def Map_transformation_for_X(self, position_x):

    #     axis_of_symmetry = 0.39716 # Map about x = 0.39716 symmetry

    #     if map_choice == 1: # red_left
    #         return position_x
    #     elif map_choice == -1: # blue_right
    #         return (2 * axis_of_symmetry - position_x)
    #     else:
    #         print("ERROR map_choice!!! ERROR map_choice!!! ERROR map_choice!!! exit(1)!!!")
    #         exit(1)

    # def Map_transformation_for_Yaw(self, position_x):

    #     axis_of_symmetry = 1.57 # Map about yaw = 0.39716 symmetry

    #     if map_choice == 1: # red_left
    #         return position_x
    #     elif map_choice == -1: # blue_right
    #         return (2 * axis_of_symmetry - position_x)
    #     else:
    #         print("ERROR map_choice!!! ERROR map_choice!!! ERROR map_choice!!! exit(1)!!!")
    #         exit(1)

    def map_choice_of_positions(self, i):
        # blue_right_scan_0816
        positions_blue_right = [(-0.05,-0.35,1.57), # 0: middle_Obstacle_Left_Side 
                                (0.16,0.1,0),  # 1: shelf_front
                                (-0.33,0.1,3.14), # 2: desk
                                (-0.15,-0.05,-1.57), # 3: home_prepare (middle向home转)
                                (-0.6, -2.27, -1.7), # 4: home
                                (0.17,0.1+0.06*(move_forward.get_execution_count()-1),0), # 5: restart_1 (shelf_front的y平移)
                                (-0.07, 0.05, 3.14), # 6: timeout_1 ((middle转半圈))
                                (-0.19,0,1.26)]# 7: middle_Obstacle_Right_Side

        # red_left_make
        # positions_red_left  =  [(-0.39,0,-1.57), # 0: middle 
        #                         (-0.05,0.05,0),  # 1: shelf_front
        #                         (-0.52,-0.17,3.14), # 2: desk
        #                         (-0.42,0,1.57), # 3: home_prepare (middle向home转)
        #                         (-0.8, 2.3, 0), # 4: home
        #                         (-0.05,0.02-0.03*(move_forward.get_execution_count()-1),0), # 5: restart_1 (shelf_front的y平移)
        #                         (-0.39, 0, 3.14)] # 6: timeout_1 ((middle转半圈))

        # red_left_scan_0816
        positions_red_left = [(-0.08,0.2,-1.57), # 0: middle_Obstacle_Left_Side 
                            (0.2,0.1,0),  # 1: shelf_front
                            (-0.23,-0.05,3.14), # 2: desk
                            (-0.07,0.25,1.57), # 3: home_prepare (middle向home转)
                            (-0.47, 2.39, 1.7), # 4: home
                            (0.22,0.1-0.06*(move_forward.get_execution_count()-1),0), # 5: restart_1 (shelf_front的y平移)
                            (0, 0, 3.14), # 6: timeout_1 ((middle转半圈))
                            (0.2,0.1,0)] # 7: middle_Obstacle_Right_Side

        if map_choice == 1: # red_left
            print('return position[', i, ']:', positions_red_left[i])
            return positions_red_left[i]
        elif map_choice == -1: # blue_right
            print('return position[', i, ']:', positions_blue_right[i])
            return positions_blue_right[i]
        else:
            print("ERROR map_choice!!! ERROR map_choice!!! ERROR map_choice!!! exit(1)!!!")
            exit(1)

# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx
# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx


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
        self.result_class = 0


    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))

        return frame

    # 图像处理，适配物体识别
    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))

        return frame

    # detect object
    def obj_detect(self, img):
        x = y = 0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        # 加载模型
        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")

        t1 = time.time()
        # 输入数据处理
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)

        # 推理
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]

        # 获得识别结果
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)
        t2 = time.time()

        # img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if boxes is not None:
            boxes = boxes * 5
            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])
            left, top, right, bottom = boxes[0]
            x = int((left + right) / 2)
            y = int((top + bottom) / 2)
            self.result_class = classes[0]
            # print x, y

        self.show_image(img_ori)

        # Print time (inference-only)
        print("time: " + str(t2 - t1) + "s")
#####################################################################################################
        if (x + y > 0) and (scores[0] > 0.55):##############################and (scores[0] > 0.65)
            return x, y, classes[0]
        else:
            return None
#####################################################################################################
    def run(self):
        self.mc.set_color(0, 0, 255)  # blue, arm is busy
        self.init_mycobot()

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(50)


class MoveForwardUntilDetected:
    def __init__(self):
        self.mc = mc
        #rospy.init_node('movement', anonymous=True)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(20)
        self.move_cmd = Twist()
        self.move_cmd.linear.x = 0.03  # 设置线速度
        self.detect = Detect_marker()
        self.target_detected = False
        self.distance_ok = False
        self.execution_count = 0  # 执行命令的计数器
        self.start_time = time.time()  # 记录开始时间
        self.forward_time = 0
        self.runtime = False

        print('finished init')

    def execute_command_and_restart(self, result_class):
        """执行抓取放置后后重新开始前进检测"""
        # 准备抓取
        self.mc.send_angles(angles_ready_grab, Speed)
        print("执行抓取准备动作")
        time.sleep(1)

        # 抓取过渡动作
        self.mc.send_angles([(map_choice * 90.0), -65.56, 90, -29, 0, -45],90)
        time.sleep(0.05)
        self.mc.send_angles([(map_choice * 90.0), -65.56, 78, -26, 0, -45],90)
        time.sleep(0.05)
        self.mc.send_angles([(map_choice * 90.0), -65.56, 67, -16, 0, -45],90)
        time.sleep(0.05)
        self.mc.send_angles([(map_choice * 90.0), -65.56, 57, -6, 0, -45],90)
        time.sleep(0.05)
        self.mc.send_angles([(map_choice * 90.0), -65.56, 50, 6, 0, -45],90)
        time.sleep(0.05)
        self.mc.send_angles([(map_choice * 90.0), -65.56, 41, 17, 0, -45],90)
        time.sleep(0.05)

        # 抓取时姿势
        self.mc.send_angles(angles_grab,Speed)
        time.sleep(0.3)
        # 抓取
        basic.grap(True)
        print("抓取动作")
        time.sleep(0.3)

        # 抬起
        self.mc.send_angles(angles_raise, Speed)
        print("抬起动作")
        time.sleep(0.1)

        # 后退
        # if (self.execution_count == 0) and (0.7-self.forward_time*0.15 > 0):
        #     m_speed.moveforward(0.7-self.forward_time*0.15, 0.2)
        # if self.execution_count == 1:
            # m_speed.moveback(self.forward_time*0.15, 0.2)
        if self.execution_count == 2:
            m_speed.moveback(self.forward_time*0.15, 0.2)
        if self.execution_count == 3:
            m_speed.moveback(self.forward_time*0.13, 0.2)



        # 旋转（向左）
        m_speed.rotate_to_left(3.33, 0.5)   # 旋转90度
        print("旋转（向左）")
        time.sleep(1)

        # 后退
        m_speed.moveback(0.8, 0.25)        # 后退(3.2,0.18)
        print("后退")
        time.sleep(0.5)

        # 旋转
        m_speed.rotate_to_right(3.30, 1)
        time.sleep(0.3)

        # task3 desk (# zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx zqx )
        navigator.run2(navigator.map_choice_of_positions(2)) # 2: desk
        m_speed.moveforward(0.2,0.25)

        # 放置
        print('result_class:',result_class)
        if result_class == 0:
            angles_putdown[0] -= 25
        if result_class == 1:
            angles_putdown[0] += 25
        print('angles_putdown[0]:', angles_putdown[0])

        self.mc.send_angles(angles_putdown, Speed)
        print("准备放置")
        if result_class == 0:
            angles_putdown[0] += 25
        if result_class == 1:
            angles_putdown[0] -= 25
        time.sleep(1.2)

        # 松爪
        basic.grap(False)
        print("松爪")
        time.sleep(0.1)


        # 抬起（复位）
        self.mc.send_angles(angles_raise, Speed)
        print("抬起（复位）")
        #time.sleep(1.2)
        time.sleep(0.5)




        self.target_detected = False  # 重置目标检测标志
        self.execution_count += 1  # 命令执行次数加一
        if self.execution_count >= 4 or time.time() - self.start_time > 420: # 480秒等待时间
            print("达到执行次数上限或超时，程序停止。")
            m_speed.moveback(1,0.5)
            navigator.run2(navigator.map_choice_of_positions(3)) # 3: home_prepare
            navigator.run2(navigator.map_choice_of_positions(4)) # 4: home
            print('go home')
            rospy.signal_shutdown("Execution completed or timeout.")
        else:
            # 后退
            m_speed.moveback(0.9,0.4)
            print("后退")
            # 旋转
            m_speed.rotate_to_left(4, 0.75)
            time.sleep(0.3)
            # 前进
            navigator.run2(navigator.map_choice_of_positions(5)) # 5: restart_1
            print(navigator.map_choice_of_positions(5))
            print("前进")
            self.sonor_start_movement()
            # m_speed.moveforward(3.8, 0.2)
            # time.sleep(1)

            # 旋转（向右）
            #navigator.run2(0,0.02-0.03*(self.execution_count-1),-1.57)
            m_speed.rotate_to_right(3.33, 0.5)  # 旋转90度
            print("旋转（向右）")
            # time.sleep(1)

            mc.send_angles(angles_top_ready, Speed)
            time.sleep(1)
            print("抬起机械臂准备")
            self.start_movement()
    
    def moveforward_runtime(self):
        print('Warning:runtime:')
        m_speed.rotate_to_left(9, 0.17)
        m_speed.moveback(1, 0.2)
        navigator.run2(navigator.map_choice_of_positions(6)) # 6: timeout_1 
        m_speed.rotate_to_left(24, 0.17)
        navigator.run2(navigator.map_choice_of_positions(1)) # 1: shelf_front
        print('ready to task3')
        self.sonor_start_movement()
        m_speed.rotate_to_right(3.33, 0.5)  # 旋转90度
        # navigator.run2(0,0.05,-1.57)
        time.sleep(0.1)
        m_speed.moveback(0.15, 0.2)
        self.start_movement()


    def start_movement(self):
        self.move_cmd.linear.x = 0.02  # 每次开始前重置线速度
        self.target_detected = False  # 确保目标检测标志被重置
        self.forward_time = time.time()
        while not rospy.is_shutdown() and not self.target_detected:

            frame = cap.read()
            target_info = self.detect.obj_detect(frame)
            self.forward_time = time.time()-self.forward_time
            if not self.runtime:
                if 500 > self.forward_time >= (15-self.execution_count*2):
                    print('!!!!!moveforward runtime:', self.forward_time)
                    self.runtime = True
                    self.stop_movement()
                    self.moveforward_runtime() 
            else:
                if 500 > self.forward_time >= 15:
                    print('!!!!!moveforward runtime(>=15):', self.forward_time)
                    self.stop_movement()
                    self.moveforward_runtime() 
            if (target_info is not None) and (self.forward_time < (15-self.execution_count*2)):
                _, y ,result_class= target_info  # 假设返回的是(x, y)，我们只需y来判断是否超过屏幕一半
                screen_midpoint = frame.shape[1] // 2
                if y is not None and (screen_midpoint-45) < y < (screen_midpoint+35):
                    print('y-screen_midpoint: ', y-screen_midpoint)
                    print("目标已超过右半屏，停止前进，准备执行命令。")
                    self.runtime = False
                    # self.forward_time = time.time()-self.forward_time
                    print('forward_time:', self.forward_time)
                    self.target_detected = True
                    self.stop_movement()
                    self.execute_command_and_restart(result_class)  # 执行命令并准备重新开始
                    break
            self.pub.publish(self.move_cmd)
            self.rate.sleep()
        print("startMmovement_end")


    def sonor_start_movement(self):
        self.move_cmd.linear.x = 0.03  # 每次开始前重置线速度
        self.distance_ok = False  # 确保目标检测标志被重置
        while not rospy.is_shutdown() and not self.distance_ok:
            distance = listen_for_distance()
            print("Distance: {:.2f}".format(distance))
            if distance <= 0.26:
                print("停止前进，已经接近任务三货架。")
                self.distance_oka = True
                self.stop_movement()
                break
            self.pub.publish(self.move_cmd)
            self.rate.sleep()

    def stop_movement(self):
        self.move_cmd.linear.x = 0
        self.pub.publish(self.move_cmd)

    def get_execution_count(self):
        return self.execution_count

if __name__ == "__main__":
    try:
        move_forward = MoveForwardUntilDetected()
        navigator = DirectNavigator()
        # 抬起机械臂准备
        mc.send_angles(angles_top_ready, Speed)
        # print("抬起机械臂准备")
        # 松爪
        basic.grap(False)
        print("松爪")
        #time.sleep(0.5)
        
        navigator.run(navigator.map_choice_of_positions(obstacle_side)) # 0 or 7: middle_Obstacle_Left or Right_Side
        print('go to task3') 
        # m_speed.rotate_to_left(12, 0.17)
        #time.sleep(3)

        
        
        navigator.run2(navigator.map_choice_of_positions(1)) # 1: shelf_front
        print('ready to task3')
        move_forward.sonor_start_movement()
        m_speed.rotate_to_right(3.33, 0.5)  # 旋转90度
        #navigator.run2(0,0.05,-1.57)
        time.sleep(0.1)
        m_speed.moveback(0.15, 0.2)

        # m.moveforward(0.7)
        # m.rotate_to_right(9.05)

        # m.moveback(1)
        # # 松爪
        # basic.grap(False)
        # print("松爪")


        move_forward.start_movement()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation terminated.")


        # target_x = 2.21
        # target_y = 0.32
        # target_yaw = 1.56  # 90 degrees in radians

