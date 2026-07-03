#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams2(object):

	# get the results by calibration
	# ratio = 0.198 
	ratio = 0.171
 
	#ratio =  0.153
	# ratio = 0.206 #front
	# increase x_bias to move front, or decrease x_bias to move back
	#x_bias =-4#2 13 gray
 	x_bias = -4

	#x_bias = 5
	# x_bias = 0
	# increase y_bias to move left, or decrease y_bias to move right
	#y_bias = 47#50 gray
 	y_bias = 47

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
	height_bias = 170.9#170.9#160.9
	# height_bias = 343.9

	grab_direct = "front"
	# coords_ready = [190, -30, 245, -175, 0, -134,-43]
	coords_ready = [190, -30, 245, -173, 0, -133]
	coords_ready_left_1 = [130, 220, 180, -175, -10, -43]
	coords_ready_left_2 = [220, 150, 180, -175, -10, -43]
	coords_ready_right_1 = [150, -160, 180, -175, 0, -43]
	coords_ready_right_2 = [210, -120, 180, -175, 0, -43]
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
	region_left1 = [214.9, 153.7, 199.2, -174.92, -5.11, -39.65]  # 左边偏移100
	region_left2 = [253.1, 148.4, 188.6, -153.66, -23.43, -53.94]
	region_right1 = [248.1, -105.0, 185.6, 177.8, -5.86, -43.81]  # 右边偏移100
	region_right2 = [273.9, -103.5, 198.4, -160.01, -31.46, -49.99]


	# grab_direct = "right"
	# if grab_direct == "right":
	# 	y_bias = -5
	# 	x_bias = 40
	# 	coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
	
	GRAB_MOVE_SPEED = 30
	PLACE_MOVE_SPEED = 20

	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams2 = GrabParams2()

