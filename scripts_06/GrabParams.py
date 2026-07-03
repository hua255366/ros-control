#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	#ratio = 0.193#0.300
	ratio = 0.262
 
	# increase x_bias to move front, or decrease x_bias to move back
	#x_bias = -1
	x_bias = 3

  #x_bias = -10#-30
  
	# increase y_bias to move left, or decrease y_bias to move right
	y_bias = 35

  #y_bias = 40
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
	height_bias = 175
	

	grab_direct = "front"
	#coords_ready = [165, -50, 245, -175, 20, -136]
	coords_ready = [193, -50, 235, -180, 10, -139]
	coords_ready_left_1 = [130, 220, 180, -175, -10, -43]
	#coords_ready_left_2 = [220, 150, 180, -175, -10, -43]
	coords_ready_left_2 = [220, 150, 180, -175, -10, -43]
	coords_ready_right_1 = [150, -160, 180, -175, 0, -43]
	coords_ready_right_2 = [210, -120, 180, -175, 0, -43]
	coords_chuhsi=[0,0,0,0,0,0]
	coords_prepre = [60.6, -61.0, 350.9, 86.7, 42.72, 90.5]
  
	#place_coords = [110.6, -71.0, 255.9, 100.7, 42.72, 90.5]
	place_coords = [110.6, -71.0, 255.9, 96.7, 42.72, 90.5]
	#coords_ready_test = [50.6, -81.0, 255.9, 96.7, 42.72, 90.5]
	coords_ready_test = [50.6, -81.0, 258.9, 96.7, 42.72, 90.5]

	# 定义放置积木块的固定区域的坐标
	region_left1 = [130, 220, 180, -175, -10, -43]  # 左边偏移100
	region_left2 = [220, 150, 180, -175, -10, -43]
	region_right1 = [150, -160, 180, -175, 0, -43]   # 右边偏移100
	region_right2 = [210, -120, 180, -175, 0, -43]
	
	# grab_direct = "right"
	# if grab_direct == "right":
	# 	y_bias = -5
	# 	x_bias = 40
	# 	coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
	
	
	GRAB_MOVE_SPEED = 32

	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams = GrabParams()

