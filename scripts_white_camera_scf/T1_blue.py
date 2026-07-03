#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
import time

up_catch=[-32.6, -193.3, 353.1, -89.53, -42.87, 176.69]
down_put=[-29.2, -199.9, 250.7, -90.68, -42.34, 177.29]

mc = MyCobot('/dev/arm',115200)
#将LED变色
mc.set_color(200,200,200)
#到达上层初始位置
mc.send_coords([-38.9, -164.6, 380.3, -97.3, -40.24, -178.15],45,0)#30
time.sleep(1)
#到达上层抓取位置
mc.send_coords(up_catch,45,0)#30
time.sleep(0.5)#1.5
#夹爪闭合
mc.set_gripper_state(1, 20)
time.sleep(1)#1
#返回上层初始位置
mc.send_coords([-51.1, -123.3, 399.4, -92.73, -42.99, 176.58],30,0)
time.sleep(1.5)
#到达下层初始位置
mc.send_coords([-61.0, -64.7, 291.5, -101.32, -40.99, -170.22],30,0)
#mc.send_coords([(-67),(-58.8),276,(-93.07),(-42),178.36],30,0)
time.sleep(2)
#到达下层放置位置
mc.send_coords(down_put,30,0)
time.sleep(1.5)
#夹爪张开
mc.set_gripper_state(0, 30)
time.sleep(1)
#返回下层初始位置
mc.send_coords([-61.0, -64.7, 291.5, -101.32, -40.99, -170.22],45,0)#30
time.sleep(1.5)
#返回上层初始位置
mc.send_coords([-38.9, -164.6, 380.3, -97.3, -40.24, -178.15],35,0)#30
#设置LED为绿色
mc.set_color(0,255,0)