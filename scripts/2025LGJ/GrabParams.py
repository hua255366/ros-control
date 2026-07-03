#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	ratio = 0.35
	# increase x_bias to move front, or decrease x_bias to move back
	x_bias = 5

	# increase y_bias to move left, or decrease y_bias to move right
	y_bias = 30
	#               	 (+x)front
	#                 	  ^
	#				 	  :
	#				  	  :
	#                 	  :
	# (+y)< ..............o..............(-y)right
	#					  :
	#					  :
	#					  :
	#					  :
	#					 (-x)

	# increase height_bias to move higher, or decrease height_bias to move lower
	height_bias = 153
	

	grab_direct = "front"
	
	#coords_ready= [194.3,-75.4,263.9,-170.21,2.36,-138.09]
	coords_ready=[155.4, -65.3, 254.4, -174.1, 0.34, -134.95]
	
	GRAB_MOVE_SPEED = 60

	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams = GrabParams()

