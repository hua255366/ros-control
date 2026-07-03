#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
import time

#在此抓取程序中，小方块放置位置应位于摄像头的正前方，小方块在架子上的放置位置可位于前三分之二处
mc = MyCobot('/dev/arm',115200)
#设置开始程序时的LED颜色
mc.set_color(200,244,200)
#夹爪打开
mc.set_gripper_state(0, 15)
time.sleep(1)
#移动到上层抓取准备点
mc.send_coords([(-67.5),(-35),420.4,(-72.95),(-42.58),162.41],25,0)
time.sleep(3)
#移动到上层抓取位置
mc.send_coords([(-66.7),(-157.2),379.4,(-83.58),(-44.9),169.46],25,0)
time.sleep(3)
#夹爪抓取闭合
mc.set_gripper_state(1, 15)
time.sleep(3.5)
#返回上层抓取准备点
mc.send_coords([(-67.5),(-35),420.4,(-72.95),(-42.58),162.41],25,0)
time.sleep(2)
#移动到下层放置准备点
mc.send_coords([(-65.6),(-41.6),308.7,(-90.98),(-44.76),177.79],25,0)
time.sleep(4)
#移动到下层放置点位
mc.send_coords([(-54.5),(-161.5),298.4,(-88.66),(-44.29),175.2],25,0)
time.sleep(3)
#夹爪松开放置
mc.set_gripper_state(0, 15)
time.sleep(3.5)
#返回下层放置准备点
mc.send_coords([(-65.6),(-41.6),308.7,(-90.98),(-44.76),177.79],25,0)
time.sleep(2.5)
#回到上层抓取准备点
mc.send_coords([(-67.5),(-35),420.4,(-72.95),(-42.58),162.41],25,0)
#将LED设置为绿色
mc.set_color(0,255,0)