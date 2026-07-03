#encoding: UTF-8
#!/usr/bin/env python2

from GrabParams import grabParams

import time
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle

class Rob_basic(object):

    def __init__(self):
        super(Rob_basic, self).__init__()
        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()
        self.angular = 0 # linear  = 1

    #grap
    def grap(self, flag):
        if flag:
            # close
            # self.mc.set_gripper_state(1, 0)
            time.sleep(0.1)
            self.mc.set_gripper_value(45,30)  
            time.sleep(2)
        else:
            # open
            time.sleep(0.1)
            self.mc.set_gripper_value(255,30)
            time.sleep(2)

    def move_to_my_coords(self,coords,speed,times):
        print("move_to_my_coords")
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.mc.send_coords(coords,speed,self.angular)
        time.sleep(times)

    def move_to_my_coords2(self,coords,speed,times):
        print("move_to_my_coords")
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.mc.send_coords(coords,speed,1)
    # self.mc.send_coords(coords,speed,self.angular)
        time.sleep(times)
        

    def move_to_my_angles(self,angles,speed,times):
        print("move_to_my_angles")
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.mc.send_angles(angles,speed)
        time.sleep(times)

# def move_to_target_coords(coords,speed):
#     print("move_to_target_coords")
#     mc.set_color(0,0,255)#blue, arm is busy
#     mc.send_coords(coords,speed,angular)
#     time.sleep(4)


# def move_to_target_coords2(coords,speed):
#     print("move_to_target_coords")
#     mc.set_color(0,0,255)#blue, arm is busy
#     time.sleep(0.1)
#     mc.send_coords(coords,speed,angular)
    
#     count = 0
#     while 1:
#         time.sleep(0.1)
#         is_finised = mc.is_in_position(coords,1);
#         print(is_finised)
        
#         coords_now = mc.get_coords()
#         if len(coords_now)<6:
#             continue
#         dx = coords_now[0] - coords[0]
#         dy = coords_now[1] - coords[1]
#         dz = coords_now[2] - coords[2]
#         print(dx,dy,dz)
#         if abs(dx) >4 or abs(dy)>4:
#             continue
#         else:
#             count +=1            
            
#             if count >= 5:
#                 print(coords)    
#                 print(coords_now)                
#                 break

# def get_coords():
#     coords_now = []
#     count = 0
#     while len(coords_now)<6 and count < 6:  
#         time.sleep(0.5)            
#         coords_now = mc.get_coords()        
#         print("get_coords ", coords_now, count)
#         count = count + 1
        
#     return coords_now


# def get_angles():
#     angles = mc.get_angles()
#     while len(angles)<6:
#         angles = mc.get_angles()
#     return angles

# def release_servo(servo_id):
#     mc.release_servo(servo_id)

# def release_all_servos():
#     mc.release_all_servos()

# def focus_servo(servo_id):
#     mc.focus_servo(servo_id)

# def focus_all_servos():
#     for servo_id in range(1,7):
#         mc.focus_servo(servo_id)
#         time.sleep(0.2)
