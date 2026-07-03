from pymycobot.mycobot import MyCobot
import  time
mc = MyCobot("/dev/arm", 115200)
print(mc.get_speed())
time.sleep(1)
mc.set_speed(50)
print(mc.get_speed())