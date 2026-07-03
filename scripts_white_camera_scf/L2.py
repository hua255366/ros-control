#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
import threading
from multiprocessing import Process
import os, time
if __name__ == "__main__":

		os.system("python  /home/robuster/beetle_ai/scripts/dnn_grab_2.py")
		os.system("python  /home/robuster/beetle_ai/scripts/place_4.py")
		

t = threading.Thread(target=dnn_grab_3,name='dnn_grab_4')
t.setDaemon(True)
t.start()