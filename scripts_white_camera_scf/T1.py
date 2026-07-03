#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
import time



mc = MyCobot('/dev/arm',115200)
#将LED变色
mc.set_color(200,200,200)
#到达上层初始位置
mc.send_coords([67.6,96.5,375.6,(-99.76),(-43.07),4.24],65,0)#25
time.sleep(2)

mc.send_coords([71.1, 145.7, 351.6, -99.07, -39.98, 2.34],65,0)#65.1, 146.8, 354.8, -100.59, -44.37, 4.69
time.sleep(0.5)

mc.set_gripper_state(1, 50)#25
time.sleep(0.5)#1

mc.send_coords([67.6,96.5,375.6,(-99.76),(-43.07),4.24],65,0)#25
time.sleep(0.5)

mc.send_coords([63.3,48.8,259.4,(-95.61),(-45.16),4.16],65,0)#25
time.sleep(1)#2.2

mc.send_coords([57.8, 149.9, 251.8, -95.09, -40.55, 5.69],65,0)#66.8,139.1,257.6,(-96.9),(-45.71),0.37###25
time.sleep(1)

mc.set_gripper_state(0, 50)#25
time.sleep(0.5)#1

mc.send_coords([63.3,48.8,259.4,(-95.61),(-45.16),4.16],65,0)#25
time.sleep(0.5)#1.5

mc.send_coords([67.6,96.5,375.6,(-99.76),(-43.07),4.24],65,0)#25
#设置LED为绿色
mc.set_color(0,255,0)