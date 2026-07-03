#encoding: UTF-8
#!/usr/bin/env python2

import mobile_to_goal, sonor
from Basic import Rob_basic
from GrabParams import grabParams
from movement import Movement
from sonor import Sonor
from obj_detect import Detect_marker
from obj_follow import Follow_object
from pymycobot.mycobot import MyCobot

import time, rospy, cv2

if __name__ == '__main__':
    # 初始化所有模块

    # mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
    # mc.set_color(255,0,0)
    # time.sleep(1)
    # mc.set_color(0,255,0)follow.open_camera()

    # 视觉搜索物体
    # detect_result = follow.moving_search()


    rospy.init_node('send_goals_python',anonymous=True)
    basic = Rob_basic()                                         #调用Basic的Rob_basic类
    move = Movement()                                           #调用movement的Movement类
    # sonor = Sonor()                                             #调用sonor的Sonor类
    Detect = Detect_marker()                                    #调用obj_detect的Detect_marker类
    follow = Follow_object()                                    #调用obj_follow的Follow_object类

    move.moveforward(0.15, 2)
    # time.sleep(0.5)
    move.right_trapezoidal(280,0.8,1)


    for _ in range(4):
        goal_5 = mobile_to_goal.read_goal("goal_5.txt")
        goal_number = 5
        print("坐标5_初始点接收完毕...")
        mobile_to_goal.send_goal(goal_number, goal_5)
        print("到达坐标5_初始点...")
        time.sleep(0.5)
        for _ in range(2):  
            distance = Sonor().get_sonor_data()
            print(distance)
            Sonor().sonor_control_goal_4()
        time.sleep(1)
        move.right_trapezoidal(98.23, 0.8, 1.5)


        goal_4 = mobile_to_goal.read_goal("goal_4.txt")
        goal_number = 4
        print("坐标4_初始点接收完毕...")
        mobile_to_goal.send_goal(goal_number, goal_4)
        print("到达坐标4_初始点...")
        time.sleep(0.5)
        for _ in range(2):  
            distance = Sonor().get_sonor_data()
            print(distance)
            Sonor().sonor_control_goal_4()
        time.sleep(12)