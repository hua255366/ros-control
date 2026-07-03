from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord,Angle

import time

# 初始化一个MyCobot对象
mc = MyCobot("/dev/ttyUSB2", 115200)

# 开启吸泵
def pump_on():
    # 让2号位工作
    mc.set_basic_output(2, 0)
    # 让5号位工作
    mc.set_basic_output(5, 0)

# 停止吸泵
def pump_off():
    # 让2号位停止工作
    mc.set_basic_output(2, 1)
    # 让5号位停止工作
    mc.set_basic_output(5, 1)

pump_off()
time.sleep(8)
pump_on()
time.sleep(8)
pump_off()
time.sleep(8)
