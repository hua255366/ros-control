# encoding: UTF-8





# !/usr/bin/env python2





import cv2



import os



import numpy as np



import time



import rospy



from pymycobot.mycobot import MyCobot



from opencv_yolo import yolo



# from VideoCapture import FastVideoCapture





import math



from GrabParams import grabParams



import basic



import argparse



add1 = 5



add2 = 5



parser = argparse.ArgumentParser(description='manual to this script')



parser.add_argument("--debug", type=bool, default="True")



args = parser.parse_args()



height_bias = grabParams.height_bias



coords = grabParams.coords_ready



done = grabParams.done



CLASSES = ( "cat ", "bird ")





class Detect_marker(object):



    def __init__(self):



        super(Detect_marker, self).__init__()



        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)



        self.mc.power_on()



        self.yolo = yolo()



        # parameters to calculate camera clipping parameters



        self.x1 = self.x2 = self.y1 = self.y2 = 0



        # use to calculate coord between cube and mycobot



        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0



        # The coordinates of the grab center point relative to the mycobot



        # The coordinates of the cube relative to the mycobot



        self.c_x, self.c_y = grabParams.IMG_SIZE / 2, grabParams.IMG_SIZE / 2



        # The ratio of pixels to actual values



        self.ratio = grabParams.ratio



    # Grasping motion



    def move(self, x, y):



        global height_bias, done



        coords_target = [coords[0] + int(x) - 4, coords[1] + int(y) , height_bias, coords[3], coords[4], coords[5]]



        basic.move_to_target_coords(coords_target, grabParams.GRAB_MOVE_SPEED)



        basic.grap(True)



        angles = [10.1, -22.76, -20.3, -28.74, -5.27, 57.56]



        self.mc.send_angles(angles, 30)



        time.sleep(1.5)



        done = True



        print("Done")



        self.mc.set_color(0, 255, 0)



    def init_mycobot(self):



        basic.grap(False)



        time.sleep(1)



        basic.move_to_target_coords(coords, grabParams.GRAB_MOVE_SPEED)



        # calculate the coords between cube and mycobot



    def get_position(self, x, y):



        # print "self.ratio: ", self.ratio



        # return (-(x - self.c_x)*self.ratio), (-(y - self.c_y)*self.ratio)



        wx = wy = 0



        if grabParams.grab_direct == "front":



            wx = (self.c_y - y) * self.ratio



            wy = (self.c_x - x) * self.ratio







        elif grabParams.grab_direct == "right":



            wx = (self.c_x - x) * self.ratio



            wy = (y - self.c_y) * self.ratio



        return wx, wy



    def transform_frame(self, frame):



        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))



        return frame



    def transform_frame_128(self, frame):



        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))



        return frame



    # detect object



    def obj_detect(self, img):



        x = y = 0



        img_ori = img



        img_ori = self.transform_frame(img)



        img = self.transform_frame_128(img)



        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")



        t1 = time.time()



        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)



        net.setInput(blob)



        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]



        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)



        t2 = time.time()



        # img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)



        if boxes is not None:

            boxes = boxes * 5



            detected_class = classes[0]



            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])



            left, top, right, bottom = boxes[0]



            x = int((left + right) / 2)



            y = int((top + bottom) / 2)



            # print x, y



        cv2.imshow("figure", img_ori)



        cv2.waitKey(10)



        # Print time (inference-only)



        print("time: " + str(t2 - t1) + "s")



        if x + y > 0:



            return x, y, detected_class







        else:



            return None



    def run(self):



        self.mc.set_color(0, 0, 255)  # blue, arm is busy



        self.init_mycobot()



    def show_image(self, img):



        if grabParams.debug and args.debug:

            cv2.imshow("figure", img)



            cv2.waitKey(50)



        # -------------------------------------------------------------------------------------------------------------



    def grap(self, flag):



        if flag:



            # close



            # self.mc.set_gripper_state(1, 0)



            self.mc.set_gripper_value(40, 0)



            time.sleep(1)







        else:



            # open



            self.mc.set_gripper_state(0, 0)



            time.sleep(1)



    def move_to_target_coords(self, coords, speed):



        print("move_to_target_coords")



        self.mc.send_coords(coords, speed, 1)



        time.sleep(2)



    # Grasping motion



    def run_put_down_left_1(self):



        angles_1_1 = [49.04, -66.26, -20.91, 20.39, -5.53, 56.77]



        angles_1_2 = [37.17, -89.38, 61.52, -7.91, 7.73, 33.39]



        #########################################################



        angles = [-2.84, -24.52, -20.03, -34.72, -5, 45.95]

        angles_1_3 = [37.17, -89.38, 75, -15, 7.73, 33.39]



        #########################################################



        coords_0 = [185.3, -57.5, 261.5, -175.27, -1.25, -144.42]



        self.grap(True)



        self.mc.send_angles(angles_1_1, 40)



        time.sleep(1)



        self.grap(False)



        print("open")



        #########################################



        self.mc.send_angles(angles_1_3, 40)



        time.sleep(2)



        #########################################



        # angles_1_2 =[56.95, 0,0,0,0,0]



        #self.move_to_target_coords(coords_0, grabParams.GRAB_MOVE_SPEED)



        ##################################################

        self.mc.send_angles(angles, 40)   

        ##################################################



        time.sleep(2)



    def run_put_down_left_2(self):



        angles_1_2 = [55.35, -25.87, -88.85, 40.17, -6.24, 48.16]



        #######################################################



        angles_1_3 = [55.35, -25.87, 75, -15, 7.73, 33.39]

        angles = [-2.84, -24.52, -20.03, -34.72, -5, 45.95]



        #########################################################



        coords_0 = [185.3, -57.5, 261.5, -175.27, -1.25, -144.42]



        self.grap(True)



        self.mc.send_angles(angles_1_2, 40)



        time.sleep(1)



        self.grap(False)



        print("open")



        #########################################



        self.mc.send_angles(angles_1_3, 40)



        time.sleep(2)



        #########################################



        #self.move_to_target_coords(coords_0, grabParams.GRAB_MOVE_SPEED)



        ##################################################

        self.mc.send_angles(angles, 40)   

        ##################################################



        time.sleep(2)



    def run_put_down_right_1(self):



        angles_2_1 = [-25.77, -52.21, -25.93, -11.51, -5.27, 57.65]



        angles_2_2 = [-29.53, 0, 0, 0, 0, 0]

        # angles_2_2 = [-20.03, -58.35, -13.53, 4.39, 4.65, 44.91]



        #######################################################



        angles_2_3 = [-20.03, -58.35, 75, -15, 7.73, 33.39]

        angles = [-2.84, -24.52, -20.03, -34.72, -5, 45.95]



        #########################################################



        coords_0 = [185.3, -57.5, 261.5, -175.27, -1.25, -144.42]



        self.grap(True)



        self.mc.send_angles(angles_2_1, 40)



        time.sleep(1)



        self.grap(False)



        print("open")



        #########################################



        self.mc.send_angles(angles_2_3, 40)



        time.sleep(2)



        #########################################



        # angles_2_2=[-29.53,0,0,0,0,0]



        #self.move_to_target_coords(coords_0, grabParams.GRAB_MOVE_SPEED)



        ##################################################

        self.mc.send_angles(angles, 40)   

        ##################################################



        time.sleep(2)



    def run_put_down_right_2(self):



        angles_2_2 = [-15.94, -40.42, -83.18, 39.99, -6.76, 22.32]



        #######################################################



        angles_2_3 = [-15.94, -40.42, 75, -15, 7.73, 33.39]

        angles = [-2.84, -24.52, -20.03, -34.72, -5, 45.95]



        #########################################################



        # angles_2_3 = [37.17, -89.38, 50, -15, 7.73, 33.39]      



        coords_0 = [185.3, -57.5, 261.5, -175.27, -1.25, -144.42]



        self.grap(True)



        self.mc.send_angles(angles_2_2, 40)



        time.sleep(1)



        self.grap(False)



        print("open")



        #########################################



        self.mc.send_angles(angles_2_3, 40)



        time.sleep(2)



        #########################################



        # self.mc.send_angles(angles_2_3, 40)                      



        # time.sleep(2)

        #self.move_to_target_coords(coords_0, grabParams.GRAB_MOVE_SPEED)



        ##################################################

        self.mc.send_angles(angles, 40)   

        ##################################################



        time.sleep(2)





i = 0



left = 1



right = 1



detect = Detect_marker()



detect.run()



while i < 4:



    cap = cv2.VideoCapture(2)



    # cap = FastVideoCapture(grabParams.cap_num)



    # time.sleep(0.5) 



    init_num = 0



    nparams = 0



    num = 0



    miss = 0



    while True:



        retval, frame = cap.read()



        frame = cv2.flip(frame, 0)



        frame = cv2.flip(frame, 1)



        detect_result = detect.obj_detect(frame)



        if detect_result is None:



            continue







        else:



            x, y, class_detected = detect_result



            real_x, real_y = detect.get_position(x, y)



            coords_now = basic.get_coords()



            if len(coords_now) == 6:

                coords = coords_now



            detect.move(real_x + grabParams.x_bias-2, real_y + grabParams.y_bias)



            print("class_detected:", class_detected)



            break



    cap.release()



    cv2.destroyAllWindows()



    if i == 0:

        add1 = class_detected



    i += 1



    if detect_result is not None and class_detected == add1 and left == 1:

        detect.run_put_down_left_1()



        print("run_put_down_left_1")



        left += 1



        continue

    if detect_result is not None and class_detected != add1 and right == 1:

        detect.run_put_down_right_1()



        print("run_put_down_right_1")



        right += 1



        continue



    if detect_result is not None and class_detected == add1 and left != 1:

        

        detect.run_put_down_right_2()



        print("run_put_down_right_2")



        continue



    if detect_result is not None and class_detected != add1 and right != 1:

        detect.run_put_down_left_2()



        print("run_put_down_left_2")



        continue