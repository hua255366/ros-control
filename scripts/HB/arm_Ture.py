from pymycobot.mycobot import MyCobot
import time

mc = MyCobot("/dev/arm", 115200)

mc.focus_servo(1)
mc.focus_servo(2)
mc.focus_servo(3)
mc.focus_servo(4)
mc.focus_servo(5)
mc.focus_servo(6)



print("angles",mc.get_angles())
print("coords",mc.get_coords())