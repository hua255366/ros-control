#encoding: UTF-8
#!/usr/bin/env python2
import cv2
import os
import numpy as np
import time
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

coords = grabParams.coords_ready
done = grabParams.done

MAX_GRABS = 4

CLASSES = ("apple", "clock", "banana", "cat", "bird")  # [0,1,2,3,4]

# ============== 分拣用：类别 -> 放置点 ==============
# 识别到什么类别，抓到真实物体后就放到对应的点。
# 这两个点需要你自己标定：把机械臂手动摇到“右边”/“左边”放置位置，
# 读 get_coords() 填进来。
PLACE_POINT_RIGHT = [217.6, -151.3, 201.7, -175.64, -6.81, -45.7]   # 占位值，需标定：cat 放这里
PLACE_POINT_LEFT  = [236.3, 118.8, 182.0, -179.62, -0.35, -36.91]  # 占位值，需标定：bird 放这里

CLASS_TO_PLACE_POINT = {
    "cat":  PLACE_POINT_RIGHT,
    "bird": PLACE_POINT_LEFT,
}

# 抓到物体后先抬高这么多(mm)再平移，避免拖着物体刮到桌面/障碍物
# 这是脚本本地常量，不依赖 GrabParams.py，按你实际情况调整这个数值即可
LIFT_OFFSET = 40


class Detect_marker(object):

    def __init__(self):
        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()

        self.yolo = yolo()

        # 模型只加载一次，不要放在 obj_detect 里面每帧重新读
        self.net = cv2.dnn.readNetFromONNX(
            "/home/robuster/beetle_ai/scripts/beetle_obj.onnx"
        )

        self.c_x, self.c_y = grabParams.IMG_SIZE / 2, grabParams.IMG_SIZE / 2
        self.ratio = grabParams.ratio

    # 把像素坐标换算成相对机械臂当前位置的实际偏移量(mm)，跟原脚本一致
    def get_position(self, x, y):
        wx = wy = 0
        if grabParams.grab_direct == "front":
            wx = (self.c_y - y) * self.ratio
            wy = (self.c_x - x + 100) * self.ratio
        elif grabParams.grab_direct == "right":
            wx = (self.c_x - x) * self.ratio
            wy = (y - self.c_y) * self.ratio
        return wx, wy

    # 核心：先抓真实位置的物体，再根据类别放到对应的点
    # x, y: 物体相对当前坐标的实际偏移量(mm)，由 get_position() 算出
    def pick_and_sort(self, x, y, class_name):
        global coords, done

        place_target = CLASS_TO_PLACE_POINT.get(class_name)
        if place_target is None:
            print("识别到 %s，不在分拣目标类别里，跳过" % class_name)
            return False

        height_bias = grabParams.height_bias
        side = "右" if class_name == "cat" else "左"

        # 1. 移动到实际识别出的物体位置，下降到抓取高度
        pick_coords = [coords[0] + int(x), coords[1] + int(y), height_bias,
                       coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(pick_coords, 30)

        # 2. 闭合夹爪，抓住物体
        basic.grap(True)
        time.sleep(1)

        # 3. 先抬高一段再平移，避免拖着物体刮到桌面/货架边缘
        lift_coords = pick_coords[:]
        lift_coords[2] = height_bias + LIFT_OFFSET
        basic.move_to_target_coords(lift_coords, 30)

        # 4. 平移到分拣目标点上方（cat->右边点，bird->左边点），仍保持抬高
        place_coords = place_target[:]
        place_coords[2] = place_target[2] + LIFT_OFFSET
        self.mc.send_coords(place_coords, 30,0)

        # 5. 下降到放置高度
        place_coords[2] = place_target[2]
        self.mc.send_coords(place_coords, 30 ,0)

        # 6. 松开夹爪，放下物体
        time.sleep(2)
        basic.grap(False)
        time.sleep(1)

        # 7. 抬高离开放置点
        place_coords[2] = place_target[2] + LIFT_OFFSET
        self.mc.send_coords(place_coords, 30,0)

        basic.move_to_target_coords(grabParams.coords_ready, 30)

        done = True
        print("识别到 %s，已从实际位置抓取，分拣到%s侧" % (class_name, side))
        self.mc.set_color(0, 255, 0)  # green, arm is free

        return True

    # init mycobot
    def init_mycobot(self):
        basic.grap(False)
        time.sleep(0.5)
        basic.move_to_target_coords(coords, 30)

    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(
            frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))
        return frame

    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))
        return frame

    # detect object, 返回 (x, y, class_name)
    def obj_detect(self, img):
        x = y = 0
        class_name = None

        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        t1 = time.time()
        blob = cv2.dnn.blobFromImage(
            img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        self.net.setInput(blob)

        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())[0]

        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)
        t2 = time.time()

        if boxes is not None:
            boxes = boxes * 5
            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])
            left, top, right, bottom = boxes[0]
            x = int((left + right) / 2)
            y = int((top + bottom) / 2)
            class_name = CLASSES[classes[0]]
            print("识别到: %s, 置信度: %.2f" % (class_name, scores[0]))

            if  class_name == "banana":
                class_name = "cat"
        self.show_image(img_ori)
        print("time: " + str(t2 - t1) + "s")



        if x + y > 0:
            return x, y, class_name
        else:
            return None

    def run(self):
        self.mc.set_color(0, 0, 255)  # blue, arm is busy
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

    grabbed_count = 0

    try:
        while cv2.waitKey(1) < 0:
            # 设置了次数上限的话，抓够了就停
            if MAX_GRABS is not None and grabbed_count >= MAX_GRABS:
                print("已完成 %d 次分拣，结束" % grabbed_count)
                break

            frame = cap.read()
            #frame = cv2.flip(frame, 0)
            #frame = cv2.flip(frame, 1)

            detect_result = detect.obj_detect(frame)
            if detect_result is None:
                continue

            x, y, class_name = detect_result

            # 不是 cat/bird 这两个分拣类别，跳过这一帧，继续等
            if class_name not in CLASS_TO_PLACE_POINT:
                print("识别到 %s，非分拣目标类别，继续等待" % class_name)
                continue

            # 用像素坐标换算出物体相对机械臂当前位置的真实偏移量(mm)
            real_x, real_y = detect.get_position(x, y)
            coords_now = basic.get_coords()
            if len(coords_now) == 6:
                coords = coords_now

            success = detect.pick_and_sort(
                real_x + grabParams.x_bias, real_y + grabParams.y_bias, class_name)
            if success:
                grabbed_count += 1
                print("已完成 %d 次分拣" % grabbed_count)
    finally:
        # 不管是按键退出、抓够次数退出、还是异常退出，最后都要关相机
        cap.close()


