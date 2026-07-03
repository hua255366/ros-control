#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
# import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse

mc = MyCobot(grabParams.usb_dev,grabParams.baudrate)
mc.set_color(0,255,255)
mc.send_coords(grabParams.coords_ready,40,0)
basic.grap(False)
mc.set_color(0,255,0)