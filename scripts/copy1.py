#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	ratio = 0.333
	
	# increase x_bias to move front, or decrease x_bias to move back
	x_bias = 20

	# increase y_bias to move left, or decrease y_bias to move right
	y_bias = 10

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
	height_bias = 170
	

	grab_direct = "right"
	coords_ready = [217, -30, 237.2, -175, 3, -135]
	#coords_ready = [190,-60,245,-175,12.5,-137]
	#coords_ready = [-64.1,-233.5,200.6,175.95,-0.11,135.28]

	# grab_direct = "right"
	# if grab_direct == "right":
	# 	y_bias = -5
	# 	x_bias = 40
	# 	coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
	
	GRAB_MOVE_SPEED = 20

	# show image and waitkey
	debug = True #	IMG_SIZE = 640
True         

	# please do not change the parameter values below
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams = GrabParams()