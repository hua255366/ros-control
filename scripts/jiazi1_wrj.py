from pymycobot.mycobot import MyCobot
import time
def gripper_test(mc):
	print("Start check IO part of api\n")
	flag = mc.is_gripper_moving()
	print("Is gripper moving: {}".format(flag))
	time.sleep(1)
	mc.set_gripper_value(255, 50)
	time.sleep(3)
	mc.set_gripper_value(200, 50)
	while True:
		time.sleep(3)
		mc.set_gripper_state(1, 100)
		time.sleep(3)
		mc.set_gripper_state(0, 100)
		time.sleep(3)
		mc.set_gripper_state(1, 100)
		time.sleep(3)
		print("")
		print(mc.get_gripper_value())
if __name__ == "__main__":
	mc = MyCobot("/dev/arm", 115200)
	mc.set_encoders([2048, 2048, 2048, 2048, 2048, 2048], 20)
	time.sleep(3)
	gripper_test(mc)