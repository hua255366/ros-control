import cv2
import numpy as np
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle
import time
import basic
from GrabParams import grabParams
import math
import rospy
from geometry_msgs.msg import Twist

rospy.init_node('movement', anonymous=True)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(20) # 20hz
move_cmd = Twist()

mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
mc.set_color(0,0,255)#blue, arm is busy   

mc.set_gripper_value(255,30)
time.sleep(3)

angles = [-90, -20, 0, 25, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

lower_blue = np.array([100,43,46])
upper_blue = np.array([124,255,255])

lower_red = np.array([170, 120, 120])
upper_red = np.array([180,255,255])

lower_yellow = np.array([26, 43, 46])
upper_yellow = np.array([34, 255, 255])

lower_green = np.array([35,43,35])
upper_green = np.array([90,255,255])

lower_purple = np.array([125,43,46])
upper_purple = np.array([155,255,255])

lower_orange = np.array([11,43,46])
upper_orange = np.array([25,255,255])

cap = cv2.VideoCapture(2)

while True:
    
    move_cmd.linear.x = 0.02 #m/s
    move_cmd.linear.z = 0 #m/s
    pub.publish(move_cmd)

    retval,frame = cap.read()

    flag = 0
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_purple, _ = cv2.findContours(mask_purple, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #red
    for contour_red in contours_red:
        area_red = cv2.contourArea(contour_red)
        if area_red > 5000 and area_red < 10000:  
            x_red, y_red, w_red, h_red = cv2.boundingRect(contour_red)
            cv2.rectangle(frame, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 255, 0), 2)
            print("x_red:",x_red,"y_red:", y_red)
            if(x_red>235 and x_red <270) and (y_red>130 and y_red <190):
                flag = 1
    #yellow
    for contour_yellow in contours_yellow:
        area_yellow = cv2.contourArea(contour_yellow)
        if area_yellow > 5000 and area_yellow < 10000:  
            x_yellow, y_yellow, w_yellow, h_yellow = cv2.boundingRect(contour_yellow)
            cv2.rectangle(frame, (x_yellow, y_yellow), (x_yellow + w_yellow, y_yellow + h_yellow), (0, 255, 0), 2)
            print("x_yellow:",x_yellow,"y_yellow:", y_yellow)
            if(x_yellow>235 and x_yellow <270) and (y_yellow>130 and y_yellow <190):
                flag = 1
    #blue
    for contour_blue in contours_blue:
        area_blue = cv2.contourArea(contour_blue)
        if area_blue > 5000 and area_blue<10000 :  
            x_blue, y_blue, w_blue, h_blue = cv2.boundingRect(contour_blue)
            cv2.rectangle(frame, (x_blue, y_blue), (x_blue + w_blue, y_blue + h_blue), (0, 255, 0), 2)
            print("x_blue:",x_blue,"y_blue:", y_blue)
            if(x_blue>235 and x_blue <270) and (y_blue>130 and y_blue <190):
                flag = 1
    #green
    for contour_green in contours_green:
        area_green = cv2.contourArea(contour_green)
        if area_green > 5000 and area_green < 10000:  
            x_green, y_green, w_green, h_green = cv2.boundingRect(contour_green)
            cv2.rectangle(frame, (x_green, y_green), (x_green + w_green, y_green + h_green), (0, 255, 0), 2)
            print("x_green:",x_green,"y_green:", y_green)
            if(x_green>235 and x_green <270) and (y_green>130 and y_green <190):
                flag = 1
    #purple            
    for contour_purple in contours_purple:
        area_purple = cv2.contourArea(contour_purple)
        if area_purple > 5000 and area_purple < 10000:  
            x_purple, y_purple, w_purple, h_purple = cv2.boundingRect(contour_purple)
            cv2.rectangle(frame, (x_purple, y_purple), (x_purple + w_purple, y_purple + h_purple), (0, 255, 0), 2)
            print("x_purple:",x_purple,"y_purple:", y_purple)
            if(x_purple>235 and x_purple <270) and (y_purple>130 and y_purple <190):
                flag = 1
    #orange
    for contour_orange in contours_orange:
        area_orange = cv2.contourArea(contour_orange)
        if area_orange > 5000 and area_orange < 10000:  
            x_orange, y_orange, w_orange, h_orange = cv2.boundingRect(contour_orange)
            cv2.rectangle(frame, (x_orange, y_orange), (x_orange + w_orange, y_orange + h_orange), (0, 255, 0), 2)
            print("x_orange:",x_orange,"y_orange:", y_orange)
            if(x_orange>235 and x_orange <270) and (y_orange>130 and y_orange <190):
                flag = 1

    cv2.imshow('frame', frame)
    if flag == 1:
        break
    #cv2.imshow('Color Recognition', ret)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

move_cmd.linear.x = 0 #m/s
move_cmd.linear.z = 0 #m/s
pub.publish(move_cmd)

cap.release()
cv2.destroyAllWindows()

angles = [-90, -35, -3, 49, -2, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_gripper_value(40,30)
time.sleep(3)

angles = [-90, 0, 0,0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, 50, -150,110, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, -25, -80,110, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_gripper_value(255,30)
time.sleep(3)

angles = [-90, 25, -100,110, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

angles = [-90, 0, 0,0, 0, -45]
mc.send_angles(angles,30)
time.sleep(3)

mc.set_color(0,255,0)#green, arm is free