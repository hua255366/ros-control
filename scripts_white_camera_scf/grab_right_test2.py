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
import subprocess
import actionlib
import yaml
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from grabParams_zyt3 import grabParams_zyt3
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument("--debug", type=bool, default="False")
args = parser.parse_args()

done = grabParams_zyt3.done

class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()
        rospy.init_node('grab_right', anonymous=True)
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.rate = rospy.Rate(10) # 10hz
        self.mc = MyCobot(grabParams_zyt3.usb_dev, grabParams_zyt3.baudrate)
        self.mc.power_on() 
        self.yolo = yolo()
        self.c_x, self.c_y = grabParams_zyt3.IMG_SIZE/2, grabParams_zyt3.IMG_SIZE/2
        self.ratio = grabParams_zyt3.ratio
        self.lv = 940
        self.hr = 2.1
        self.detect_count = 0
        self.clazz = []
        self.direction = 0 
        self.aruco_count = 0

    # Grasping motion
    # 单点进程 竖直方向初次夹取
    def move_high(self, x, y, dist):
        global done
        # print(x)
        # if math.fabs(x) > 5:
        #     x = 5
        # global done
        time.sleep(0.2)
        # 抓取
        # 防止离太近 先收回来
        coords = grabParams_zyt3.coords_right_high
        
        coords_target = [coords[0]-2, coords[1]+20, coords[2]+60, coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(coords_target, grabParams_zyt3.GRAB_MOVE_SPEED)
        time.sleep(1)
        # 移动到目标位置
        coords_target1 = [coords[0]-2, coords[1]-60, coords[2]+50, coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(coords_target1, grabParams_zyt3.GRAB_MOVE_SPEED)
        basic.grap(True)

        coords_target3 = [coords[0], coords[1]+40, coords[2]+60, coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(coords_target3, grabParams_zyt3.GRAB_MOVE_SPEED)
        time.sleep(1)
        basic.grap(False)
        # 放回4
        time.sleep(1)
        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles,30)
        time.sleep(3)
        coords_target4 = [coords[0], coords[1]+40, coords[2]+40, coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(coords_target4, grabParams_zyt3.GRAB_MOVE_SPEED)


        # self.mc.send_coords(grabParams_zyt3.coords_pitchdown1, 30, 0) # 先抬高
        # time.sleep(0.5)
        # self.mc.send_coords(grabParams_zyt3.coords_pitchdown2, 30, 0)
        # time.sleep(1)
        # basic.grap(False) 松抓
        done = False
        time.sleep(1)

        self.mc.set_color(0,255,0) #抓取结束，亮绿灯

    # 充能站放置 
    def move_back(self):
        coords_back = grabParams_zyt3.coords_back
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
        time.sleep(0.5)
        coords_height = [-50.7, -130.1, 285.6, -85.45, 45.12, -173.88]         
        basic.move_to_target_coords(coords_height,30)


    def get_position(self, x, y):
        # print "self.ratio: ", self.ratio
        # return (-(x - self.c_x)*self.ratio), (-(y - self.c_y)*self.ratio)
        wx = wy = 0
        if grabParams_zyt3.grab_direct == "front":
            wx = (self.c_y - y) * self.ratio
            wy = (self.c_x - x) * self.ratio
        elif grabParams_zyt3.grab_direct == "right":
            wx = (self.c_x - x) * self.ratio
            wy = (y - self.c_y) * self.ratio
        return wx, wy
            
    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams_zyt3.IMG_SIZE, grabParams_zyt3.IMG_SIZE))
        return frame

    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams_zyt3.IMG_SIZE, grabParams_zyt3.IMG_SIZE))

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
            return None
        else:
            return None
        

    # 前进后退
    def going(self, dist):
       # 单位为cm
        # if self.direction:
        # go_count = int(dist + grabParams.move_power_high_left + 0.5)
        # else:
        # go_count = int(dist + grabParams.move_power_high_right + 0.5)
        go_count = int(dist * grabParams_zyt3.dist_bias)
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
        go_count = int(dist * grabParams_zyt3.dist_bias)
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
        go_count = int(dist * grabParams_zyt3.dist_bias)
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
        go_count = int(dist * grabParams_zyt3.dist_bias)
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


    # 需要修改为新的放置位置
    def put_down(self):
        self.mc.send_coords([15,-192,300,-125,60,152], 70, 0)
        basic.grap(False)

    def show_image(self, img):
        if grabParams_zyt3.debug and args.debug:
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
    os.system("python /home/robuster/RoboCom/navigation/BackcangNavigation.py --debug")
    time.sleep(20)
    detect = Detect_marker()
    #rospy.init_node('navigation')
    detect.run_2()
    time.sleep(2)
    # detect.run()
    cap = FastVideoCapture(grabParams_zyt3.cap_num)
    time.sleep(0.5)
    count = 1
    num = sum_x = sum_y = 0   
    count_grab = 0
    i=0
    # detect.going(detect.c_x - result[0]) # 尽量对准第一个

    while cv2.waitKey(1) < 0 and not done:
        # 更换逻辑，慢慢往前找寻目标
        print("zhixing")

        # 开始夹取
        frame = cap.read()
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) # 顺时针转九十度
        # frame = detect.transform_frame(frame)
        detect_result = detect.obj_detect(frame)
        if detect_result is None:
            if i == 8:
              #detect.going2(-160)
              #detect.going(-30)
              coords_height = [-50.7, -110.1, 285.6, -85.45, 45.12, -173.88]         
              basic.move_to_target_coords(coords_height,30)
              os.system("python /home/robuster/RoboCom/navigation/BackNavigation.py")
              break
            detect.going(5) # 往前走一段继续识别
            i+=1
            
            continue
        else:
            i=0
            x, y  = detect_result
            real_x, real_y = detect.get_position(x, y)
            print(x, y)
            # if num < count:
            #     sum_x += real_x
            #     sum_y += real_y
            #     num += 1
            # elif num ==count:
            #     # coords_now = basic.get_coords()
            #     # if len(coords_now) == 6:
            #     #     coords = coords_now
            #     # rotation_angle = self.get_rotation(corners)                                                         
            #     print(sum_x/count, sum_y/count)
            #     detect.mc.set_color(255,0,0) #抓取开始，亮红灯
            #     detect.move_high(sum_x/count + grabParams_zyt3.x_bias, sum_y/count + grabParams_zyt3.y_bias, 0)
            #     num = sum_x = sum_y = 0  
            detect.mc.set_color(255,0,0) #抓取开始，亮红灯
            detect.move_high(sum_x/count + grabParams_zyt3.x_bias, sum_y/count + grabParams_zyt3.y_bias, 0)
            
            # print("move")
            
            print("zhuaqu")
            
            # 前往充能站
            # going_chong()
            # 放置积木块
            # time.sleep(40)
            # detect.move_back()
            
            # 返回仓库货架
            # gong_cang()
            
            count_grab += 1
            
            if count_grab == 3:
                break
            # detect.going(20) # 往前到下一个抓取位置

        # os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right.py --debug") # 回到高点防止鬼畜
        time.sleep(2)
    cap.close()
    

    #     if i is not 4:
    #         detect.going(10) # 往前到下一个抓取位置
    #     if i == 4:
    #         back_pose_ready()
    #         os.system("python /home/robuster/RoboCom/navigation/BackNavigation.py")
    #back_pose_ready()
    os.system("python /home/robuster/RoboCom/navigation/BackNavigation.py")

# 返回仓库货架
def gong_cang():
    global done
    detect = Detect_marker()
    detect.going(-10)
    # 右转180°
    detect.going2(180)
    # os.system("python /home/robuster/RoboCom/navigation/BackcangNavigation.py") #前往仓库货架
    send_cang()
    done = False

# 回到仓库
def send_cang1(goal):
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
	client.send_goal(goal)  #, done_cb=home_reached_callback
# def send_cang1(goal):
#     client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
#     client.wait_for_server()
#     goal.target_pose.header.frame_id = 'map'
#     goal.target_pose.header.stamp = rospy.Time.now()
#     client.send_goal(goal)

#     # 等待目标到达
#     finished_within_time = client.wait_for_result(rospy.Duration(60))  # 设置一个超时时间（例如60秒）

#     if not finished_within_time:
#         client.cancel_goal()
#         rospy.loginfo("Timed out achieving goal")
#     else:
#         state = client.get_state()
#         if state == actionlib.GoalStatus.SUCCEEDED:
#             rospy.loginfo("Goal succeeded!")
#         else:
#             rospy.loginfo("Goal failed with state: %s" % state)
#             return 1

    


def send_cang():
    #rospy.init_node('navigation')
    with open('/home/robuster/RoboCom/navigation/pose_ck.yaml', 'r') as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

    pose_x = yaml_data['pose']['position']['x']
    pose_y = yaml_data['pose']['position']['y']
    pose_z = yaml_data['pose']['position']['z']

    orien_x = yaml_data['pose']['orientation']['x']
    orien_y = yaml_data['pose']['orientation']['y']
    orien_z = yaml_data['pose']['orientation']['z']
    orien_w = yaml_data['pose']['orientation']['w']

    home = MoveBaseGoal()
    home.target_pose.pose = Pose(Point(pose_x, pose_y, pose_z),
                                 Quaternion(orien_x, orien_y, orien_z, orien_w))

def going_chong():
    detect = Detect_marker()
    # 先右转90°cangchong
    detect.going2(160)
    detect.going(30)
    
    send_chong()

# 回到充能站
def send_chong1(goal):
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    client.send_goal(goal)  #, done_cb=home_reached_callback

    

def send_chong():
    #rospy.init_node('navigation')

    with open('/home/robuster/RoboCom/navigation/pose_cnz.yaml', 'r') as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

    pose_x = yaml_data['pose']['position']['x']
    pose_y = yaml_data['pose']['position']['y']
    pose_z = yaml_data['pose']['position']['z']

    orien_x = yaml_data['pose']['orientation']['x']
    orien_y = yaml_data['pose']['orientation']['y']
    orien_z = yaml_data['pose']['orientation']['z']
    orien_w = yaml_data['pose']['orientation']['w']

    home = MoveBaseGoal()
    home.target_pose.pose = Pose(Point(pose_x, pose_y, pose_z),
                                 Quaternion(orien_x, orien_y, orien_z, orien_w))
    send_chong1(home)

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
    if grabParams_zyt3.side == 'right':
        detect.going2_faster(-30)
        detect.going_faster(-10)
        detect.going2_faster(50)
    else:
        detect.going2_faster(-30)
        detect.going_faster(-13)
        detect.going2_faster(-200)
if __name__ == "__main__":
    # rospy.init_node('navigation')
    #detecte = Detect_marker()
   # detecte.move_high(0,0,0)
    main()
    # back_pose_ready()
    # going_test()
    