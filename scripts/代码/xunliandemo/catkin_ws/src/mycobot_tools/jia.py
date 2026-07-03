from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
mc = MyCobot("/dev/ttyUSB0", 1000000)
mc.send_angles([0, 0, 0, 0, 0, 0],30)
time.sleep(6)
mc.send_angles([41.83, -8.26, -124.01, 37.79, -0.7, -75.49],30)
time.sleep(6)
mc.set_gripper_state(1, 0)
time.sleep(2)
mc.set_gripper_state(0, 0)
time.sleep(2)
mc.send_angles([-41.83, -8.26, -124.01, 37.79, -0.7, -75.49],30)
time.sleep(6)
mc.set_gripper_state(1, 0)
time.sleep(2)
mc.set_gripper_state(0, 0)
time.sleep(2)
#while True:
#    mc.set_gripper_state(1, 0)
#    print("Close")
#   time.sleep(2)
#   mc.set_gripper_state(0, 0)
#   print("Open")
#   time.sleep(2)



















































































































































































































