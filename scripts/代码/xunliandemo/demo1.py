#encoding: UTF-8
#!/usr/bin/env python2
import time
from GrabParams import grabParams
import math
import rospy
from geometry_msgs.msg import Twist


class movement(object):

	def __init__(self):
		super(movement, self).__init__()

		rospy.init_node('movement', anonymous=True)
		self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		self.rate = rospy.Rate(20) # 20hz

	#小车后退
	def moveback(self, time_seconds,speed):
	    print("backward...")
	    count = 20*time_seconds
	    move_cmd = Twist()
	    while count > 0:
	        move_cmd.linear.x = speed #m/s
	        self.pub.publish(move_cmd)
	        self.rate.sleep()
	        count -= 1

	def moveforward(self, time_seconds,speed):		
	    print("forward...")
	    count = 20*time_seconds
	    move_cmd = Twist()
	    while count > 0:
	        move_cmd.linear.x = speed #m/s
	        self.pub.publish(move_cmd)
	        self.rate.sleep()
	        count -= 1

	#小车右转
	def rotate_to_right(self, time_seconds):
	    print("rotate_to_right...")
	    count = 20*time_seconds
	    move_cmd = Twist()
	    while count > 0:
	        move_cmd.angular.z = -1 #rad/s
	        self.pub.publish(move_cmd)
	        self.rate.sleep()
	        count -= 1

	#小车左转
	def rotate_to_left(self, time_seconds):
	    print("rotate_to_left...")
	    count = 20*time_seconds
	    move_cmd = Twist()
	    while count > 0:
	        move_cmd.angular.z = 1 #rad/s
	        self.pub.publish(move_cmd)
	        self.rate.sleep()            
	        count -= 1
m = movement()
'''

#1

#m.rotate_to_right(1.5)
m.rotate_to_left(1.5)
time.sleep(1)
m.moveforward(0.4,0.4)
time.sleep(1)
m.rotate_to_left(1.42)
time.sleep(1)
m.moveback(0.4,-0.22)
'''
#2
m.moveforward(0.4,0.1)
time.sleep(1)
m.rotate_to_left(1.4)
time.sleep(1)
m.moveback(0.7,-0.22)