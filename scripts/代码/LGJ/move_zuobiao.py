from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
from GrabParams import grabParams
mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.power_on()
mc.set_color(0,0,255)#blue, arm is busy   

#coords = [64.9, 47.1, 411.0, -92.78, -45.98, 0.24]
#coords = [67.6, 145.1, 379.1, -89.51, -43.94, -1.83]
#coords =[-22.299999999999997, -120.4, 360, 92.25, 44.1, 2.69]
coords= [185.3, -57.5, 261.5, -175.27, -1.25, -144.42]
mc.send_coords(coords,15,0)
#mc.send_coords(coords_top_ready,Speed, 0)

mc.set_color(0,255,0)#green, arm is free
