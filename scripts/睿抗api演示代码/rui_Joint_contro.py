from pymycobot.mycobot import MyCobot
 from pymycobot.genre import Angle
 import time
 # MyCobot类初始化需要两个参数：第一个是串口字符串，第二个是波特率
mc = MyCobot("/dev/arm", 115200)
 #通过传递角度参数，让机械臂每个关节移动到对应[0, 0, 0, 0, 0, 0]的位置
mc.send_angles([0, 0, 0, 0, 0, 0], 50)
 #设置等待时间，确保机械臂已经到达指定位置
time.sleep(2.5)
 #让关节1移动到90这个位置
mc.send_angle(Angle.J1.value, 90, 50)#设置等待时间，确保机械臂已经到达指定位置
time.sleep(2)
 #以下代码可以让机械臂左右摇摆#设置循环次数
while num > 0:
 #让关节2移动到50这个位置
mc.send_angle(Angle.J2.value, 50, 50)
 #设置等待时间，确保机械臂已经到达指定位置
time.sleep(1.5)
 #让关节2移动到-50这个位置
mc.send_angle(Angle.J2.value,-50, 50)
 #设置等待时间，确保机械臂已经到达指定位置
time.sleep(1.5)
 num-= 1
 #让机械臂缩起来。你可以手动摆动机械臂，然后使用get_angles()函数获得坐标数列，#通过该函数让
机械臂到达你所想的位置。
mc.send_angles([88.68,-138.51, 155.65,-128.05,-9.93,-15.29], 50)
 #设置等待时间，确保机械臂已经到达指定位置
time.sleep(2.5)