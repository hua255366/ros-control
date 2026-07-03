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
from pymycobot import MyCobot
from pymycobot.genre import Angle

import time, rospy, cv2

def goal1_gab(obj_info):
    x, y, width, height, label = obj_info
    # real_x, real_y = Detect_marker().get_position(-y,x) #0.2,1)  目标坐标值x＝摄像头返回值-y  y=摄像头返回值x
    if width > 165:
        real_y = grabParams.y_near
    elif 165 >=  width  >= 140:
        real_y = grabParams.y_middle
    else:
        real_y = grabParams.y_far
    print("------------")
    print(real_y)
    print("------------")
    Detect_marker().grab_move(1.6, real_y)#

if __name__ == '__main__':

    rospy.init_node('send_goals_python',anonymous=True)
    basic = Rob_basic()
    move = Movement()
    # sonor = Sonor()
    Detect = Detect_marker()
    follow = Follow_object()
    mc = MyCobot("/dev/arm", 115200)

    move.forward_trapezoidal(1.40,0.7,2)
    # move.moveforward(0.05, 2.5)#0.05,2
    # move.moveforward(0.5, 2)
    # move.moveforward(0.2,1)

# # 第一次
#     # 移动到目标点
#     for _ in range(4):  #6
#         distance = Sonor().get_sonor_data()
#         print(distance)
#         Sonor().sonor_control_goal_3()                      # 超声波精调
#     time.sleep(1)
    move.left_trapezoidal(98.23, 0.8, 1.5)
    time.sleep(1)
    move.forward_trapezoidal(0.41,0.5,1)
    # move.moveforward(0.05,2)  # 补充
    # move.moveforward(0.2,1)                                 # 前进(0.1,2)
    # move.moveforward(0.05,2.2)  # 补充
    time.sleep(0.5)
    
    #调整前后距离
    for _ in range(4):  #10
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()                      # 二次精调
    time.sleep(1)
    basic.move_to_my_angles(grabParams.angles_ready,80,1.5)
    move.left_trapezoidal(98.23, 0.8, 1.5)
    time.sleep(1)

    # move.moveback(0.10,1.0)

   # 机械臂初始化     
    Detect.init_mycobot()

    # 视觉搜索物体
    detect_result = follow.moving_search()
    # time.sleep(1)
   
    #抓取物体
    goal1_gab(detect_result)
    move.forward_trapezoidal(0.04,0.05,0.8)
    time.sleep(0.5)

    # 转身后退到放置位置
    move.right_trapezoidal(99, 0.8, 1.5)
    time.sleep(0.5)

    move.backward_trapezoidal(0.56, 0.4, 3)

    # 根据物体类型放置
    x, y, width, height, label = detect_result
    if label == "clock":##
        basic.move_to_my_coords(grabParams.coords_place_clock,80,2.5)
        basic.grap(False)
        time.sleep(0.5)
        mc.send_angle(Angle.J2.value, 20, 30)
    else:
        basic.move_to_my_coords(grabParams.coords_place_apple,80,1.5)
        basic.grap(False)
        time.sleep(0.5)
        mc.send_angle(Angle.J2.value, 20, 30)

    # 返回准备位置 
    basic.move_to_my_angles(grabParams.angles_ready,60,0.5)
    move.forward_trapezoidal(0.54,0.4,1)   
    basic.move_to_my_coords(grabParams.coords_ready,80,0)


# # # 第二次
    time.sleep(0.5)
    #调整前后距离
    for _ in range(4):  #10
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()                      # 二次精调
    time.sleep(1)
    move.left_trapezoidal(98, 0.8, 1.5)
    time.sleep(1)
    # move.moveback(0.10,0.5)

    # 重新打开摄像头
    follow.open_camera()

    # 视觉搜索物体
    detect_result = follow.moving_search()
    # time.sleep(1)
   
    #抓取物体
    goal1_gab(detect_result)
    move.backward_trapezoidal(0.12,0.08,0.5)
    # move.moveback(0.07, 2)  #后退到合适距离
    time.sleep(0.5)
    move.right_trapezoidal(99, 0.8, 1.5)   #旋转两个90度，即180度,车头对墙，方便后面测距

    time.sleep(0.5)

    # 转身后退到放置位置
    # move.left_trapezoidal(97, 0.8, 1.5)

    move.backward_trapezoidal(0.55, 0.4, 3)

    # 根据物体类型放置
    x, y, width, height, label = detect_result
    if label == "clock":##
        basic.move_to_my_coords(grabParams.coords_place_clock,80,2.5)
        basic.grap(False)
        time.sleep(0.5)
        mc.send_angle(Angle.J2.value, 20, 30)
    else:
        basic.move_to_my_coords(grabParams.coords_place_apple,80,1.5)
        basic.grap(False)
        time.sleep(0.5)
        mc.send_angle(Angle.J2.value, 20, 30)


    # 返回准备位置 
    basic.move_to_my_angles(grabParams.angles_ready,60,0.5)
    move.forward_trapezoidal(0.53,0.2,1)   
    basic.move_to_my_coords(grabParams.coords_ready,80,0)


 # # # 第三次
    time.sleep(0.5)
    #调整前后距离
    for _ in range(4):  #10
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()                      # 二次精调
    time.sleep(1)
    move.left_trapezoidal(98, 0.8, 1.5)
    time.sleep(1)
    move.moveforward(0.10,0.5)


    # 打开摄像头并搜索物体
    follow.open_camera()

    # 视觉搜索物体
    detect_result = follow.moving_search()
    # time.sleep(1)
   
    #抓取物体
    goal1_gab(detect_result)

    move.backward_trapezoidal(0.18,0.08,0.5)
    move.right_trapezoidal(99, 0.8, 1.5)
    # time.sleep(0.5) #旋转两个90度，即180度,车头对墙，方便后面测距

    time.sleep(0.5)

    # 转身后退到放置位置
    # move.left_trapezoidal(97, 0.8, 1.5)
    time.sleep(0.5)
    move.backward_trapezoidal(0.54, 0.4, 3)

    # 根据物体类型放置
    x, y, width, height, label = detect_result
    if label == "clock":##
        basic.move_to_my_coords(grabParams.coords_place_clock,80,2.5)
        basic.grap(False)
        time.sleep(0.5)
        mc.send_angle(Angle.J2.value, 20, 30)
    else:
        basic.move_to_my_coords(grabParams.coords_place_apple,80,1.5)
        basic.grap(False)
        time.sleep(0.5)
        mc.send_angle(Angle.J2.value, 20, 30)


    # 返回准备位置 
    basic.move_to_my_angles(grabParams.angles_ready,60,0.5)
    move.forward_trapezoidal(0.53,0.2,1)   
    basic.move_to_my_coords(grabParams.coords_ready,80,0)


# # # 第四次
    time.sleep(0.5)
    #调整前后距离
    for _ in range(4):  #10
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()                      # 二次精调
    time.sleep(1)
    move.left_trapezoidal(87, 0.8, 1.5)
    time.sleep(1)
    move.moveforward(0.2,0.5)

    # 重新打开摄像头
    follow.open_camera()

    # 视觉搜索物体
    detect_result = follow.moving_search()
    # time.sleep(1)
   
    #抓取物体
    goal1_gab(detect_result)


    move.backward_trapezoidal(0.25,0.08,0.5)
    time.sleep(0.5)
    move.right_trapezoidal(99, 0.8, 1.5)


    # # 转身后退到放置位置
    # move.left_trapezoidal(97, 0.8, 1.5)
    time.sleep(1)

    move.backward_trapezoidal(0.51, 0.4, 3)

    # 根据物体类型放置
    x, y, width, height, label = detect_result
    if label == "clock":##
        basic.move_to_my_coords(grabParams.coords_place_clock,80,2.5)
        basic.grap(False)
        time.sleep(0.5)
        mc.send_angle(Angle.J2.value, 20, 30)
    else:
        basic.move_to_my_coords(grabParams.coords_place_apple,80,1.5)
        basic.grap(False)
        time.sleep(0.5)
        mc.send_angle(Angle.J2.value, 20, 30)


    # 返回准备位置      
    basic.move_to_my_coords(grabParams.coords_ready,30,0)

    # 调整姿态
    move.moveforward(0.15, 2)
    # time.sleep(0.5)
    move.left_trapezoidal(98,0.8,1)

    # # 最终导航到目标点
    # reach_goal4()
    goal_4 = mobile_to_goal.read_goal("goal_4.txt")
    goal_number = 4
    print("坐标4_初始点接收完毕...")
    mobile_to_goal.send_goal(goal_number, goal_4)
    print("到达坐标4_初始点...")
    time.sleep(0.5)
    for _ in range(10):  
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_4()

    # move.left_trapezoidal(98, 0.8, 1.5)
    
    # for _ in range(8):  #8
    #     distance = Sonor().get_sonor_data()    
    #     print(distance)
        
    #     Sonor().sonor_control_goal_3()
