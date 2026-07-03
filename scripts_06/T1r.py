#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
import time



mc = MyCobot('/dev/arm',115200)
#将LED变色
mc.set_color(200,200,200)
#到达上层初始位置
mc.send_coords([57.8, 92.7, 386.4, -100.5, -41.82, 12.35],50,0)
time.sleep(0.5)
#到达上层抓取位置
mc.send_coords([61.6, 141.3, 363.7, -94.81, -41.59, 5.4],50,0)
time.sleep(0.4)
#夹爪闭合
mc.set_gripper_state(1, 50)
time.sleep(0.5)
#返回上层初始位置
mc.send_coords([57.8, 92.7, 386.4, -100.5, -41.82, 12.35],50,0)
time.sleep(0.5)
#到达下层初始位置
mc.send_coords([60.6, 68.4, 287.5, -104.61, -40.41, 12.33],50,0)
#mc.send_coords([(-67),(-58.8),276,(-93.07),(-42),178.36],20,0)
time.sleep(1)
#到达下层放置位置
mc.send_coords([62.4, 139.5, 264.9, -104.04, -41.58, 10.49],40,0)
time.sleep(0.4)
#夹爪张开
mc.set_gripper_state(0, 50)
time.sleep(0.5)
#返回下层初始位置
mc.send_coords([60.6, 68.4, 287.5, -104.61, -40.41, 12.33],50,0)
time.sleep(0.6)
#返回上层初始位置
mc.send_coords([57.8, 92.7, 386.4, -100.5, -41.82, 12.35],50,0)
#设置LED为绿色
mc.set_color(0,255,0)