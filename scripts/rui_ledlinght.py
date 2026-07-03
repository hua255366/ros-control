from pymycobot.mycobot import MyCobot
import  time
mc = MyCobot("/dev/arm", 115200)
i = 7
while i > 0:
 	mc.set_color(255,0,255) 
	time.sleep(0) 
	mc.set_color(0,255,255)
	time.sleep(0)
	mc.set_color(255,255,0) 
	time.sleep(0)
	mc.set_color(255,255,255)  
	time.sleep(0) 
	mc.set_color(0,0,0) 
	time.sleep(0) 
	i-= 1