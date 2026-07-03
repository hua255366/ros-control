from pymycobot.mycobot import MyCobot


mc = MyCobot('/dev/arm',115200)
mc.send_angles([(-92.63),19.42,(-65.47),53.34,(-0.7),(-45)],35)