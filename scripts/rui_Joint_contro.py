from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
num=3
mc = MyCobot("/dev/arm", 115200)
mc.send_angles([0, 0, 0, 0, 0, 0], 50)
time.sleep(2.5)
mc.send_angle(Angle.J1.value, 90, 50)
time.sleep(2)
while num > 0:
	mc.send_angle(Angle.J2.value, 50, 50)
	time.sleep(1.5)
	mc.send_angle(Angle.J2.value,-50, 50)
	time.sleep(1.5)
 	num-= 1
mc.send_angles([88.68,-138.51, 155.65,-128.05,-9.93,-15.29], 50)
time.sleep(2.5)