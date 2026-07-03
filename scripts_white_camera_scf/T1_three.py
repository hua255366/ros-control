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

mc.send_coords([70.5, 144.7, 350.3, -98.34, -40.59, 4.14],65,0)#65.1, 146.8, 354.8, -100.59, -44.37, 4.69^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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






#reach the upper position,second time###################################################
mc.send_coords([28.5, 97.5, 380.7, -109.11, -42.5, 35.97],65,0)#25[67.6,96.5,375.6,(-99.76),(-43.07),4.24]
time.sleep(2.5)

mc.send_coords([17.6, 139.1, 360.1, -99.93, -45.66, 29.32],65,0)#[-8.6, 140.4, 345.6, -91.12, -39.4, 5.1]
time.sleep(1)

#mc.send_coords([-8.6, 140.4, 345.6, -91.12, -39.4, 5.1],65,0)
#time.sleep(1)

mc.set_gripper_state(1, 50)#25
time.sleep(0.5)#1

mc.send_coords([43.2, 61.4, 339.3, -109.76, -41.57, 36.14],65,0)#25[67.6,96.5,375.6,(-99.76),(-43.07),4.24]
time.sleep(1)

#mc.send_coords([63.3,48.8,259.4,(-95.61),(-45.16),4.16],65,0)#25
#time.sleep(2.2)

mc.send_coords([10.9, 155.9, 281.3, -121.49, -41.13, 48.66],65,0)#[-36.9, 146.7, 258.9, -108.76, -36.46, 11.11]
time.sleep(1)

mc.set_gripper_state(0, 50)#25
time.sleep(0.5)#1

mc.send_coords([63.3,48.8,259.4,(-95.61),(-45.16),4.16],65,0)#25
time.sleep(0.5)#1.5






#reach the upper position,last time#######################################################
mc.send_coords([67.6,96.5,375.6,(-99.76),(-43.07),4.24],65,0)#25
time.sleep(1.5)

mc.send_coords([88.4, 107.5, 364.8, -100.76, -40.32, -18.88],65,0)#25
time.sleep(0.5)

mc.send_coords([99.5, 148.2, 342.1, -91.14, -38.69, -28.99],65,0)#25
time.sleep(0.75)

mc.send_coords([99.5, 148.2, 342.1, -91.14, -38.69, -28.99],65,0)#25
time.sleep(0.5)

mc.set_gripper_state(1, 50)#25
time.sleep(0.5)#1

mc.send_coords([85.0, 80.5, 313.2, -105.66, -39.86, -12.5],65,0)#25
time.sleep(0.5)

mc.send_coords([108.3, 155.9, 283.4, -120.66, -41.69, -6.08],65,0)#25
time.sleep(0.5)

mc.set_gripper_state(0, 50)#25
time.sleep(1)#1

mc.send_coords([67.6,96.5,375.6,(-99.76),(-43.07),4.24],65,0)#25
time.sleep(1.5)





