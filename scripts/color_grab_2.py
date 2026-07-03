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


y_bias = grabParams.y_bias
x_bias = grabParams.x_bias

IMG_SIZE = grabParams.IMG_SIZE

cap_num = grabParams.cap_num

# show image and waitkey
debug = grabParams.debug

coords = grabParams.coords_ready
done = grabParams.done


class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()

        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()

        self.yolo = yolo()

        # choose place to set cube
        self.color = 0
        # parameters to calculate camera clipping parameters
        self.x1 = self.x2 = self.y1 = self.y2 = 0
        # set color HSV
        self.HSV = {
            "yellow": [np.array([22, 93, 0]), np.array([45, 255, 255])],
            "red": [np.array([170, 120, 120]), np.array([180, 255, 255])],
            "green": [np.array([35, 43, 35]), np.array([90, 255, 255])],
            "blue": [np.array([90, 43, 46]), np.array([110, 255, 255])],
            "purple": [np.array([123, 43, 46]), np.array([138, 255, 255])],
        }
        # use to calculate coord between cube and mycobot
        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0
        # The coordinates of the cube relative to the mycobot
        self.c_x, self.c_y = IMG_SIZE / 2, IMG_SIZE / 2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio

    # 从 source layer 抓取，放到 target layer
    # x, y: 抓取点相对 coords_ready 的偏移量(mm)，由摄像头检测换算得到
    # pick_height: 本次抓取使用的 z 高度（来源层标定出的高度）
    def pick_and_place(self, x, y, pick_height):
        global done

        # 1. 移动到方块上方，下降到抓取高度
        pick_coords = [coords[0] + int(x), coords[1] + int(y), pick_height,
                       coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(pick_coords, grabParams.GRAB_MOVE_SPEED)

        # 2. 闭合夹爪，夹住方块
        basic.grap(True)
        time.sleep(1)

        # 3. 先抬高一段距离再平移，避免拖着方块刮到货架边缘
        lift_coords = pick_coords[:]
        lift_coords[2] = pick_height + grabParams.LIFT_OFFSET
        basic.move_to_target_coords(lift_coords, grabParams.GRAB_MOVE_SPEED)

        # 4. 平移到下层放置点上方（仍保持抬高状态）
        place_height = grabParams.SHELF_LAYERS[grabParams.TARGET_LAYER]["height_bias"]
        place_coords = grabParams.PLACE_COORDS[:]
        place_coords[2] = place_height + grabParams.LIFT_OFFSET
        basic.move_to_target_coords(place_coords, grabParams.GRAB_MOVE_SPEED)

        # 5. 下降到放置高度
        place_coords[2] = place_height
        basic.move_to_target_coords(place_coords, grabParams.GRAB_MOVE_SPEED)

        # 6. 松开夹爪，放下方块
        basic.grap(False)
        time.sleep(1)

        # 7. 抬高离开放置点，再回到零位
        place_coords[2] = place_height + grabParams.LIFT_OFFSET
        basic.move_to_target_coords(place_coords, grabParams.GRAB_MOVE_SPEED)

        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles, 30)
        time.sleep(3)

        done = True
        print("Done")
        self.mc.set_color(0, 255, 0)  # green, arm is free

    # init mycobot
    def init_mycobot(self):
        angles = [0, 0, 0, 0, 0, 0]
        self.mc.send_angles(angles, 30)
        basic.grap(False)
        time.sleep(1)
        basic.move_to_target_coords(coords, grabParams.GRAB_MOVE_SPEED)

    def get_position(self, x, y):
        wx = wy = 0
        if grabParams.grab_direct == "front":
            wx = (self.c_y - y) * self.ratio
            wy = (self.c_x - x) * self.ratio
        elif grabParams.grab_direct == "right":
            wx = (self.c_x - x) * self.ratio
            wy = (y - self.c_y) * self.ratio
        return wx, wy

    # 根据方块在画面中的像素 y 坐标，判断它属于哪一层货架。
    # 返回 (层名, 该层标定好的高度)；没匹配到时层名返回 None，
    # 高度回退到默认值，并打印提示，方便你发现标定区间没设对。
    def get_layer_height(self, y_pixel):
        for name, layer in grabParams.SHELF_LAYERS.items():
            y_min, y_max = layer["y_pixel_range"]
            if y_min <= y_pixel < y_max:
                print("检测到目标位于 %s 层, 高度 height_bias=%s"
                      % (name, layer["height_bias"]))
                return name, layer["height_bias"]
        print("未匹配到任何货架层(y_pixel=%s)，使用默认高度 height_bias=%s"
              % (y_pixel, grabParams.height_bias))
        return None, grabParams.height_bias

    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (IMG_SIZE, IMG_SIZE))

        return frame

    # detect cube color
    def color_detect(self, img):
        # set the arrangement of color'HSV
        x = y = 0
        for mycolor, item in self.HSV.items():
            redLower = np.array(item[0])
            redUpper = np.array(item[1])
            # transfrom the img to model of gray
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # wipe off all color expect color in range
            mask = cv2.inRange(hsv, item[0], item[1])
            # a etching operation on a picture to remove edge roughness
            erosion = cv2.erode(mask, np.ones((1, 1), np.uint8), iterations=2)
            # the image for expansion operation, its role is to deepen the color depth in the picture
            dilation = cv2.dilate(erosion, np.ones(
                (1, 1), np.uint8), iterations=2)
            # adds pixels to the image
            target = cv2.bitwise_and(img, img, mask=dilation)
            # the filtered image is transformed into a binary image and placed in binary
            ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
            # get the contour coordinates of the image, where contours is the coordinate value, here only the contour is detected
            contours, hierarchy = cv2.findContours(
                dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) > 0:
                # do something about misidentification
                boxes = [
                    box
                    for box in [cv2.boundingRect(c) for c in contours]
                    if 70 < min(box[2], box[3]) and max(box[2], box[3]) < 120
                ]
                print(boxes)
                if boxes:
                    for box in boxes:
                        x, y, w, h = box
                    # find the largest object that fits the requirements
                    c = max(contours, key=cv2.contourArea)
                    # get the lower left and upper right points of the positioning object
                    x, y, w, h = cv2.boundingRect(c)
                    print(x, y, w, h)
                    # locate the target by drawing rectangle
                    cv2.rectangle(img, (x, y), (x + w, y + h), (130, 130, 0), 2)
                    # calculate the rectangle center
                    x, y = (x * 2 + w) / 2, (y * 2 + h) / 2
                    # calculate the real coordinates of mycobot relative to the target
                    if mycolor == "yellow":
                        self.color = 1
                    elif mycolor == "red":
                        self.color = 0
                    else:
                        self.color = 1

        if abs(x) + abs(y) > 0:
            return x, y
        else:
            return None

    def run(self):
        self.mc.set_color(0, 0, 255)  # blue, arm is busy
        self.init_mycobot()

    def show_image(self, img):
        print(args.debug)
        if debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(50)


if __name__ == "__main__":
    detect = Detect_marker()
    detect.run()

    cap = FastVideoCapture(cap_num)
    time.sleep(0.5)

    while cv2.waitKey(1) < 0 and not done:
        frame = cap.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)

        # deal img
        frame = detect.transform_frame(frame)

        # get detect result
        detect_result = detect.color_detect(frame)
        detect.show_image(frame)
        if detect_result is None:
            continue
        else:
            x, y = detect_result

            # 根据方块在画面中的像素 y 坐标，判断它属于哪一层
            layer_name, grab_height = detect.get_layer_height(y)

            # 只抓取来源层(upper)的方块；如果检测到的是目标层(lower)或
            # 未匹配到任何层，跳过这次检测，继续等下一帧
            if layer_name != grabParams.SOURCE_LAYER:
                continue

            # calculate real coord between cube and mycobot, unit mm
            real_x, real_y = detect.get_position(x, y)
            coords_now = basic.get_coords()
            if len(coords_now) == 6:
                coords = coords_now

            detect.pick_and_place(real_x + x_bias, real_y + y_bias, grab_height)
            cap.close()
