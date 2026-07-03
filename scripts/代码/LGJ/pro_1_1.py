from pymycobot.mycobot import MyCobot
import threading
from pymycobot.genre import Angle
from multiprocessing import Process
from GrabParams import grabParams
import os, time
import time
#import pro_2



if __name__ == "__main__":
	mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
	mc.power_on()
	mc.set_color(0,0,255)
	
	i=0

	while i<4:
		i+=1
		os.system(
        "python /home/robuster/LGJ/pro_1_end.py  --debug ''"
    )
	angles = [0, 0, 0, 0, 0, 0]
	mc.send_angles(angles, 30)
	time.sleep(2)
	coords= [185.3, -57.5, 261.5, -175.27, -1.25, -144.42]
	mc.send_coords(coords,15,0)
	mc.set_color(0,255,0)
		