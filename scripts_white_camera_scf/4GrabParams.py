#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	# ratio = 0.198 
	ratio = 0.202
    #ratio = 0.175
	#ratio =  0.153
	# ratio = 0.206 #front
	# increase x_bias to move front, or decrease x_bias to move back
	x_bias = 40 
 
	#x_bias = 5
	# x_bias = 0
	# increase y_bias to move left, or decrease y_bias to move right
	y_bias = 30
 
	#y_bias = -70
	# y_bias = 0

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
	height_bias = 177.15
	# height_bias = 343.9

	grab_direct = "front"
	# coords_ready = [190, -30, 245, -175, 0, -134,-43]
	coords_ready = [194, -45, 245, -173, 0, -133]
	# coords_ready = [53.7, 112.0, 318.0, -85.93, 45.13, 7.59]
	#coords_ready = [-50.7,-130.1,285.6, -85.45, 45.12, -173.88]
 	# coords_ready = [-33.7,-150.1,325.6, -85.45, 45.12, -173.88]
  #coords_ready = [190, -30, 245, -175, 0, -134]
	
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
	
	GRAB_MOVE_SPEED = 20
	PLACE_MOVE_SPEED = 10

	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams = GrabParams()

