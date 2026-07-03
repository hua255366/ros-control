#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time

#机器人
mc = MyCobot("/dev/arm", 115200)
Speed = 40
#上层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
coords_top_ready = [-67.5, -35.0, 420.4, -72.95, -42.58, 162.41]

coords_top_grap =  [-66.7, -157.2, 379.4, -83.58, -44.9, 169.46]
coords_top_down = [24.4, -148.1, 328.6, -84.09, -45.1, 179.32]


coords_top_back =  [-67.5, -35.0, 420.4, -72.95, -42.58, 162.41]



#下层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
coords_bottom_ready =  [-65.6, -41.6, 308.7, -90.98, -44.76, 177.79]


coords_bottom_reach =  [-54.5, -161.5, 298.4, -88.66, -44.29, 175.2]
coords_bottom_back = [-65.6, -41.6, 308.7, -90.98, -44.76, 177.79]
coords_bottom_down = [-57.3, -72.6, 379.0, -127.14, -33.42, -154.02]

coords_bottom_before_grab = [-60.0, -96.7, 353.7, -115.37, -38.21, -162.8]

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

def put_down(ready,grab, back, down_head, before_grab, speed):

    mc.send_coords(ready,speed, 1)
    print("put_ready")
    time.sleep(3)
    #mc.send_coords(down_head, speed, 0)
    #time.sleep(5)
    #mc.send_coords(before_grab, speed, 0)
    #time.sleep(5)
    mc.send_coords(grab,speed, 1)
    time.sleep(2)
    print("put_grab")
    grap(False)
    time.sleep(1)
    mc.send_coords(back,speed, 1)
    time.sleep(1)
    print("put_grab")
    #time.sleep(4)


    #mc.send_coords(back,speed, 0)

def grab_up(ready,grab,down, back,speed):
    mc.send_coords(ready,speed, 0)

    print("grab_ready")
    time.sleep(2)
    mc.send_coords(grab,10, 1)
    time.sleep(2)
    grap(True)
    time.sleep(1)
    print("grab_grab")
    # # mc.send_coords(down,speed, 1)

    # print("grab_down")
    # # time.sleep(1)
    # grap(True)
    # time.sleep(2)
    
    mc.send_coords(back,speed, 1)
    time.sleep(1)
    print("grad_back")

if __name__ == "__main__":

    mc.power_on()
    #angles = [0, 0, 0, 0, 0, 0]
    #mc.send_angles(angles,80)
    #time.sleep(2)
    #grap(False)
    mc.set_gripper_value(255,30)
    grab_up(coords_top_ready,coords_top_grap, coords_top_down, coords_top_back,Speed)
    time.sleep(1)
    put_down(coords_bottom_ready,coords_bottom_reach, coords_bottom_back, coords_bottom_down, coords_bottom_before_grab,Speed)

   
