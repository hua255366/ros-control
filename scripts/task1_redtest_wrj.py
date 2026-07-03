import cv2
import numpy as np
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
import basic
from GrabParams_2 import grabParams
import math
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('movement', anonymous=True)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(20)  # 20hz
move_cmd = Twist()

global motion_num

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

mc.set_gripper_value(40, 65)
time.sleep(2) 
mc.set_gripper_value(255, 30)

