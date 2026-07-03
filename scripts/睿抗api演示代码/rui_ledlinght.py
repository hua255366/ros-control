from pymycobot.mycobot import MyCobot
import time#以上需写在代码开头，意为导入项目包
# MyCobot类初始化需要两个参数：串口和波特率
mc = MyCobot("/dev/arm", 115200)
 i = 7
 #循环7次while i > 0:
 mc.set_color(0,0,255) #蓝灯亮
time.sleep(2) #等2秒
mc.set_color(255,0,0) #红灯亮
time.sleep(2) #等2秒
mc.set_color(0,255,0) #绿灯亮
time.sleep(2) #等2秒
i-= 1