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





#mc.send_coords([185.3, -57.5, 261.5, -175.27, -1.25, -144.42], 40, 1)
#time.sleep(2)

#print(mc.get_encoders())


angles =[3.16,-24.52,-20.03,-47.72,-5,56.95]

mc.send_angles(angles, 40)  






