#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

	# get the results by calibration
	ratio = 0.269
	# increase x_bias to move front, or decrease x_bias to move back
	#x_bias = -6
	#x_bias = 0

	# increase y_bias to move left, or decrease y_bias to move right
	#y_bias = 35
	#y_bias = 0
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
	height_bias = 360
	#height_bias = -145
	

	#grab_direct = "front"
	#coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
	#coords_ready = [210, -30, 240, -175, 0, -138]
	#coords_ready = [-62.8, -65.4, 365.8, 91.2, 43.03, 1.69]
	#coords_ready = [51.2, -64.3,300, -92.1, -0.22,-91.22]
	#coords_ready =[-8.2, -18.2, 412.5, 90.18, 40.15, -171.88]
	#coords_ready =[2.1, -17.8, 412.6, -89.99, -0.35, 0.43]
	#coords_ready =[64.9, 47.1, 411.0, -92.78, -45.98, 0.24]


	grab_direct = "right"
	if grab_direct == "right":
		y_bias = -105 
		x_bias = 69
		#coords_ready = [-59.3, -181.2, 252.8, -178.51, 0.28, 135]
		coords_ready = [-62.8, -65.4, 365.8, 91.2, 43.03, 1.69]
	
	GRAB_MOVE_SPEED = 20

	# show image and waitkey
	debug = True #True         

	# please do not change the parameter values below
	IMG_SIZE = 640
	done = False
	cap_num = 2
	usb_dev = "/dev/arm"
	baudrate = 115200

grabParams = GrabParams()

