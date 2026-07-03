from pymycobot.mycobot import MyCobot


mc = MyCobot('/dev/ttyACM0',115200)
mc.release_servo(1)
mc.release_servo(2)
mc.release_servo(3)
mc.release_servo(4)