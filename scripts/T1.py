from pymycobot.mycobot import MyCobot
import time


mc = MyCobot('/dev/arm',115200)
mc.send_angles([93.42, -0.96, -70.66, 83.58, -5.09, -42.18],60)
time.sleep(0.1)
mc.send_angles([93.77, -32.69, -32.51, 75.05, -3.42, -40.95],60)
time.sleep(0.3)
mc = MyCobot('/dev/arm',115200)
mc.set_gripper_state(1, 70)
time.sleep(0.5)
mc.send_angles([93.42, -0.96, -70.66, 83.58, -5.09, -42.18],60)
time.sleep(0.3)
mc.send_angles([93.77, 13.27, -122.43, 116.01, -2.37, -45.26],60)
time.sleep(0.8)
mc.send_angles([93.25, -38.93, -80.15, 123.57, -4.65, -41.83],60)
time.sleep(0.1)
mc = MyCobot('/dev/arm',115200)
mc.set_gripper_state(0, 70)
time.sleep(0.8)
mc.send_angles([93.77, 13.27, -122.43, 116.01, -2.37, -45.26],70)
time.sleep(0.8)
mc.send_angles([93.42, -0.96, -70.66, 83.58, -5.09, -42.18],70)