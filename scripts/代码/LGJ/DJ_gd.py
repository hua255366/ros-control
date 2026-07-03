from pymycobot.mycobot import MyCobot


mc = MyCobot('/dev/ttyACM0',115200)
mc.focus_servo(1)
mc.focus_servo(2)
mc.focus_servo(3)
mc.focus_servo(4)