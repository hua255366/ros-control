#encoding: UTF-8
#!/usr/bin/env python2
import cv2 as cv
import os
import time
from pymycobot.mycobot import MyCobot
import math
from GrabParams import grabParams
import basic
import dnn_grab_2

class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()
       
    

    # Grasping motion
    def run(self):
        coords = grabParams.coords_ready
        #coords_target = [dnn_grab_2.coords_target[0]-50, coords[1]+int(y), height_bias+60, coords[3], coords[4], coords[5]]
        #basic.move_to_target_coords(coords_target,10)
        #coords_target = [dnn_grab_2.coords_target[0]-50, coords[1]+int(y), height_bias, coords[3], coords[4], coords[5]]
        #eg  :coords_target = [coords[0]+int(x)-50, coords[1]+int(y), height_bias, coords[3], coords[4], coords[5]]
        #basic.move_to_target_coords(coords_target,10)
        self.mc.send_coords([coords[0]-37,coords[1],grabParams.height_bias+30,coords[3],coords[4],coords[5]], 30, 0)
        time.sleep(2)

        #self.mc.send_coords([coords[0]+80,coords[1],grabParams.height_bias,coords[3],coords[4],coords[5]], 20, 0)
        #time.sleep(4)

        basic.grap(False)
        basic.move_to_target_coords(coords,30)

        #angles = [0, 0, 0, 0, 0, 0]
        #self.mc.send_angles(angles,30)
        #time.sleep(3)



if __name__ == "__main__":
    detect = Detect_marker()
    detect.mc.set_color(0,0,255)#blue, arm is busy
    detect.run()
    detect.mc.set_color(0,255,0)#green, arm is free
