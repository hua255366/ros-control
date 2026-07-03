#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time

#机器人
mc = MyCobot("/dev/arm", 115200)
Speed = 50
#上层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
coords_top_ready = [-64.2, -52.0, 408.0, 95.87, 39.27, 3.92]
# [71.5, -138.1, 355.2, 89.26, 47.1, 5.52]
coords_top_grap = [-70.7, -158.0, 371.9, 107.38, 38.5, 15.43]
# [71.5, -200.1, 325.2, 89.26, 47.1, 5.52]



coords_top_grap_ok = [-66.6, -74.3, 401.9, 101.86, 35.49, 6.4]
# [61.5, 60.8, 330.8, 86.53, 45, -178.72]

#下层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
coords_bottom_ready = [-60.5, -98.9, 266.3, 92.28, 39.76, 2.16]
# [45.0, -138.3, 250.2, 93.79, 45.66, 8.09]
coords_bottom_grap = [-59.6, -157.4, 258.6, 93.13, 41.1, 0.21]
# [45.0, -210.3, 240.2, 93.79, 45.66, 8.09]
coords_bottom_grap_ok = [61.5, 60.8, 260.8, 86.53, 45, -178.72]

#夹爪开关控制接口
def grap(flag):
    if flag:
        # close
        # self.mc.set_gripper_state(1, 0)
        time.sleep(0.1)
        mc.set_gripper_value(40,30)
        time.sleep(1)
    else:
        # open
        time.sleep(0.1)
        mc.set_gripper_value(255,30)
        time.sleep(1)
def put_down(ready,grab,speed):
    mc.send_coords(ready,speed, 0)
    time.sleep(1)
    print("put_ready")
    mc.send_coords(grab,speed, 1)
    time.sleep(2)
    print("put_grab")
    grap(False)
    mc.send_coords(ready,speed, 1)
    time.sleep(1)
    mc.send_coords(coords_top_ready,speed, 0)

def grab_up(ready,grab,speed):
    mc.send_coords(ready,speed, 0)
    print("grab_ready")
    time.sleep(1)
    mc.send_coords(grab,speed, 1)
    time.sleep(2)
    print("grab_grab")
    grap(True)
    #time.sleep(1)
    mc.send_coords(ready,speed, 1)

if __name__ == "__main__":

    mc.power_on()
    #angles = [0, 0, 0, 0, 0, 0]
    #mc.send_angles(angles,80)
    #time.sleep(2)
    #grap(False)
    mc.set_gripper_value(255,30)
    grab_up(coords_top_ready,coords_top_grap,Speed)
    time.sleep(2)
    put_down(coords_bottom_ready,coords_bottom_grap,Speed)



# mc.send_coords(coords_top_ready,Speed, 0)

#[-64.2, -52.0, 408.0, 95.87, 39.27, 3.92]
#[-70.7, -158.0, 371.9, 107.38, 38.5, 15.43]

#[-60.5, -98.9, 266.3, 92.28, 39.76, 2.16]
#[-62.8, -47.0, 292.4, 97.18, 37.24, 5.06]4num*2
#[-59.6, -157.4, 258.6, 93.13, 41.1, 0.21]