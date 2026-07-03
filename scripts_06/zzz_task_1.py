#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
import time



mc = MyCobot('/dev/arm',115200)
#将LED变色
mc.set_color(200,200,200)
#到达上层初始位置
mc.send_coords([-58.5, -87.9, 389.4, -97.7, -42.14, -170.13],20,0)
time.sleep(1)
#到达上层抓取位置
mc.send_coords([-59.4, -144.5, 363.4, -93.62, -41.26, -174.88],20,0)
time.sleep(1.5)
#夹爪闭合
mc.set_gripper_state(1, 20)
time.sleep(1)
#返回上层初始位置
mc.send_coords([-58.5, -87.9, 389.4, -97.7, -42.14, -170.13],20,0)
time.sleep(1.5)
#到达下层初始位置
mc.send_coords([-61.0, -64.7, 291.5, -101.32, -40.99, -170.22],20,0)
#mc.send_coords([(-67),(-58.8),276,(-93.07),(-42),178.36],20,0)
time.sleep(2)
#到达下层放置位置
mc.send_coords([-62.4, -139.3, 268.0, -101.54, -41.56, -171.3],20,0)
time.sleep(1.5)
#夹爪张开
mc.set_gripper_state(0, 20)
time.sleep(1)
#返回下层初始位置
mc.send_coords([-61.0, -64.7, 291.5, -101.32, -40.99, -170.22],20,0)
time.sleep(1.5)
#返回上层初始位置
mc.send_coords([-58.5, -87.9, 389.4, -97.7, -42.14, -170.13],20,0)
#设置LED为绿色
mc.set_color(0,255,0)