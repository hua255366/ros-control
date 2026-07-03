from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
import basic
from GrabParams import grabParams

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

mc.set_color(0,0,255)#blue, arm is busy   

mc.set_gripper_value(255,30)
time.sleep(3)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-152, -66, -6, -6, -3, 58]
mc.send_angles(angles,30)
time.sleep(5)
'''
angles = [-152, -66, 6, -13, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(4)

angles = [-140, -66, -6, -6, -3, 58]
mc.send_angles(angles,30)
time.sleep(5)

angles = [-140, -66, 6, -13, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)


angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(4)

angles = [158, -66, -6, -6, -3, 58]
mc.send_angles(angles,30)
time.sleep(5)

angles = [158, -66, 6, -13, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(4)

angles = [145, -66, -6, -6, -3, 58]
mc.send_angles(angles,30)
time.sleep(5)

angles = [145, -66, 6, -13, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)


angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [132, -67, 0, -9, -4, 58]
mc.send_angles(angles,30)
time.sleep(5)

angles = [132, -60, 0, -15, -4, 58]
mc.send_angles(angles,30)
time.sleep(2)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [120, -67, 0, -9, -4, 58]
mc.send_angles(angles,30)
time.sleep(5)

angles = [120, -60, 0, -15, -4, 58]
mc.send_angles(angles,30)
time.sleep(2)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [66, -67, 0, -9, -4, 58]
mc.send_angles(angles,30)
time.sleep(5)

angles = [66, -60, 0, -15, -4, 58]
mc.send_angles(angles,30)
time.sleep(2)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [55, -67, 0, -9, -4, 58]
mc.send_angles(angles,30)
time.sleep(5)

angles = [55, -60, 0, -15, -4, 58]
mc.send_angles(angles,30)
time.sleep(2)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)


angles = [-28, -34, -70, 25, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, 0, 0,0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, -29, 0, 40, 0, -45]
mc.send_angles(angles, 30)
time.sleep(3)

#angles = [-90, -37, -12, 57, -2, -45]
#mc.send_angles(angles,30)
#time.sleep(3)


angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

#1
angles = [-28, -34, -70, 25, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-28, -22, -70, 18, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

#2
angles = [-22, -69, 0, -6, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-22, -60, 0, -10, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

#3
angles = [63, -69, 4, -9, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [63, -60, 4, -13, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [11, -23, -39, -29, -3, 58]
mc.send_angles(angles,30)
time.sleep(3)

#4
angles = [53, -69, 4, -9, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

angles = [53, -60, 4, -13, -4, 58]
mc.send_angles(angles,30)
time.sleep(3)

#chufaqu_left
angles = [-90, 0, 0,0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, -35, -3, 49, -2, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_gripper_value(40,30)
time.sleep(3)

angles = [-90, 0, 0,0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, 50, -70,-30, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, 50, -150,110, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, -25, -80,110, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_gripper_value(255,30)
time.sleep(3)

angles = [-90, 25, -100,110, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, 0, 0,0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_color(0,255,0)#green, arm is free
'''
'''
#chufaqu_left
angles = [90, 0, 0, 0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)


angles = [90, -28, -4, 37, -4, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_gripper_value(40,30)
time.sleep(3)

angles = [90, 0, 0,0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [90, 70, -140, 80, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [90, -13, -101, 124, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_gripper_value(255,30)
time.sleep(3)

angles = [90, 70, -140, 80, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [90, 0, 0, 0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_color(0,255,0)#green, arm is free
'''