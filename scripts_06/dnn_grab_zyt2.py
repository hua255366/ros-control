#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
# import rospy
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="True")
args = parser.parse_args()

height_bias = grabParams.height_bias
coords = grabParams.coords_ready
coords2 = grabParams.coords_ready
coords3 = grabParams.coords_chuhsi


coords_left1 = grabParams.region_left1
coords_left2 = grabParams.region_left2
coords_right1 = grabParams.region_right1
coords_right2 = grabParams.region_right2

done = grabParams.done

CLASSES = ("apple", "clock", "banana","cat ","bird ") #[0,1,2,3,4]

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
        self.c_x, self.c_y = grabParams.IMG_SIZE/2, grabParams.IMG_SIZE/2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio


    # Grasping motion
    def move(self, x, y,max_pairs):
        global height_bias, done
        # 抓取动作
        coords_target = coords2
        # coords_target = [coords[0]+int(x), coords[1]+int(y), height_bias, coords[3], coords[4], coords[5]]
        coords_target = [n_final+int(x), m_final+int(y), height_bias, coords[3], coords[4], coords[5]]
        print("coords_target=",coords_target)
        basic.move_to_target_coords(coords_target, grabParams.GRAB_MOVE_SPEED)
        

        basic.grap(True)
        if coords_target[0] >= 230:
            coords_target[0] = coords_target[0]-20
        # 返回准备阶段
        time.sleep(1)
        coords_target1 = [coords_target[0], coords_target[1]-30, height_bias+50, coords_target[3], coords_target[4], coords_target[5]]
        print("coords_target1=",coords_target1)
        basic.move_to_target_coords(coords_target1, grabParams.GRAB_MOVE_SPEED)
        # 放置动作
        time.sleep(1)

        if sum == 3 and put_cat == 0:
            #目的地
            basic.move_to_target_coords(grabParams.coords_ready, grabParams.GRAB_MOVE_SPEED)
            time.sleep(3)
            basic.move_to_target_coords(coords_left1, grabParams.GRAB_MOVE_SPEED)
            basic.grap(False)
            time.sleep(1)
            
        if sum == 4 and put_bird == 0:
            basic.move_to_target_coords(grabParams.coords_ready, grabParams.GRAB_MOVE_SPEED)
            time.sleep(3)
            basic.move_to_target_coords(coords_left2, grabParams.GRAB_MOVE_SPEED)
            basic.grap(False)
            time.sleep(1)
            
       
            
        # 放置右边 
        if sum == 3 and put_cat != 0:
            basic.move_to_target_coords(grabParams.coords_ready, grabParams.GRAB_MOVE_SPEED)
            time.sleep(3)
            basic.move_to_target_coords(coords_right1, grabParams.GRAB_MOVE_SPEED)
            basic.grap(False)
            time.sleep(1)
            basic.grap(False)
            
        if sum == 4 and put_bird != 0:
            basic.move_to_target_coords(grabParams.coords_ready, grabParams.GRAB_MOVE_SPEED)
            time.sleep(3)
            basic.move_to_target_coords(coords_right2, grabParams.GRAB_MOVE_SPEED)
            basic.grap(False)
            time.sleep(1)
            basic.grap(False)
            

        # # 放置左边
        # if sum == 3 and put_cat == 0:
        #     coords_target_left1 = [coords[0], coords[1]+210, height_bias+10, coords[3], coords[4], coords[5]]
        #     basic.move_to_target_coords(coords_target_left1, grabParams.GRAB_MOVE_SPEED)
        #     basic.grap(False)  # 打开夹子
        #     time.sleep(1)
        #     coords_target_left1_back = [coords[0], coords[1]+210, height_bias+20, coords[3], coords[4], coords[5]]
        #     basic.move_to_target_coords(coords_target_left1_back, grabParams.GRAB_MOVE_SPEED)
        # if sum == 4 and put_bird == 0:
        #     coords_target_left2 = [coords[0], coords[1]+180, height_bias+10, coords[3], coords[4], coords[5]]
        #     basic.move_to_target_coords(coords_target_left2, grabParams.GRAB_MOVE_SPEED)
        #     basic.grap(False)
        #     time.sleep(1)
        #     coords_target_left2_back = [coords[0], coords[1]+180, height_bias+20, coords[3], coords[4], coords[5]]
        #     basic.move_to_target_coords(coords_target_left2_back, grabParams.GRAB_MOVE_SPEED)
        # # 放置右边 
        # if sum == 3 and put_cat != 0:
        #     coords_target_right1 = [coords[0], coords[1]-60, height_bias+10, coords[3], coords[4], coords[5]]
        #     basic.move_to_target_coords(coords_target_right1, grabParams.GRAB_MOVE_SPEED)
        #     basic.grap(False)
        #     time.sleep(1)
        #     coords_target_right1_back = [coords[0], coords[1]-60, height_bias+20, coords[3], coords[4], coords[5]]
        #     basic.move_to_target_coords(coords_target_right1_back, grabParams.GRAB_MOVE_SPEED)
        # if sum == 4 and put_bird != 0:
        #     coords_target_right2 = [coords[0], coords[1]-50, height_bias+10, coords[3], coords[4], coords[5]]
        #     basic.move_to_target_coords(coords_target_right2, grabParams.GRAB_MOVE_SPEED)
        #     basic.grap(False)
        #     time.sleep(1)
        #     coords_target_right2_back = [coords[0], coords[1]-50, height_bias+20, coords[3], coords[4], coords[5]]
        #     basic.move_to_target_coords(coords_target_right2_back, grabParams.GRAB_MOVE_SPEED)

        # time.sleep(2)
        # angles = [0, 0, 0, 0, 0, 0]
        # self.mc.send_angles(angles,30)
        
        # if max_pairs == 2 or max_pairs == 3:
        #     time.sleep(1)
        #     angles = [0, 0, 0, 0, 0, 0]
        #     self.mc.send_angles(angles,30)
        #     time.sleep(8)
        #     basic.move_to_target_coords(coords2, grabParams.GRAB_MOVE_SPEED)
        #     print("coords_back=",coords2)
        # else:

        # 返回准备阶段
        time.sleep(2)
        basic.move_to_target_coords(final_target, grabParams.GRAB_MOVE_SPEED)
        print("final_target=",final_target)
        time.sleep(5)




        if max_pairs == 1:
            done = True
            print("Done")
            self.mc.set_color(0,255,0)#green, arm is free
        else:
            done = False


    # init mycobot
    def init_mycobot(self): 
        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
        basic.grap(False)      
        time.sleep(1)         
        basic.move_to_target_coords(coords,grabParams.GRAB_MOVE_SPEED) 
 


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

    #图像处理，适配物体识别
    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))

        return frame
   
    
    # detect object
    def obj_detect(self, img):
        x=y=0
        i=0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

          
        #加载模型
        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")
        #net = cv2.dnn.readNetFromONNX(grabParams.ONNX_MODEL)
        t1 = time.time()
        #输入数据处理
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        
        #推理
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]
        
        
        #获得识别结果
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)
        t2 = time.time()

        img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if boxes is not None:
            boxes = boxes*5
            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])
            left, top, right, bottom = boxes[0]
            x = int((left+right)/2)
            y = int((top+bottom)/2)
            # print x, y

        self.show_image(img_ori)  

        # Print time (inference-only)
        print("time: " + str(t2-t1) + "s")  
        i+=1
        print("i=",i)
      
        if x+y > 0 and (classes[0]==3 or classes[0]==4):
            return x, y,classes
        else:
            angles = [0, 0, 0, 0, 0, 0]
            self.mc.send_angles(angles,30)
            return None

    def run(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.init_mycobot()

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(50) 
        


if __name__ == "__main__":

    
    detect = Detect_marker()
    detect.run()   

    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5) 

    init_num = 0
    nparams = 0
    num = 0
    miss = 0

    # 抓取数量为4
    max_pairs = 4
    # 抓取方向
    put_cat = 0
    put_bird = 0 
    n = coords2[0]
    n2 = coords2[0]
    n_final = coords2[0]
    m_final = coords2[1]
    zhuaq_x = coords2[0]
    zhuaq_y = coords2[1]
    flag = 0 
    final_target = coords2

    while cv2.waitKey(1) < 0 and not done:
        # read camera
        frame = cap.read()
        
        # get detect result
        detect_result = detect.obj_detect(frame)
        
         
        
        if detect_result is None:
            if n < 220:
                n+=20
                n_final = n
                print("n=",n)
                time.sleep(2)
                coords_target1_test = [n, coords2[1], coords2[2], coords2[3], coords2[4], coords2[5]]
                basic.move_to_target_coords(coords_target1_test, grabParams.GRAB_MOVE_SPEED)
                final_target = coords_target1_test
            elif zhuaq_y < 50:
                if flag == 0:
                    zhuaq_x = n2
                    zhuaq_y += 70
                    time.sleep(2)
                    n_final = zhuaq_x
                    m_final = zhuaq_y
                    target2 = [zhuaq_x, zhuaq_y, coords2[2], coords2[3], coords2[4], coords2[5]]
                    basic.move_to_target_coords(target2, grabParams.GRAB_MOVE_SPEED)
                    final_target = target2
                    flag = 1
                elif n2<220 and flag == 1:
                    n2 += 20
                    zhuaq_x = n2
                    n_final = zhuaq_x
                    time.sleep(2)
                    target3 = [zhuaq_x, zhuaq_y, coords2[2], coords2[3], coords2[4], coords2[5]]
                    basic.move_to_target_coords(target3, grabParams.GRAB_MOVE_SPEED) 
                    final_target = target3

      
            continue
        else:        
            x, y, classes = detect_result
            print("classes=",classes)
            #类别的数值
            sum = classes[0]
            print("sum=",sum) 
            # calculate real coord between cube and mycobot, unit mm
            real_x, real_y = detect.get_position(x, y)
            # print(real_x, real_y) 
            coords_now = basic.get_coords()
            if len(coords_now) == 6:
                coords = coords_now
            detect.move(real_x + grabParams.x_bias, real_y + grabParams.y_bias,max_pairs)
            if sum == 3:
                put_cat +=1
            elif sum == 4:
                put_bird +=1
            print(put_cat,put_bird)    
            max_pairs -= 1
            print("put_cat,put_bird",put_cat,put_bird)


    cap.close()

   
