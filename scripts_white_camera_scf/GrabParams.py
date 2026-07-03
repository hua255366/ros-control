#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	# ratio = 0.198 
	ratio =0.306
 
	#ratio =  0.153
	# ratio = 0.206 #front
	# increase x_bias to move front, or decrease x_bias to move back
	#x_bias =-4#2 13 gray
 	x_bias =5 ##-14

	#x_bias = 5
	# x_bias = 0
	# increase y_bias to move left, or decrease y_bias to move right
	#y_bias = 47#50 gray
 	y_bias =40#65

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
	height_bias = 170#170.9#169.9
	# height_bias = 343.9

	grab_direct = "front"
	# coords_ready = [250, -30, 245, -175, 0, -134,-43]
	#coords_ready = [180, -61.1,274.1, -179.50.8, -141.22]############yuanfeng_whitecamera_version
	#coords_ready = [192.7, -50.0, 265.1, -175.95, 1.3, -133.4]
	#coords_ready =[166.7, -61.1, 274.1, -179.84, 2.56, -138.22]################
	#coords_ready =[190.9, -61.1, 224.1, -173,17,-141.4]
	coords_ready =[217, -30, 237.2, -175, 3, -135]

	coords_ready_left_1 = [268.3, 134.3, 158.8, -137.1, -27.85, -58.97]#[130, 220, 180, -175, -10, -43]
	coords_ready_left_2 =[290.9, 62.1, 173.4, -145.37, -25.44, -55.2]# [220, 150, 180, -175, -10, -43]
	coords_ready_right_1 =[261.3, -127.1, 181.3, -137.4, -38.43, -73.86]# [150, -160, 180, -175, 0, -43]
	coords_ready_right_2 = [231.1, -152.4, 190.6, -166.52, -19.43, -59.01]#[210, -120, 180, -175, 0, -43]
	# coords_ready = [53.7, 112.0, 318.0, -85.93, 45.13, 7.59]
	#coords_ready = [-50.7,-130.1,285.6, -85.45, 45.12, -173.88]
 	# coords_ready = [-33.7,-150.1,325.6, -85.45, 45.12, -173.88]
  #coords_ready = [190, -30, 245, -175, 0, -134]
	
	coords_chuhsi=[0,0,0,0,0,0]
	coords_prepre = [60.6, -61.0, 350.9, 86.7, 42.72, 80.5]
  
	#place_coords = [110.6, -71.0, 255.9, 100.7, 42.72, 90.5]
	place_coords = [110.6, -71.0, 255.9, 96.7, 42.72, 90.5]
	#coords_ready_test = [50.6, -81.0, 255.9, 96.7, 42.72, 90.5]
	coords_ready_test = [50.6, -81.0, 258.9, 96.7, 42.72, 90.5]

	# 定义放置积木块的固定区域的坐标
	region_left1 =[255.8, 125.8, 200.6, 142.91, 29.96, 146.03]#[185.7, 146.1, 174.9, -154.17, -17.4, -54.61]#[241.3, 157.8, 207.5, 148.44, 26.26, 122.54] #[268.3, 134.3, 158.8, -137.1, -27.85, -58.97]  # 左边偏移100# [185.7, 146.1, 174.9, -154.17, -17.4, -54.61][255.8, 125.8, 200.6, 142.91, 29.96, 146.03]
	region_left2 = [215.5, 159.6, 182.4, -176.65, -0.56, -46.71]#[185.7, 146.1, 174.9, -154.17, -17.4, -54.61]#[290.9, 62.1, 173.4, -145.37, -25.44, -55.2]
	region_right1 =[261.3, -127.1, 181.3, -137.4, -38.43, -73.86]#[248.1, -105.0, 185.6, 177.8, -5.86, -43.81]  # 右边偏移100
	region_right2 = [231.1, -152.4, 190.6, -166.52, -19.43, -59.01]#[273.9, -103.5, 198.4, -160.01, -31.46, -49.99]


	# grab_direct = "right"
	# if grab_direct == "right":
	# 	y_bias = -5
	# 	x_bias = 40
	# 	coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
	
	GRAB_MOVE_SPEED = 45#45#30
	PLACE_MOVE_SPEED = 45#30

	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams = GrabParams()

