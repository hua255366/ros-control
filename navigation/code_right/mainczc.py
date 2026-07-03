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

def reach_goal1():
    for _ in range(12):  
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_3()
    time.sleep(0.5)
    move.rotate_to_left(0.55,2.7)
    time.sleep(0.5)
    move.moveforward(0.1,1.2)
    time.sleep(0.5)
    for _ in range(10):  
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()
    time.sleep(0.5)
    move.rotate_to_right(0.55, 2.7) # (0.55, 2.7)旋转90°   ,,,比90多一点
   
    # Detect_marker().init_mycobot()

def reach_goal2():
    # goal_2 = mobile_to_goal.read_goal("goal_2.txt")
    # goal_number = 2
    # print("坐标2_放置点接收完毕...")
    # mobile_to_goal.send_goal(goal_number, goal_2)
    # print("到达坐标2_放置点...")
    for _ in range(6):  
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_3()
    time.sleep(0.5)    
    move.rotate_to_right(0.55,2.7)
    time.sleep(0.5)
    move.moveforward(0.15, 3.8)

def reach_goal3():
    goal_3 = mobile_to_goal.read_goal("goal_3.txt")
    goal_number = 3
    print("坐标3_初始点接收完毕...")
    mobile_to_goal.send_goal(goal_number, goal_3)
    print("到达坐标3_初始点...")

def reach_goal4():
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

def goal1_gab(obj_info):
    x, y, width, height, label = obj_info
    real_x, real_y = Detect_marker().get_position(-y,x)
    print(real_x,real_y)
    Detect_marker().grab_move(real_x + grabParams.x_bias , grabParams.y + grabParams.y_bias)

if __name__ == '__main__':
    # mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
    # mc.set_color(255,0,0)
    # time.sleep(1)
    # mc.set_color(0,255,0)
    rospy.init_node('send_goals_python',anonymous=True)
    basic = Rob_basic()
    move = Movement()
    # sonor = Sonor()
    Detect = Detect_marker()
    follow = Follow_object()

    move.moveforward(0.05, 2.5)#0.05,2
    move.moveforward(0.5, 2)
    move.moveforward(0.2,1)

# 第一次
    # 移动到目标点
    for _ in range(4):  #6
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_3()                      # 超声波精调
    time.sleep(1)
    move.rotate_to_left(0.55,2.7)                          # 左转(0.55,2.7)
    time.sleep(1)
    move.moveforward(0.05,2)  # 补充
    move.moveforward(0.2,1)                                 # 前进(0.1,2)
    move.moveforward(0.05,2.2)  # 补充
    time.sleep(0.5)
    
    #调整前后距离
    for _ in range(4):  #10
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()                      # 二次精调
    time.sleep(1)
    move.rotate_to_right(0.55, 2.7) # (0.55, 2.7)旋转90°      # 右转复位
    time.sleep(1)

    for _ in range(6):  
        distance = Sonor().get_sonor_data()
        Sonor().sonor_control_goal_2()
        time.sleep(0.5)


   # 机械臂初始化     
    Detect.init_mycobot()

    # 视觉搜索物体
    detect_result = follow.moving_search()
   
    #抓取物体
    goal1_gab(detect_result)
    

   #调整前后距离
    move.moveforward(0.05,1.5)
    for _ in range(5):  #8
        distance = Sonor().get_sonor_data()
        print(distance)
        # Sonor().sonor_control_goal_3()
        Sonor().sonor_control_goal_5()
    time.sleep(0.5)

    # 转身后退到放置位置
    move.rotate_to_left(0.55,2.5)    #
    time.sleep(0.5)
    move.moveback(0.05, 1)
    move.moveback(0.1, 1)
    move.moveback(0.2, 1)
    move.moveback(0.1, 1)
    move.moveback(0.05, 1)

    # 根据物体类型放置
    x, y, width, height, label = detect_result
    if label == "clock":##
        basic.move_to_my_coords(grabParams.coords_place_clock,60,3)
        basic.grap(False)
    else:
        basic.move_to_my_coords(grabParams.coords_place_apple,60,3)
        basic.grap(False)

    # 返回准备位置 
    basic.move_to_my_angles(grabParams.angles_ready,60,0.5)
    move.moveforward(0.05, 1)
    move.moveforward(0.1, 1)
    basic.move_to_my_coords(grabParams.coords_ready,80,0)
    move.moveforward(0.2, 1.5)
    move.moveforward(0.05, 1)


# # # 第二次
    time.sleep(0.5)
    #调整前后距离
    for _ in range(4):  #10
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()                      # 二次精调
    time.sleep(1)
    move.rotate_to_right(0.55, 2.7) # (0.55, 2.7)旋转90°      # 右转复位
    time.sleep(1)

    for _ in range(6):  
        distance = Sonor().get_sonor_data()
        Sonor().sonor_control_goal_2()
        time.sleep(0.5)

    # 重新打开摄像头
    follow.open_camera()

    # 视觉搜索物体
    detect_result = follow.moving_search()
   
    #抓取物体
    goal1_gab(detect_result)
    

   #调整前后距离
    move.moveforward(0.05,1.5)
    for _ in range(5):  #8
        distance = Sonor().get_sonor_data()
        print(distance)
        # Sonor().sonor_control_goal_3()
        Sonor().sonor_control_goal_5()
    time.sleep(0.5)

    # 转身后退到放置位置
    move.rotate_to_left(0.55,2.5)    #
    time.sleep(0.5)
    move.moveback(0.05, 1)
    move.moveback(0.1, 1)
    move.moveback(0.2, 1)
    move.moveback(0.1, 1)
    move.moveback(0.05, 1)

    # 根据物体类型放置
    x, y, width, height, label = detect_result
    if label == "clock":##
        basic.move_to_my_coords(grabParams.coords_place_clock,60,3)
        basic.grap(False)
    else:
        basic.move_to_my_coords(grabParams.coords_place_apple,60,3)
        basic.grap(False)

    # 返回准备位置 
    basic.move_to_my_angles(grabParams.angles_ready,60,0.5)
    move.moveforward(0.05, 1)
    move.moveforward(0.1, 1)
    basic.move_to_my_coords(grabParams.coords_ready,80,0)
    move.moveforward(0.2, 1.5)
    move.moveforward(0.05, 1)

    # # reach_goal1()
    # # move.moveback(0.05,2)
    # # move.rotate_to_right(0.55, 2.8) # (0.55, 2.7)旋转90°   ,,,比90多一点      
    # time.sleep(0.5)
    # for _ in range(6):  
    #     distance = Sonor().get_sonor_data()
    #     print(distance)
    #     Sonor().sonor_control_goal_2() 
    # time.sleep(0.5)
    # follow.open_camera()
    # detect_result = follow.moving_search()
    # goal1_gab(detect_result)
    # # move.rotate_to_right(0.5, 1)
    # # move.moveforward(0.15, 1.5)
    # # move.rotate_to_right(0.6, 2)
    # reach_goal2()
    # x, y, width, height, label = detect_result
    # if label == "clock":
    #     basic.move_to_my_coords(grabParams.coords_place_clock,20,4)
    #     basic.grap(False)
    # else:
    #     basic.move_to_my_coords(grabParams.coords_place_apple,20,4)
    #     basic.grap(False)
    # basic.move_to_my_coords(grabParams.coords_ready,20,4)
    # # move.moveback(0.3, 1)
    # # move.rotate_to_left(1, 3.5)
    # move.moveback(0.15, 2)
    # time.sleep(0.5)
    # move.rotate_to_left(0.55, 2.85)#3.1

 # # # 第三次
    time.sleep(0.5)
    #调整前后距离
    for _ in range(4):  #10
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()                      # 二次精调
    time.sleep(1)
    move.rotate_to_right(0.55, 2.7) # (0.55, 2.7)旋转90°      # 右转复位
    time.sleep(1)

    for _ in range(6):  
        distance = Sonor().get_sonor_data()
        Sonor().sonor_control_goal_2()
        time.sleep(0.5)

    # 打开摄像头并搜索物体
    follow.open_camera()

    # 视觉搜索物体
    detect_result = follow.moving_search()
   
    #抓取物体
    goal1_gab(detect_result)
    

   #调整前后距离
    move.moveforward(0.05,1.5)
    for _ in range(5):  #8
        distance = Sonor().get_sonor_data()
        print(distance)
        # Sonor().sonor_control_goal_3()
        Sonor().sonor_control_goal_5()
    time.sleep(0.5)

    # 转身后退到放置位置
    move.rotate_to_left(0.55,2.5)    #
    time.sleep(0.5)
    move.moveback(0.05, 1)
    move.moveback(0.1, 1)
    move.moveback(0.2, 1)
    move.moveback(0.1, 1)
    move.moveback(0.05, 1)

    # 根据物体类型放置
    x, y, width, height, label = detect_result
    if label == "clock":##
        basic.move_to_my_coords(grabParams.coords_place_clock,60,3)
        basic.grap(False)
    else:
        basic.move_to_my_coords(grabParams.coords_place_apple,60,3)
        basic.grap(False)

    # 返回准备位置 
    basic.move_to_my_angles(grabParams.angles_ready,60,0.5)
    move.moveforward(0.05, 1)
    move.moveforward(0.1, 1)
    basic.move_to_my_coords(grabParams.coords_ready,80,0)
    move.moveforward(0.2, 1.5)
    move.moveforward(0.05, 1)

#     reach_goal1()
#     time.sleep(0.5)
#     move.moveback(0.05, 1.5)
#     # move.rotate_to_right(0.55, 2.8) # (0.55, 2.7)旋转90°   ,,,比90多一点      
#     time.sleep(0.5)
#     follow.open_camera()
#     detect_result = follow.moving_search()
#     # if detect_result is  not None:
#     goal1_gab(detect_result)
#     # move.moveback(0.1, 1.5)
#     # move.rotate_to_right(0.5, 1)
#     # move.moveforward(0.15, 1.5)
#     # move.rotate_to_right(0.6, 2)
#     reach_goal2()
# # if detect_result is  not None:
#     x, y, width, height, label = detect_result
#     if label == "clock":
#         basic.move_to_my_coords(grabParams.coords_place_clock,20,4)
#         basic.grap(False)
#     else:
#         basic.move_to_my_coords(grabParams.coords_place_apple,20,4)
#         basic.grap(False)
#     basic.move_to_my_coords(grabParams.coords_ready,20,4)
#     move.moveback(0.15, 2)
#     time.sleep(0.5)
#     move.rotate_to_left(0.55, 2.82)#3.1

# # # 第四次
    time.sleep(0.5)
    #调整前后距离
    for _ in range(4):  #10
        distance = Sonor().get_sonor_data()
        print(distance)
        Sonor().sonor_control_goal_1()                      # 二次精调
    time.sleep(1)
    move.rotate_to_right(0.55, 2.7) # (0.55, 2.7)旋转90°      # 右转复位
    time.sleep(1)

    for _ in range(6):  
        distance = Sonor().get_sonor_data()
        Sonor().sonor_control_goal_2()
        time.sleep(0.5)

    # 重新打开摄像头
    follow.open_camera()

    # 视觉搜索物体
    detect_result = follow.moving_search()
   
    #抓取物体
    goal1_gab(detect_result)
    

   #调整前后距离
    move.moveforward(0.05,1.5)
    for _ in range(5):  #8
        distance = Sonor().get_sonor_data()
        print(distance)
        # Sonor().sonor_control_goal_3()
        Sonor().sonor_control_goal_5()
    time.sleep(0.5)

    # 转身后退到放置位置
    move.rotate_to_left(0.55,2.5)    #
    time.sleep(0.5)
    move.moveback(0.05, 1)
    move.moveback(0.1, 1)
    move.moveback(0.2, 1)
    move.moveback(0.1, 1)
    move.moveback(0.05, 1)

    # 根据物体类型放置
    x, y, width, height, label = detect_result
    if label == "clock":##
        basic.move_to_my_coords(grabParams.coords_place_clock,60,3)
        basic.grap(False)
    else:
        basic.move_to_my_coords(grabParams.coords_place_apple,60,3)
        basic.grap(False)

    # 返回准备位置      
    basic.move_to_my_coords(grabParams.coords_ready,30,0)

    # 调整姿态
    move.moveforward(0.15, 2)
    # time.sleep(0.5)
    move.rotate_to_right(1, 4.3)

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



    # reach_goal4()
    # for _ in range(10):  
    #     distance = Sonor().get_sonor_data()
    #     print(distance)
    #     Sonor().sonor_control_goal_4()
    # time.sleep(0.5)
    # move.rotate_to_left(0.55, 2.9)
    # time.sleep(0.5)
    # move.moveforward(0.1, 1.5)
    # for _ in range(20):  
    #     distance = Sonor().get_sonor_data()
    #     print(distance)
    #     Sonor().sonor_control_goal_4()
    # time.sleep(0.5)
    # time.sleep(1)
    # move.moveforward(0.05, 2)
