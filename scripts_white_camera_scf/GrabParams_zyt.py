#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	ratio = 0.170 #front0.206
	# increase x_bias to move front, or decrease x_bias to move back
	# x_bias = -40
	x_bias = -40
	# x_bias = 45
	# increase y_bias to move left, or decrease y_bias to move right
	# y_bias = 45
	y_bias = 30
	# y_bias = 50

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
	height_bias = 230


	grab_direct = "front"
	coords_ready = [190, -30, 245, -175, 0, -134]
	#place_coords = [190, -30, 245, -175, 0, -134]
	# grab_direct = "right"
	 #if grab_direct == "right":
	 #	y_bias = -5
	 #	x_bias = 40
	 #	coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
	
	
	GRAB_MOVE_SPEED = 20
	#PLACE_MOVE_SPEED = 20
	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200
	
    # 公共货架抓取，左边
	coords_left_ready= [53.7, 112.0, 318.0, -85.93, 45.13, 7.59] # 向左高初始状态
	
	coords_left_put_ready = [53.7, 112.0, 220.0, -85.93, 45.13, 7.59] # 向左低初始状态
	 # 公共货架抓取
	coords_right_ready = [-50.7,-130.1,315.6, -85.45, 45.12, -173.88]

	coords_right_put_ready = [-50.7,-130.1,230.0, -85.45, 45.12, -173.88]



grabParams = GrabParams()

