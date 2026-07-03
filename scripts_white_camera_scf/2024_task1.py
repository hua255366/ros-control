#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time

#机器人
mc = MyCobot("/dev/arm", 115200)
Speed = 30
#上层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
#coords_top_ready = [71.5, -138.1, 355.2, 89.26, 47.1, 5.52]
#coords_top_grap = [71.5, -200.1, 325.2, 89.26, 47.1, 5.52]
#zxy
coords_top_ready =[66.2, 80.1, 408.5, -87.8, -43.84, -4.77]
#1coords_top_grap = [77.2, 136.3, 376.0, -77.43, -44.24, -14.37]
#jin coords_top_grap = [79.5, 163.1, 368.7, -107.33, -44.76, 7.31]
coords_top_grap = [74.3, 183.7, 353.8, -94.89, -46.99, 0.33]
#coords_top_grap_ok = [61.5, 60.8, 330.8, 86.53, 45, -178.72]
#1coords_top_grap_ok = [67.1, 69.6, 406.3, -88.71, -41.46, -2.16]
coords_top_grap_ok =[70.9, 187.0, 353.9, -94.34, -43.31, -0.17]
#下层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
#coords_bottom_ready =[45.0, -138.3, 250.2, 93.79, 45.66, 8.09]
#coords_bottom_grap = [45.0, -210.3, 240.2, 93.79, 45.66, 8.09]
#coords_bottom_grap_ok = [61.5, 60.8, 260.8, 86.53, 45, -178.72]
#1coords_bottom_ready =[68.2, 80.0, 335.2, -91.26, -46.15, -3.04]
#2coords_bottom_ready =[58.6, -71.9, 275.6, -27.22, -26.62, -35.99]
coords_bottom_ready =[57.0, -52.1, 251.0, -58.7, -40.88, -19.8]
#1coords_bottom_grap = [51.0, 155.2, 297.3, -100.39, -44.09, 8.55]
coords_bottom_grap_ok = [68.0, 25.4, 331.5, -91.22, -49.91, -4.34]
coords_bottom_grap = [52.7, 172.5, 287.6, -103.05, -46.63, 8.96]
def grap(flag):
    if flag:
        # close
        # self.mc.set_gripper_state(1, 0)
        time.sleep(1)
        mc.set_gripper_value(40,30)
        time.sleep(2)
    else:
        # open
        time.sleep(0.1)
        mc.set_gripper_value(255,30)
        time.sleep(1)
def put_down(ready,grab,speed):
    mc.send_coords(ready,speed, 0)
    time.sleep(2)
    print("put_ready")
    mc.send_coords(grab,speed, 1)
    time.sleep(3)
    print("put_grab")
    grap(False)
    mc.send_coords(ready,speed, 1)
    time.sleep(1)
    mc.send_coords(coords_top_ready,speed, 0)

def grab_up(ready,grab,speed):
    mc.send_coords(ready,speed, 0)
    print("grab_ready")
    time.sleep(2)
    mc.send_coords(grab,speed, 1)
    time.sleep(3)
    print("grab_grab")
    grap(True)
    #time.sleep(1)
    mc.send_coords(ready,speed, 1)
    
def grab_re(ready,speed):
    mc.send_coords(ready,speed, 0)
    print("grab_ready")
    
if __name__ == "__main__":

    mc.power_on()
    #angles = [0, 0, 0, 0, 0, 0]
    #mc.send_angles(angles,80)
    #time.sleep(2)
    #grap(False)
    mc.set_gripper_value(255,30) 
    grab_re(coords_top_ready,Speed)
    time.sleep(1)
    grab_up(coords_top_ready,coords_top_grap,Speed)
    time.sleep(2)
    put_down(coords_bottom_ready,coords_bottom_grap,Speed)

   