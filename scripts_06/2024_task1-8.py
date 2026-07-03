#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time

#机器人
mc = MyCobot("/dev/arm", 115200)
Speed = 40

#上层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
coords_top_ready = [-56.4, -131.1, 379.5, 93.86, 37.28, 4.45]
coords_top_grap = [-57.2, -162.6, 356.2, 90.47, 42.12, -0.12]
coords_top_grap_ok = [61.5, 60.8, 330.8, 86.53, 45, -178.72]

#下层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
coords_bottom_ready =[-57.3, -97.2, 292.8, 90.77, 37.63, 3.11]
coords_bottom_grap = [-52.9, -179.8, 272.2, 96.52, 41.12, 4.63]
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

   