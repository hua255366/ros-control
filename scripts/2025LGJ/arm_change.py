from pymycobot.mycobot import MyCobot

from pymycobot.genre import Angle
import time

mc = MyCobot("/dev/arm", 115200)

# ZB = [-76.37, -18.28, 3.07, 24.96, -16.34, -49.65]
# ZQ = [-80.41, -40.34, 13.97, 20.91, -10.45, -46.93]
# FZ=[-80.41, -106.96, 100.98, 9.49, -6.06, -46.05]
# SH=[-80.94, -122.43, 138.33, 8.7, -4.39, -45.87]

#[100.19, -18.19, 0.35, 24.25, -16.69, -49.13]
#[96.76, -40.86, 12.12, 20.12, -10.81, -47.28]
angles = [-80.41, -106.96, 100.98, 9.49, -6.06, -46.05]
mc.send_angles(angles, 70)
time.sleep(1.8)
# angles = [-80.41, -40.34, 13.97, 20.91, -10.45, -46.93]
# mc.send_angles(angles, 70)
# time.sleep(1.8)

# angle_T=mc.get_angles()
# angle_T[1]=angle_T[1]+40
# mc.send_angles(angle_T,80) 
# time.sleep(0.3)

# angles = [0, 0, 0, 0, 0, 0]
# mc.send_angles(angles, 80)
# time.sleep(0.5)

mc.release_servo(1)
# mc.release_servo(2)
# mc.release_servo(3)
# mc.release_servo(4)
# mc.release_servo(5)
# mc.release_servo(6)

print("OK")
