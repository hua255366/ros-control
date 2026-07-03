from pymycobot.mycobot import MyCobot
from pymycobot.genre import Coord
import time
mc = MyCobot("/dev/arm", 115200)
coords = mc.get_coords()
print(coords)
print(mc.get_coords())