#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
import rospy
from geometry_msgs.msg import Twist
from pymycobot.mycobot import MyCobot
from opencv_yolo import yolo
from VideoCapture import FastVideoCapture
import math
from GrabParams import grabParams
import basic
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="False")
args = parser.parse_args()

done = grabParams.done

class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()
        rospy.init_node('grab_right', anonymous=True)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10) # 10hz
        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on() 
        self.yolo = yolo()
        self.c_x, self.c_y = grabParams.IMG_SIZE/2, grabParams.IMG_SIZE/2
        self.ratio = grabParams.ratio
        self.lv = 940
        self.hr = 2.1
        self.detect_count = 0
        self.clazz = []
        self.direction = 0 
        self.aruco_count = 0

    # Grasping motion
    # 单点进程 竖直方向初次夹取
    def move_high(self, x, y, dist):
        # print(x)
        # if math.fabs(x) > 5:
        #     x = 5
        # global done
        time.sleep(0.2)
        # 抓取
        # 防止离太近 先收回来
        coords_ori = grabParams.coords_right_high
        coords_target = [coords_ori[0] + x,  coords_ori[1] + 30,  coords_ori[2], coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target, 50, 0)
        time.sleep(0.5)
        coords_ori = grabParams.coords_right_high
        coords_target = [coords_ori[0] + x,  coords_ori[1] + 30,  coords_ori[2] + 60, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target, 50, 0)
        time.sleep(0.5)

        # 为了防止卡死先对位置 并往回收防止撞到
        coords_target_2 = [coords_ori[0] + int(x),  coords_ori[1] - 10,  
                            coords_ori[2] + grabParams.bias_right_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target_2, 50, 0)
        time.sleep(0.5) # 等它先到平面上
        # 移动到目标位置 往前推
        coords_target_3 = [coords_ori[0] + int(x) ,  coords_ori[1] + int(y),  
                            coords_ori[2] + grabParams.bias_right_high_z, coords_ori[3], coords_ori[4], coords_ori[5]]
        self.mc.send_coords(coords_target_3, 30, 0)
        time.sleep(1)
        basic.grap(True)
        time.sleep(1)

        # 放回
        self.mc.send_coords(grabParams.coords_pitchdown1, 50, 0) # 先抬高
        time.sleep(0.5)
        self.mc.send_coords(grabParams.coords_pitchdown2, 50, 0)
        time.sleep(1)
        # basic.grap(False) 松抓
        done = True
        time.sleep(1)

        self.mc.set_color(0,255,0) #抓取结束，亮绿灯

    # 充能站放置 
    def move_back(self):
        coords_back = grabParams.coords_back
        time.sleep(0.5)
        self.mc.send_coords(coords_back, 50, 0)
        # 放置
        time.sleep(3)
        coords_target_4 = [coords_back[0],coords_back[1],coords_back[2]-40,coords_back[3],coords_back[4],coords_back[5]]
        self.mc.send_coords(coords_target_4, 30, 0)
        time.sleep(0.5)
        basic.grap(False)
        time.sleep(0.5)
        self.mc.send_coords(coords_back, 50, 0)

    # def move_low(self, x, y, dist):
    # 	if math.fabs(x) > 5:
    # 		x = 5
    # 	# 以下为夹取下层
    # 	# 抓取
    # 	coords_ori = grabParams.coords_right_low
    # 	# 对位置 并往后上方收
    # 	# 往回收一下 防止撞到
    # 	coords_target = [coords_ori[0] + x,  coords_ori[1] + 20, coords_ori[2], coords_ori[3], coords_ori[4], coords_ori[5]]
    # 	self.mc.send_coords(coords_target, 50, 0)
    # 	time.sleep(0.2)
    # 	# coords_target = [coords_ori[0] + grabParams.bias_right_low_x + x,  coords_ori[1] + 10, coords_ori[2], coords_ori[3], coords_ori[4], coords_ori[5]]
    # 	# self.mc.send_coords(coords_target, 50, 0)
    # 	# time.sleep(0.6)
    # 	coords_target1 = [coords_ori[0] + grabParams.bias_right_low_x + x,  coords_ori[1] + grabParams.bias_right_low_y,  
    # 					 coords_ori[2] + grabParams.bias_right_low_z, coords_ori[3], coords_ori[4], coords_ori[5]]
    # 	self.mc.send_coords(coords_target1, 30, 0)
    # 	time.sleep(1)
    # 	# 夹取
    # 	basic.grap(True)
    # 	time.sleep(0.5)
    # 	# 退出前先回撤
    # 	coords_target_2 = [coords_ori[0] + grabParams.bias_right_low_x + x,  coords_ori[1] + grabParams.bias_right_low_y + 60,  
    # 					   coords_ori[2] + grabParams.bias_right_low_z - 20, coords_ori[3], coords_ori[4], coords_ori[5]]
    # 	self.mc.send_coords(coords_target_2, 50, 0)
    # 	time.sleep(0.3)
    # 	#抬高
    # 	coords_target_2 = [coords_ori[0] + grabParams.bias_right_low_x + x,  coords_ori[1] + grabParams.bias_right_low_y + 60,  
    # 					   coords_ori[2] + grabParams.bias_right_low_z - 20, coords_ori[3], coords_ori[4], coords_ori[5]]
    # 	self.mc.send_coords(coords_target_2, 50, 0)
    # 	time.sleep(0.3)

    # 	# 放回
    # 	self.mc.send_coords(grabParams.coords_pitchdown3, 50, 0) # 先抬高
    # 	time.sleep(0.5)
    # 	self.mc.send_coords(grabParams.coords_pitchdown4, 50, 0)
    # 	time.sleep(1)
    # 	basic.grap(False)
    # 	done = True
    # 	time.sleep(1)
        
    # 	self.mc.set_color(0,255,0) #抓取结束，亮绿灯

    def get_position(self, x, y):
        wx = wy = 0
        wx = (self.c_y - y) * self.ratio
        wy = (self.c_x - x) * self.ratio
        # wx = (self.c_x - x) * self.ratio
        # wy = (y - self.c_y) * self.ratio
        return wx, wy
            
    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))
        return frame

    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))

        return frame

    #图像处理，适配物体识别
    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))

        return frame

    def obj_detect(self, img):
        x=y=0
        i=0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        #加载模型
        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")
        
        t1 = time.time()
        #输入数据处理
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        
        #推理
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]

        
        #获得识别结果
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)
        t2 = time.time()
        print("scores=",scores)

        # img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
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
      
        if x+y > 0 :
            return x, y
        else:
            return None
        
    # 优先返回靠右的坐标
    def check_position(self, img):
        x=y=0
        i=0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        #加载模型
        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")
        
        t1 = time.time()
        #输入数据处理
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        
        #推理
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]

        
        #获得识别结果
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)
        t2 = time.time()
        print("scores=",scores)

        # img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
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
      
        if x+y > 0 and scores > 0.7:
            return x, y,classes
        else:
            angles = [0, 0, 0, 0, 0, 0]
            self.mc.send_angles(angles,30)
            return None

    # 优先返回靠左的坐标
    def check_position2(self, img):
        x = y = 0
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        leftmost_box = None
        leftmost_x = float('inf') # 设置一个初始值为正无穷大
        net = cv2.dnn.readNetFromONNX(grabParams.ONNX_MODEL)
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (grabParams.IMG_SIZE, grabParams.IMG_SIZE), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)

        if boxes is not None:
            for i in range(len(classes)):
                # if classes[i] == grabParams.detect_target:
                box = boxes[i]
                x = int((box[0] + box[2]) / 2)
                if x < leftmost_x: # 判断是否为最靠左边的坐标
                    leftmost_box = box
                    leftmost_x = x

            if leftmost_box is not None:
                left, top, right, bottom = leftmost_box
                x = int((left + right) / 2)
                y = int((top + bottom) / 2)
                w = bottom - top
                h = right - left
                cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), 2)
                # cv2.imwrite('/home/cgc/Library/_Compete/2023RoboCom/beetle_ai/img/obj/target.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])

            else:
                done = True
                self.mc.set_color(255, 192, 203)  # 识别不到，亮粉灯
                return None
        # 防止拉回去
        if x > 50:
            return None
        return x, y

    def distance(self, w):
        dist = self.hr / w * self.lv
        dist = dist - 9 - grabParams.set_diff
        return dist

    def aruco(self, frame):
        global done
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        while(1):
            self.aruco_count += 1
            corners, _, _ = cv2.aruco.detectMarkers(
                gray, cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250), parameters=cv2.aruco.DetectorParameters_create()
                )
            if len(corners) > 0:
                x = corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]
                y = corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]
                x = x/4.0
                y = y/4.0
                x_size_p = abs(x - corners[0][0][0][0])*2
                y_size_p = abs(y - corners[0][0][0][1])*2
                lenth = (x_size_p + y_size_p)/2
                dist = self.distance(lenth)
                return dist
            elif self.aruco_count == 3:
                done = True
                self.mc.set_color(255,192,203) #二维码看不到，亮粉灯
                return None

    def run(self):
        self.mc.set_color(0,0,255) #成功调用程序，亮蓝灯
        f = open("/home/robuster/RoboCom/beetle_ai/scripts/direction.txt", "r+")
        self.direction = int(f.read())
        f.seek(0)
        f.truncate()
        f.write('0')
        f.close()

    # 前进后退
    def going(self, dist):
       # 单位为cm
        # if self.direction:
        # go_count = int(dist + grabParams.move_power_high_left + 0.5)
        # else:
        # go_count = int(dist + grabParams.move_power_high_right + 0.5)
        #go_count = int(dist * grabParams.dist_bias)
        go_count = int(dist * 1)
        count = 0
        move_cmd = Twist()
        time.sleep(0.5)
        if go_count >= 0:
            while True:
                move_cmd.linear.x = 0.1
                move_cmd.angular.z = 0.0
                if go_count - count < 2:
                    move_cmd.linear.x = 0.05
                    move_cmd.angular.z = 0
                self.pub.publish(move_cmd)
                count += 1
                if count >= go_count:
                    break
                self.rate.sleep()
        else:
            go_count = -1 * go_count
            while True:
                move_cmd.linear.x = -0.1
                move_cmd.angular.z = 0.0
                if go_count - count < 2:
                    move_cmd.linear.x = 0.05
                    move_cmd.angular.z = 0
                self.pub.publish(move_cmd)
                count += 1
                if count >= go_count:
                    break
                self.rate.sleep()
        # 当循环结束时，手动停止机器人运动
        move_cmd.linear.x = 0
        move_cmd.angular.z = 0
        self.pub.publish(move_cmd)

    # 转弯
    def going2(self, dist):
       # 单位为cm
        # if self.direction:
        # go_count = int(dist + grabParams.move_power_high_left + 0.5)
        # else:
        # go_count = int(dist + grabParams.move_power_high_right + 0.5)
        go_count = int(dist * grabParams.dist_bias)
        count = 0
        move_cmd = Twist()
        time.sleep(0.5)
        if go_count >= 0:
            while True:
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = 0.1
                if go_count - count < 2:
                    move_cmd.linear.x = 0.05
                    move_cmd.angular.z = 0
                self.pub.publish(move_cmd)
                count += 1
                if count >= go_count:
                    break
                self.rate.sleep()
        else:
            go_count = -1 * go_count
            while True:
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = -0.1
                if go_count - count < 2:
                    move_cmd.linear.x = 0.05
                    move_cmd.angular.z = 0
                self.pub.publish(move_cmd)
                count += 1
                if count >= go_count:
                    break
                self.rate.sleep()
        # 当循环结束时，手动停止机器人运动
        move_cmd.linear.x = 0
        move_cmd.angular.z = 0
        self.pub.publish(move_cmd)

    # 前进后退
    def going_faster(self, dist):
       # 单位为cm
        # if self.direction:
        # go_count = int(dist + grabParams.move_power_high_left + 0.5)
        # else:
        # go_count = int(dist + grabParams.move_power_high_right + 0.5)
        go_count = int(dist * grabParams.dist_bias)
        count = 0
        move_cmd = Twist()
        time.sleep(0.5)
        if go_count >= 0:
            while True:
                move_cmd.linear.x = 0.4
                move_cmd.angular.z = 0.0
                if go_count - count < 2:
                    move_cmd.linear.x = 0.05
                    move_cmd.angular.z = 0
                self.pub.publish(move_cmd)
                count += 1
                if count >= go_count:
                    break
                self.rate.sleep()
        else:
            go_count = -1 * go_count
            while True:
                move_cmd.linear.x = -0.3
                move_cmd.angular.z = 0.0
                if go_count - count < 2:
                    move_cmd.linear.x = 0.05
                    move_cmd.angular.z = 0
                self.pub.publish(move_cmd)
                count += 1
                if count >= go_count:
                    break
                self.rate.sleep()
        # 当循环结束时，手动停止机器人运动
        move_cmd.linear.x = 0
        move_cmd.angular.z = 0
        self.pub.publish(move_cmd)

    # 转弯
    def going2_faster(self, dist):
           # 单位为cm
        go_count = int(dist * grabParams.dist_bias)
        count = 0
        move_cmd = Twist()
        time.sleep(0.5)
        if go_count >= 0:
            while True:
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = 0.2
                if go_count - count < 2:
                    move_cmd.linear.x = 0.05
                    move_cmd.angular.z = 0
                self.pub.publish(move_cmd)
                count += 1
                if count >= go_count:
                    break
                self.rate.sleep()
        else:
            go_count = -1 * go_count
            while True:
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = -0.2
                if go_count - count < 2:
                    move_cmd.linear.x = 0.05
                    move_cmd.angular.z = 0
                self.pub.publish(move_cmd)
                count += 1
                if count >= go_count:
                    break
                self.rate.sleep()
        # 当循环结束时，手动停止机器人运动
        move_cmd.linear.x = 0
        move_cmd.angular.z = 0
        self.pub.publish(move_cmd)

    def back(self):
        count = 6
        move_cmd = Twist()
        move_cmd.linear.x = -0.3
        if grabParams.put_down_direction == "right":
            move_cmd.angular.z = -0.3
        else:
            move_cmd.angular.z = 0.3
        time.sleep(0.5)
        while(count):
            self.pub.publish(move_cmd)
            count-=1
            self.rate.sleep()

    # 需要修改为新的放置位置
    def put_down(self):
        self.mc.send_coords([15,-192,300,-125,60,152], 70, 0)
        basic.grap(False)

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(500) 

    # 机械臂准备姿态
    def init_mycobot(self): 
        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
        basic.grap(False)      
        time.sleep(1)
        coords_height = [-50.7, -130.1, 285.6, -85.45, 45.12, -173.88]         
        basic.move_to_target_coords(coords_height,30)

    def run_2(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.init_mycobot()
        
def main():
    # os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right.py --debug") # 回到初始状态
    # read camera
    detect = Detect_marker()
    detect.run_2()
    time.sleep(2)
    # detect.run()
    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5) 
    count_grab = 0
    # detect.going(detect.c_x - result[0]) # 尽量对准第一个

    while cv2.waitKey(1) < 0 and not done:
        # 更换逻辑，慢慢往前找寻目标
        print("zhixing")

        # 开始夹取
        frame = cap.read()
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) # 顺时针转九十度
        frame = detect.transform_frame(frame)
        detect_result = detect.obj_detect(frame)
        if detect_result is None:
            detect.going(3) # 往前走一段继续识别
            continue
        else:   
            x, y = detect_result
            print(x, y)
            real_x, real_y = detect.get_position(x, y)
            # print("move")
            detect.mc.set_color(255,0,0) #抓取开始，亮红灯

            detect.move_high(real_x + grabParams.x_bias, real_y + grabParams.y_bias, 0)
            # 前往充能站
            going_chong()
            # 放置积木块
            detect.move_back()
            
            # 返回仓库货架
            gong_cang()
            
            count_grab += 1
            
            if count_grab == 3:
                break
            # detect.going(20) # 往前到下一个抓取位置

        # os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right.py --debug") # 回到高点防止鬼畜
        time.sleep(0.7)
    cap.close()

    #     if i is not 4:
    #         detect.going(10) # 往前到下一个抓取位置
    #     if i == 4:
    #         back_pose_ready()
    #         os.system("python /home/robuster/RoboCom/navigation/BackNavigation.py")
    back_pose_ready()
    os.system("python /home/robuster/RoboCom/navigation/BackNavigation.py")

# 返回仓库货架
def gong_cang():
    detect = Detect_marker()
    detect.going(-10)
    # 右转180°
    detect.going2(180)
    os.system("python /home/robuster/RoboCom/navigation/BackcangNavigation.py") #前往仓库货架


def going_chong():
    detect = Detect_marker()
    # 先右转90°cangchong
    detect.going2(160)
    detect.going(30)
    os.system("python /home/robuster/RoboCom/navigation/BackchongNavigation.py") #前往充能站

def going_colser():
    detect = Detect_marker()
    detect.going2(-30)
    detect.going(8)
    detect.going2(30)
    detect.going(-8)

def going_farer():
    detect = Detect_marker()
    detect.going2(30)
    detect.going(8)
    detect.going2(-30)
    detect.going(-8)

def going_test():
    detect = Detect_marker()
    detect.going2(-30)
    detect.going(5)
    detect.going2(30)
    detect.going(-5)

def back_pose_ready():
    detect = Detect_marker()
    if grabParams.side == 'right':
        detect.going2_faster(-30)
        detect.going_faster(-10)
        detect.going2_faster(50)
    else:
        detect.going2_faster(-30)
        detect.going_faster(-13)
        detect.going2_faster(-200)
if __name__ == "__main__":
    main()
    back_pose_ready()
    going_test()
    