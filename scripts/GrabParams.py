#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	ratio =0.2079
	
	# increase x_bias to move front, or decrease x_bias to move back
	x_bias = 5


	# increase y_bias to move left, or decrease y_bias to move right
	y_bias = 27

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
	height_bias = 145
	

	grab_direct = "front"
	coords_ready = [169.3, -42.5, 219.9, 178.83, 10.06, -133.16]
	# 左半边放置坐标（第1组：第一只猫+第一只鸟）
	coords_left = [231.0, 144.4, 155.5, 177.54, 8.39, -47.28]

	# 右半边放置坐标（第2组：第二只猫+第二只鸟）
	coords_right = [207.6, -177.6, 155.7, -171.67, 4.64, -48.74]

	# grab_direct = "right"
	# if grab_direct == "right":
	# 	y_bias = -5
	# 	x_bias = 40
	# 	coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
	
	GRAB_MOVE_SPEED = 15

	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams = GrabParams()

