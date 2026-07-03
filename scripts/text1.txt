from pymycobot.mycobot import MyCobot
import time


mc = MyCobot('/dev/arm',115200)
# mc.send_angles([(-92.63),19.42,(-65.74),53.34,(-0.7),(-45)],70)
# time.sleep(1)
mc.set_gripper_state(0, 25)
time.sleep(1)
mc.send_angles([(-92.46),(-17.66),(-39.9),59.85,(-1.84),(-46.4)],70)
time.sleep(1)
mc.set_gripper_state(1, 25)
time.sleep(1)
mc.send_angles([(-92.63),19.42,(-65.74),53.34,(-0.7),(-45)],70)
time.sleep(1)
mc.send_angles([(-102.39),37.96,(-142.2),110.74,4.74,(-47.46)],70)
time.sleep(1)
mc.send_angles([(-94.13),(-11.6),(-103.53),116.98,(-6.67),(-47.63)],70)
time.sleep(1)
mc.set_gripper_state(0, 40)
time.sleep(1)
mc.send_angles([(-102.39),37.96,(-142.2),110.74,4.74,(-47.46)],70)
time.sleep(1)
mc.send_angles([(-92.63),19.42,(-65.74),53.34,(-0.7),(-45)],70)