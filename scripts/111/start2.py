from pymycobot.mycobot import MyCobot


mc = MyCobot('/dev/arm',115200)
mc.send_coords([(-64.1),(-233.5),200.6,175.95,(-0.11),135.28],40,0)