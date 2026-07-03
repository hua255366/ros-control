# -*- coding: utf-8 -*-
from pymycobot.mycobot import MyCobot
import time

# 初始化机械臂
mc = MyCobot("/dev/arm", 115200)

target_angle=[-84.19, 0.0, -106.78, 99.93, -7.82, -46.49]

# 发送角度指令，运动到目标位置
mc.send_angles(target_angle, 80)
print("正在运动到目标位置...")

# 等待机械臂完成运动并保持2秒
time.sleep(2)
angle_T=mc.get_angles()
angle_T[1]= angle_T[1]+45
angle_T[2]= angle_T[2]+30
angle_T[3]= angle_T[3]-40
mc.send_angles(angle_T,60) 
time.sleep(2)
#angle_T[3]= angle_T[3]-70
#mc.send_angles(angle_T,60) 
#time.sleep(2)
target_angle=[-76.37, -18.28, 3.07, 24.96, -16.34, -49.65]
mc.send_angles(target_angle, 60)
time.sleep(2)
print("已到达目标位置并保持2秒")

# 在当前位置软化所有关节
# mc.release_servo(1)
# mc.release_servo(2)
# mc.release_servo(3)
# mc.release_servo(4)
# mc.release_servo(5)
# mc.release_servo(6)

print("已在目标位置软化所有关节")
    