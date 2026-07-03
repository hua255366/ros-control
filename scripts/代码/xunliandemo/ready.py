from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams


mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
mc.set_color(0,0,255)#blue, arm is busy   

#coords = [64.9, 47.1, 411.0, -92.78, -45.98, 0.24]
coords = [-63.3, -126.9, 357.1, 81.63, 42.54, -4.87]
mc.send_coords(coords,15,0)
time.sleep(6)

mc.set_color(0,255,0)#green, arm is free
