from pymycobot.mycobot import MyCobot


mc = MyCobot('/dev/ttyACM0',115200)
mc.send_angles([-90, 0, 0, 0, 0, -45],30)