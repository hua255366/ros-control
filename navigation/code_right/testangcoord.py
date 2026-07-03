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
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
from pymycobot.genre import Angle
from GrabParams import grabParams
import time 

coords_ready = [60.9, 77.0, 265.1, 89.2, 48.38, 179.75]
# coords_ready = [-62.1, -79.3, 264.1, 91.96, 47.9, 0.48]
# coords_grap = [-49.9, -170, 350, 90.51, 47.11, -7.27]
# #机械臂上电[-39.9, -174.9, 260.1, 100.4, 51.93, 0.53]
mc = MyCobot("/dev/arm",115200)
mc.power_on()
time.sleep(1)


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
    # basic.move_to_my_angles(grabParams.angles_ready,60,3)
    # time.sleep(1)
    basic.move_to_my_coords(grabParams.coords_ready,80,3)
    time.sleep(2)
    print("coords:", mc.get_coords())
    print("angles:", mc.get_angles())