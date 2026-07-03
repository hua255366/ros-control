from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
mc = MyCobot("/dev/arm", 115200)
i = 7
while i > 0:
	mc.send_angles([0,0,0,0,0,0],50)
	mc.set_color(255,200,180)
	time.sleep(5)
	mc.send_angles([90,45,-90,90,-90,90],50)
	mc.set_color(255,0,180)
	time.sleep(5)
	mc.send_angles([0,0,0,0,0,0],50)
	mc.set_color(0,200,180)
	time.sleep(5)
	mc.send_angles([-90,-45,90,-90,90,-90],50)
	mc.set_color(255,200,0)
	time.sleep(5)
	mc.set_color(255,255,255)
	time.sleep(1)
	i-=1