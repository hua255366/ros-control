#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time

#机器人
mc = MyCobot("/dev/arm", 115200)
Speed = 50
#上层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
coords_top_ready =[-62.8, -65.4, 365.8, 91.2, 43.03, 1.69]
coords_top_grap = [-63.3, -126.9, 357.1, 81.63, 42.54, -4.87]
coords_top_grap_ok = [118.0, -87.8, 272.5, 93.22, 43.28, 0.05]

#下层货架抓取，机械臂的控制位置，可以通过注释其他代码进行调试
coords_bottom_ready =[-62.1, -75.8, 283.9, 93.31, 43.8, -3.43]
coords_bottom_grap =[-75.0, -148.5, 263.7, 87.42, 41.38, -7.59]
coords_bottom_grap_ok = [-62.8, -65.4, 365.8, 91.2, 43.03, 1.69]
KKK=[-90.35, 9.84, -120.76, 113.11, 0.52, 136.4]

#夹爪开关控制接口
def grap(flag):
    if flag:
        # close
        # self.mc.set_gripper_state(1, 0)
        time.sleep(0.1)
        mc.set_gripper_value(40,30)#是指令机械臂的夹爪以一定的速度或在一定的时间内达到一个特定的闭合位置或力度
        time.sleep(1)
    else:
        # open
        time.sleep(0.1)
        mc.set_gripper_value(255,30)
        time.sleep(1)
def put_down(ready,grab,speed):
    mc.send_coords(ready,speed, 0)#的含义是让机械臂以指定的速度移动到由 grab 坐标指定的位置，并在到达后执行由第三个参数 1/0 指定的特定行为
    time.sleep(1)
    print("put_ready")
    #mc.send_coords(KKK,speed, 1)
    time.sleep(2)
    print("KKK")

    mc.send_coords(grab,speed, 1)
    time.sleep(2)
    print("put_grab")
    grap(False)#调用确保了机械臂的夹爪在不需要抓取物体时是张开的,False张开,True闭合
    mc.send_coords(ready,speed, 1)
    time.sleep(3)
    mc.send_coords(coords_top_ready,speed, 0)

def grab_up(ready,grab,speed):
    mc.send_coords(ready,speed, 1)
    print("grab_ready")
    time.sleep(1)
    #mc.send_coords(grab,speed, 1)
    time.sleep(2)
    print("grab_grab")
    grap(True)
    time.sleep(1)
    mc.send_coords(ready,speed, 1)

if __name__ == "__main__":

    mc.power_on()
    grap(True)
    #angles = [0, 0, 0, 0, 0, 0]
    #mc.send_angles(angles,80)
    time.sleep(2)
    #grap(False)
    #mc.set_gripper_value(255,30)#第一个参数:夹爪完全闭合,0是打开,第二个参数夹爪状态改变的时间速度
    grab_up(coords_top_ready,coords_top_grap,Speed)
    put_down(coords_bottom_ready,coords_bottom_grap,Speed)

   