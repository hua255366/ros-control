from pymycobot.mycobot import MyCobot
import  time
mc = MyCobot("/dev/arm", 115200)
mc.power_on()
print(mc.is_power_on())
mc.resume()