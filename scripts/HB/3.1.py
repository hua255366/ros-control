# -*- coding: utf-8 -*-
'''
项目信息注释：
project: task 3 yolo recognition  # 项目名称：任务3-YOLO目标识别
version: 3-1                     # 代码版本：3.1版本
author: jiayu                    # 作者：jiayu
date: 2024.6.30                  # 日期：2024年6月30日
'''

# 编码格式声明：使用UTF-8编码（支持中文等特殊字符）
# !/usr/bin/env python2  # 指定脚本使用Python2解释器执行（注意：Python2已停止维护，建议后续迁移至Python3）

# 导入依赖库
import cv2                  # OpenCV库：用于图像处理、视频捕获、图像显示
import numpy as np          # NumPy库：用于数值计算、数组操作（如矩阵运算）
import time                 # 时间库：用于延时、计时（如机械臂动作等待、识别耗时统计）
import rospy                # ROS（机器人操作系统）Python库：用于节点初始化、话题发布/订阅
from pymycobot.mycobot import MyCobot  #  mycobot机械臂控制库：用于机械臂角度控制、夹爪控制、灯光控制
from opencv_yolo import yolo # 自定义YOLO工具库：封装了YOLO图像预处理、后处理（如目标框提取、绘图）
import math                 # 数学库：用于潜在的坐标计算、角度转换（本代码暂未直接使用）
from GrabParams import grabParams  # 自定义抓取参数库：存储机械臂、相机、抓取相关的配置参数（如串口、像素比例）
import basic                # 自定义基础工具库：封装了机械臂基础动作（如抓取/释放、坐标移动，本代码暂未深入使用）
import argparse             # 命令行参数解析库：用于接收外部传入的调试模式参数
from geometry_msgs.msg import Twist  # ROS消息类型：用于发布机器人运动指令（线速度、角速度）
from actionlib.action_client import GoalManager  # ROS动作客户端工具：用于管理运动目标（本代码暂未直接使用）
import actionlib            # ROS动作库：用于实现基于动作的目标导航（如move_base导航）
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal  # ROS导航消息类型：用于发送move_base导航目标
import re                   # 正则表达式库：用于解析导航目标配置文件中的坐标数据


# -------------------------- 命令行参数解析配置 --------------------------
# 创建参数解析器，描述脚本功能
parser = argparse.ArgumentParser(description='manual to this script')
# 添加--debug参数：布尔类型，默认True（调试模式），用于控制是否输出调试信息（本代码暂未深入使用该参数）
parser.add_argument("--debug", type=bool, default="True")
# 解析传入的命令行参数
args = parser.parse_args()


# -------------------------- ROS初始化与话题发布配置 --------------------------
# 初始化ROS节点：节点名"movement"，anonymous=True表示自动添加随机后缀避免节点名重复（原代码注释，若启用需取消注释）
# rospy.init_node('movement', anonymous=True)

# 创建ROS话题发布者：发布话题为"cmd_vel"（用于控制机器人底盘运动），消息类型为Twist，队列大小1（缓存1条消息）
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

# 设置ROS发布频率：20Hz（原代码注释，控制话题发布的时间间隔，若启用需取消注释）
# rate = rospy.Rate(20)  # 20hz

# 创建Twist类型消息实例：用于存储底盘运动指令（线速度、角速度）
move_cmd = Twist()


# -------------------------- 全局参数初始化（从配置文件导入+自定义） --------------------------
# 从GrabParams配置文件导入参数：机械臂抓取高度偏差（用于调整抓取Z轴坐标）
height_bias = grabParams.height_bias
# 从GrabParams配置文件导入参数：机械臂就绪位置坐标（抓取前的准备坐标）
coords = grabParams.coords_ready
# 从GrabParams配置文件导入参数：任务完成标志（用于判断抓取/导航是否完成）
done = grabParams.done

# YOLO目标识别的类别列表：对应索引0-4分别为苹果、时钟、香蕉、猫、鸟（注意"cat "和"bird "后有空格，需与模型输出匹配）
CLASSES = ("apple", "clock", "banana", "cat ", "bird ")  # [0,1,2,3,4]

# 初始化mycobot机械臂：传入串口设备（从配置文件获取）和波特率（从配置文件获取），建立与机械臂的通信
mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)

# 初始化ROS节点：节点名"send_goals_python"，anonymous=True避免节点名重复（用于导航目标发送）
rospy.init_node('send_goals_python', anonymous=True)


# -------------------------- 全局变量声明（用于导航与识别状态跟踪） --------------------------
global outcome1  # 存储YOLO识别到的目标类别索引（0-4，对应CLASSES）
global init_num  # 机械臂放置目标的次数计数器（0-3，控制放置位置逻辑）
global left_num  # 左侧放置目标的次数计数器（用于判断左侧放置位置是否已满）
global num1      # 首次识别到的目标类别索引（用于后续同类目标的放置位置判断）

# 全局变量初始值
outcome1 = 7     # 初始化为7（无意义值，用于标记未识别到目标）
init_num = 0     # 初始放置次数为0
left_num = 0     # 初始左侧放置次数为0
num1 = 7         # 初始首次识别类别为7（无意义值）


# -------------------------- 导航目标发送函数（基于move_base） --------------------------
def send_goal(goal_number, goal):
    """
    向move_base导航节点发送导航目标，实现机器人自主导航到指定位置
    参数：
        goal_number: 目标编号（用于日志打印，区分不同目标）
        goal: MoveBaseGoal类型实例，存储导航目标的位置（x,y）和姿态（z,w四元数）
    """
    # 创建action客户端：连接"move_base"动作服务器，消息类型为MoveBaseAction
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    # 等待action服务器启动（阻塞，直到连接成功）
    client.wait_for_server()

    # 设置导航目标的坐标系："map"表示基于全局地图坐标系（确保与导航系统一致）
    goal.target_pose.header.frame_id = "map"
    # 设置目标的时间戳：使用当前ROS时间，确保目标有效性
    goal.target_pose.header.stamp = rospy.Time.now()
    # 发送导航目标到move_base服务器
    client.send_goal(goal)
    # 打印日志：提示已发送第N个目标
    str_log = "Send NO. %s Goal !!!" % str(goal_number)
    rospy.loginfo(str_log)

    # 等待导航结果：超时时间60秒（60秒内未到达目标则判定为失败）
    wait = client.wait_for_result(rospy.Duration.from_sec(60.0))
    if not wait:
        # 超时未完成：打印导航失败日志
        str_log = "The NO. %s Goal Planning Failed for some reasons" % str(goal_number)
        rospy.loginfo(str_log)
    else:
        # 导航成功：打印目标达成日志
        str_log = "The NO. %s Goal achieved success !!!" % str(goal_number)
        rospy.loginfo(str_log)


# -------------------------- 导航目标解析函数（从文件读取） --------------------------
def read_goal(filename):
    """
    从文本文件中读取导航目标参数（位置x,y；姿态z,w），生成MoveBaseGoal实例
    参数：
        filename: 导航目标配置文件名（如"goal_right_center.txt"）
    返回：
        goal: MoveBaseGoal类型实例，包含解析后的导航目标
    """
    # 创建MoveBaseGoal实例（存储导航目标）
    goal = MoveBaseGoal()

    # 打开目标配置文件（只读模式）
    file_to_read = open(filename)
    index = 0  # 行索引计数器：用于区分位置行（第2行）和姿态行（第3行）
    # 逐行读取文件内容
    for line in file_to_read.readlines():
        # 去除每行首尾的空白字符（空格、换行符等）
        line = line.strip()
        index += 1  # 行索引自增

        # 第2行：存储位置信息（x,y），格式通常为"position: [x,y]"
        if index == 2:
            # 正则表达式：匹配"["和"]"之间的内容（提取x,y数值字符串）
            pattern = re.compile(r"(?<=\[).*?(?=\])")
            query = pattern.search(line)  # 搜索匹配的内容
            listFromLine = query.group().split(',')  # 按逗号分割，得到[x字符串, y字符串]
            # 将字符串转换为浮点数，赋值给目标位置的x和y
            goal.target_pose.pose.position.x = float(listFromLine[0])
            goal.target_pose.pose.position.y = float(listFromLine[1])

        # 第3行：存储姿态信息（z,w四元数），格式通常为"orientation: [x,y,z,w]"
        if index == 3:
            # 正则表达式：匹配"["和"]"之间的内容（提取x,y,z,w数值字符串）
            pattern = re.compile(r"(?<=\[).*?(?=\])")
            query = pattern.search(line)  # 搜索匹配的内容
            listFromLine = query.group().split(',')  # 按逗号分割，得到[x,y,z,w字符串]
            # 将字符串转换为浮点数，赋值给目标姿态的z和w（四元数表示旋转，x,y通常为0）
            goal.target_pose.pose.orientation.z = float(listFromLine[2])
            goal.target_pose.pose.orientation.w = float(listFromLine[3])

    # 打印解析后的目标姿态（用于调试，确认参数正确）
    print(goal.target_pose.pose)

    # 返回解析后的导航目标
    return goal


# -------------------------- 底盘运动参数配置 --------------------------
count = 20  # 底盘运动的发布频率基数（与时间秒数相乘得到总发布次数）
rate = rospy.Rate(count)  # 设置底盘运动指令的发布频率：20Hz（确保指令稳定发送）


# -------------------------- 底盘运动控制函数（前进、后退、左转、右转） --------------------------
def moveback1(time_seconds, speed):
    """
    机器人底盘后退函数
    参数：
        time_seconds: 后退持续时间（秒）
        speed: 后退线速度（m/s，注意为负值，因为前进为正方向）
    """
    print("backward...")  # 打印动作提示
    # 计算总发布次数：频率（20Hz）* 时间（秒），确保动作持续指定时间
    count = 20 * time_seconds
    # 创建Twist消息实例（存储运动指令）
    move_cmd = Twist()

    # 循环发布后退指令，直到达到总次数
    while count > 0:
        move_cmd.linear.x = speed  # 设置线速度（后退为负）
        pub.publish(move_cmd)      # 发布运动指令到"cmd_vel"话题
        rate.sleep()               # 按20Hz频率等待，确保速度稳定
        count -= 1                 # 计数器自减，直到为0停止


def moveforward1(time_seconds, speed):
    """
    机器人底盘前进函数
    参数：
        time_seconds: 前进持续时间（秒）
        speed: 前进线速度（m/s，正值）
    """
    print("forward...")  # 打印动作提示
    # 计算总发布次数：频率（20Hz）* 时间（秒）
    count = 20 * time_seconds
    # 创建Twist消息实例
    move_cmd = Twist()

    # 循环发布前进指令
    while count > 0:
        move_cmd.linear.x = speed  # 设置线速度（前进为正）
        pub.publish(move_cmd)      # 发布指令
        rate.sleep()               # 按频率等待
        count -= 1                 # 计数器自减


def rotate_to_right1(time_seconds):
    """
    机器人底盘右转函数（逆时针旋转，根据右手坐标系：z轴向下时，负角速度为右转）
    参数：
        time_seconds: 右转持续时间（秒）
    注：角速度固定为-1 rad/s，可根据需要调整
    """
    print("rotate_to_right...")  # 打印动作提示
    # 计算总发布次数
    count = 20 * time_seconds
    # 创建Twist消息实例
    move_cmd = Twist()

    # 循环发布右转指令
    while count > 0:
        move_cmd.angular.z = -1  # 设置角速度（负为右转）
        pub.publish(move_cmd)    # 发布指令
        rate.sleep()             # 按频率等待
        count -= 1               # 计数器自减


def rotate_to_left1(time_seconds, speed):
    """
    机器人底盘左转函数（顺时针旋转，正角速度为左转）
    参数：
        time_seconds: 左转持续时间（秒）
        speed: 左转角速度（rad/s，正值）
    """
    print("rotate_to_left...")  # 打印动作提示
    # 计算总发布次数
    count = 20 * time_seconds
    # 创建Twist消息实例
    move_cmd = Twist()

    # 循环发布左转指令
    while count > 0:
        move_cmd.angular.z = speed  # 设置角速度（正为左转）
        pub.publish(move_cmd)       # 发布指令
        rate.sleep()                # 按频率等待
        count -= 1                  # 计数器自减


# -------------------------- YOLO目标识别与机械臂控制类 --------------------------
class Detect_marker(object):
    """
    目标检测与机械臂控制类：封装了机械臂初始化、YOLO目标识别、坐标计算等核心功能
    """
    def __init__(self):
        """
        类初始化函数：初始化机械臂、YOLO检测器、坐标参数等
        """
        super(Detect_marker, self).__init__()  # 调用父类（object）的初始化方法

        # 初始化机械臂：重新建立与机械臂的通信（与全局mc重复，可优化为复用全局变量）
        self.mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()  # 机械臂上电（确保机械臂可运动）

        # 初始化YOLO检测器：创建yolo类实例，用于后续图像预处理和后处理
        self.yolo = yolo()

        # 相机裁剪参数：用于存储目标框的边界坐标（初始为0，后续识别时更新）
        self.x1 = self.x2 = self.y1 = self.y2 = 0

        # 目标框坐标累加器：用于多次识别结果的平均（减少误差，本代码暂未深入使用）
        self.sum_x1 = self.sum_x2 = self.sum_y2 = self.sum_y1 = 0

        # 相机图像中心坐标：基于配置文件的图像尺寸（grabParams.IMG_SIZE），默认图像为正方形
        self.c_x, self.c_y = grabParams.IMG_SIZE / 2, grabParams.IMG_SIZE / 2

        # 像素-实际距离比例：从配置文件获取（单位：实际距离mm / 像素px，用于将图像坐标转换为实际坐标）
        self.ratio = grabParams.ratio


    def init_mycobot(self):
        """
        机械臂初始化函数：将机械臂移动到初始姿态（抓取前的准备位置）
        """
        # 机械臂初始角度列表：[关节1, 关节2, 关节3, 关节4, 关节5, 关节6]（单位：度）
        angles = [-90, 0, 0, 0, 0, -45]
        # 发送角度指令：angles为目标角度，30为运动速度（0-100，数值越大越快）
        self.mc.send_angles(angles, 30)
        # 控制夹爪释放：basic库的grap函数，False表示释放（确保初始状态夹爪打开）
        basic.grap(False)
        time.sleep(3)  # 等待3秒，确保机械臂到达目标姿态（避免动作未完成就执行下一步）

        # （原代码注释）移动到就绪坐标：basic库的坐标移动函数，可根据需要启用
        # basic.move_to_target_coords(coords,grabParams.GRAB_MOVE_SPEED)


    def get_position(self, x, y):
        """
        图像坐标转实际坐标函数：将YOLO识别到的目标中心像素坐标（x,y）转换为机械臂坐标系下的实际坐标（wx, wy）
        参数：
            x: 目标中心在图像中的x像素坐标
            y: 目标中心在图像中的y像素坐标
        返回：
            wx: 机械臂坐标系下的x轴实际距离（mm）
            wy: 机械臂坐标系下的y轴实际距离（mm）
        """
        wx = wy = 0  # 初始化实际坐标

        # 根据抓取方向（从配置文件获取）选择坐标转换公式（适配不同安装角度的相机）
        if grabParams.grab_direct == "front":
            # 正面抓取：图像y轴对应机械臂x轴，图像x轴对应机械臂y轴（方向需根据实际安装调试）
            wx = (self.c_y - y) * self.ratio
            wy = (self.c_x - x) * self.ratio
        elif grabParams.grab_direct == "right":
            # 右侧抓取：图像x轴对应机械臂x轴，图像y轴对应机械臂y轴（方向需根据实际安装调试）
            wx = (self.c_x - x) * self.ratio
            wy = (y - self.c_y) * self.ratio

        return wx, wy  # 返回实际坐标


    def transform_frame(self, frame):
        """
        图像预处理函数1：将输入图像缩放为YOLO识别所需的尺寸（从配置文件获取grabParams.IMG_SIZE）
        参数：
            frame: 原始输入图像（BGR格式，OpenCV默认）
        返回：
            frame: 缩放后带黑边的图像（letterbox方式：保持宽高比，不足部分填充黑边，避免图像拉伸）
            ratio: 图像缩放比例（原图像尺寸/目标尺寸）
            (dw, dh): 填充黑边的宽度和高度（左右填充dw/2，上下填充dh/2）
        """
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))
        return frame


    def transform_frame_128(self, frame):
        """
        图像预处理函数2：将输入图像缩放为128x128尺寸（适配ONNX模型的输入要求）
        参数：
            frame: 原始输入图像
        返回：
            frame: 缩放为128x128并带黑边的图像
        """
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))
        return frame


    def obj_detect(self, img):
        """
        YOLO目标识别核心函数：加载ONNX模型，对输入图像进行目标检测，返回目标坐标和类别
        参数：
            img: 原始输入图像（BGR格式）
        返回：
            若识别到目标：x（目标中心x像素坐标）、y（目标中心y像素坐标）、classes[0]（目标类别索引）
            若未识别到目标：None
        """
        x = y = 0  # 初始化目标中心坐标
        img_ori = img  # 保存原始图像（用于后续绘制目标框）

        # 图像预处理1：缩放为配置文件指定尺寸（用于绘制结果）
        img_ori = self.transform_frame(img)
        # 图像预处理2：缩放为128x128（用于模型输入）
        img = self.transform_frame_128(img)

        # 加载YOLO ONNX模型：模型路径为"/home/robuster/beetle_ai/scripts/beetle_obj.onnx"（需确保路径正确）
        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")

        t1 = time.time()  # 记录模型推理开始时间（用于统计耗时）

        # 图像转模型输入 blob：
        # 1/255.0：像素值归一化（将0-255转为0-1）
        # (128,128)：模型输入尺寸
        # [0,0,0]：像素均值（用于去均值，若模型训练时未使用可设为0）
        # swapRB=True：交换R和B通道（OpenCV默认BGR，模型通常要求RGB）
        # crop=False：不裁剪图像（保持缩放后的完整图像）
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)  # 将blob输入到模型

        # 模型推理：获取输出层结果（YOLO模型输出为目标框、类别、置信度等信息）
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]

        # YOLO后处理：从模型输出中提取目标框（boxes）、类别索引（classes）、置信度（scores）
        # （simple版本：默认只返回置信度最高的一个目标，适用于单目标场景）
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)

        t2 = time.time()  # 记录模型推理结束时间

        # （原代码注释）图像通道转换：若输入为RGB，需转为BGR用于OpenCV显示（本代码输入为BGR，故注释）
        # img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # 若识别到目标（boxes不为空）
        if boxes is not None:
            # 目标框坐标缩放：因模型输入为128x128，需放大5倍匹配原始绘制图像尺寸（需根据实际预处理逻辑调整）
            boxes = boxes * 5
            # 在原始绘制图像上绘制目标框：标注目标框、置信度、类别
            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])
            # 提取目标框的左上角（left, top）和右下角（right, bottom）坐标
            left, top, right, bottom = boxes[0]
            # 计算目标中心坐标（像素）
            x = int((left + right) / 2)
            y = int((top + bottom) / 2)
            # （调试用）打印目标中心坐标（原代码注释，需启用可取消注释）
            # print x, y

        # 显示识别结果图像：窗口名为"figure"，显示绘制后的图像
        cv2.imshow("figure", img_ori)
        cv2.waitKey(2)  # 等待2ms，确保图像正常显示（避免窗口无响应）

        # 打印模型推理耗时（仅推理部分，不含图像预处理）
        print("time: " + str(t2 - t1) + "s")

        # 判断是否识别到目标（x+y>0表示坐标有效）
        if x + y > 0:
            return x, y, classes[0]  # 返回目标中心坐标和类别索引
        else:
            return None  # 未识别到目标，返回None


    def run(self):
        """
        类主函数：启动机械臂初始化和目标检测准备
        """
        # 设置机械臂灯光为蓝色（0,0,255）：表示机械臂处于忙碌状态（mycobot灯光控制：RGB三色值）
        self.mc.set_color(0, 0, 255)
        # 调用机械臂初始化函数：移动到初始姿态
        self.init_mycobot()


# -------------------------- 主程序逻辑（循环执行4次抓取-放置任务） --------------------------
i = 0  # 任务计数器：控制循环执行4次（i从0到3）

# （原代码注释）导航目标初始化：从文件读取3个导航目标（右侧中心、右侧定位、右侧终点），需启用可取消注释
'''
goal1 = read_goal("goal_right_center.txt")
goal2 = read_goal("goal_right_dingwei.txt")
goal3 = read_goal("goal_right_end.txt")
'''

# 主循环：执行4次抓取-放置任务（i < 4）
while i < 4:
    # 第1次任务（i=0）：初始化位置调整与目标检测准备
    if i == 0:
        # （原代码注释）发送第0个导航目标（右侧中心），需启用可取消注释
        # send_goal(i, goal1)
        time.sleep(1)  # 等待2秒，模拟导航后的稳定时间

        # （原代码注释）左转3秒（角速度0.4 rad/s），需启用可取消注释
        # rotate_to_left1(3,0.4)
        time.sleep(0.8)  # 等待1秒

        # （原代码注释）发送第0个导航目标（右侧定位），需启用可取消注释
        # send_goal(i, goal2)
        time.sleep(1)  # 等待2秒

        # 创建Detect_marker实例：初始化目标检测与机械臂控制
        detect = Detect_marker()
        detect.run()  # 启动机械臂初始化（移动到初始姿态）
        time.sleep(1)  # 等待2秒

        # 前进3秒（速度0.2 m/s）：靠近目标物体
        moveforward1(3, 0.2)
        time.sleep(0.8)  # 等待1秒

        # 右转1.3秒（角速度-1 rad/s）：调整朝向，对准目标
        rotate_to_right1(1.3)
        time.sleep(0.8)  # 等待1秒

        # 前进1秒（速度0.3 m/s）：进一步靠近目标
        moveforward1(1, 0.3)
        time.sleep(0.8)  # 等待1秒

        # 左转1.3秒（角速度1 rad/s）：微调朝向，确保目标在相机视野中心
        rotate_to_left1(1.3, 1)
        time.sleep(0.8)  # 等待1秒

        # （原代码注释）其他姿态调整逻辑，根据实际场景选择启用
        '''
        rotate_to_right1(0.3)
        #rotate_to_left1(1.4)
        time.sleep(1)
        moveforward1(0.6,0.4)
        time.sleep(1)
        rotate_to_left1(1,0.5)
        time.sleep(1)
        moveback1(1,-0.22)
        time.sleep(1)
        '''

    # （原代码注释）打印导航结果，需启用可取消注释
    # rospy.loginfo(result)
    i += 1  # 任务计数器自增（进入下一次任务准备）


    # -------------------------- 机械臂抓取前姿态调整 --------------------------
    # 机械臂姿态1：移动到抓取准备位置（关节角度预设，需根据实际场景调试）
    angles = [-90, -29, 0, 40, 0, -45]
    mc.send_angles(angles, 30)  # 速度30
    time.sleep(2)  # 等待3秒，确保姿态到位


    # -------------------------- 相机捕获与目标识别（循环直到识别到目标） --------------------------
    # 初始化相机捕获：打开第2个相机设备（索引2，根据实际相机数量调整，0为默认相机）
    cap = cv2.VideoCapture(2)
    while True:
        # 发送轻微前进指令（0.02 m/s）：缓慢靠近目标，确保目标进入最佳识别范围
        move_cmd.linear.x = 0.04  # 线速度0.02 m/s
        move_cmd.linear.z = 0     # z轴速度0（底盘无z轴运动）
        pub.publish(move_cmd)     # 发布运动指令

        # 读取相机帧：retval为是否读取成功（True/False），frame为读取到的图像（BGR格式）
        retval, frame = cap.read()
        # 图像翻转：先上下翻转（0），再左右翻转（1），适配相机安装方向（确保目标方向正确）
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)

        # 调用目标检测函数：获取识别结果（x,y,类别）或None
        detect_result = detect.obj_detect(frame)
        if detect_result is None:
            # 未识别到目标：继续循环捕获图像
            continue
        else:
            # 识别到目标：提取目标中心坐标（x,y）和类别索引（outcome1）
            x, y, outcome1 = detect_result
            # 图像坐标转实际坐标：计算目标相对于机械臂的实际距离（mm）
            real_x, real_y = detect.get_position(x, y)
            print(real_x, real_y)  # 打印实际坐标（调试用）

            # 判断目标是否在抓取范围内（x: -10~20mm，y: -10~150mm，需根据实际机械臂工作空间调整）
            if (real_x < 20 and real_x > -10) and (real_y > -10 and real_y < 150):
                break  # 目标在范围内：退出识别循环，准备抓取

        # 按键退出：按下"q"键（ASCII码0xFF），退出识别循环（手动中断用）
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            # cap.close()  # （原代码注释）关闭相机，需启用可取消注释

    # 释放相机资源：关闭相机设备
    cap.release()
    # 关闭所有OpenCV窗口：避免残留显示窗口
    cv2.destroyAllWindows()


    # -------------------------- 机械臂抓取动作（多步姿态调整+夹爪闭合） --------------------------
    # 姿态2：抓取前的预抓取位置（靠近目标，需根据实际目标位置调试）
    angles = [-94.92, -50.44, 68.46, -19.33, 3.86, -45.96]
    mc.send_angles(angles, 30)  # 速度30
    time.sleep(2)  # 等待3秒

    # 姿态3：抓取位置（机械臂末端到达目标正上方，准备夹取）
    angles = [-87.27, -29.79, -40.95, 142.11, -4.21, -48.25]
    mc.send_angles(angles, 30)  # 速度30
    time.sleep(1.5)  # 等待3秒

    # 姿态4：微调抓取位置（确保夹爪对准目标）
    angles = [-90.87, -25.22, -41.13, 69.16, -0.08, -48.51]
    mc.send_angles(angles, 30)  # 速度30
    time.sleep(1.2)  # 等待3秒

    # 夹爪闭合：设置夹爪值为10（0为完全闭合，255为完全打开，需根据目标尺寸调试），速度30
    mc.set_gripper_value(10, 30)
    time.sleep(1)  # 等待1.5秒，确保夹爪夹紧目标


    # -------------------------- 抓取后机械臂姿态调整（抬起目标，准备移动） --------------------------
    # 姿态5：抓取后抬起（避免目标碰撞周围环境）
    angles = [-90, 0, 0, 0, 0, -45]
    mc.send_angles(angles, 50)  # 速度50（比抓取时快，提高效率）
    time.sleep(1)  # 等待1.5秒

    # 姿态6：移动到放置准备位置（远离抓取区域，准备导航到放置区）
    angles = [0, 0, 0, 0, 0, 0]
    mc.send_angles(angles, 50)  # 速度50
    time.sleep(2)  # 等待3秒

    # 姿态7：放置前的预放置位置（靠近放置区域，准备释放目标）
    angles = [11, -23, -39, -29, -3, 58]
    mc.send_angles(angles, 50)  # 速度50
    time.sleep(1)  # 等待1.5秒


    # -------------------------- 底盘移动到放置区域（根据任务次数调整后退距离） --------------------------
    # 根据当前任务次数（i）调整后退距离（远离抓取区，前往放置区）
    if i == 1:
        # 第1次任务：后退0.1秒（速度-0.1 m/s）
        # moveback1(0.1,-0.1)
        time.sleep(0.8)  # 等待1秒（原代码注释移动，暂用延时替代）
    elif i == 2:
        # 第2次任务：后退0.3秒（速度-0.1 m/s）
        moveback1(0.3, -0.1)
        time.sleep(0.8)  # 等待1秒
    elif i == 3:
        # 第3次任务：后退1.5秒（速度-0.1 m/s）
        moveback1(1.5, -0.1)
        time.sleep(0.8)  # 等待1秒
    elif i == 4:
        # 第4次任务：后退2.7秒（速度-0.1 m/s，因i<4，实际不会执行）
        moveback1(2.7, -0.1)
        time.sleep(0.8)  # 等待1秒

    # 左转1.3秒（速度-1 rad/s）：调整朝向，对准放置区域
    rotate_to_left1(1.3, -1)
    time.sleep(0.8)  # 等待1秒

    # 后退2.7秒（速度-0.2 m/s）：到达放置区域附近
    moveback1(2.7, -0.2)
    time.sleep(1)  # 等待2秒

    # （原代码注释）发送导航目标到放置区，需启用可取消注释
    # send_goal(i, goal1)

    # （原代码注释）其他姿态调整，根据实际场景选择启用
    # time.sleep(1)
    # rotate_to_left1(1.3,1)
    # time.sleep(1)
    # moveback1(0.7,-0.22)
    # time.sleep(1)

    # （原代码注释）打印导航结果，需启用可取消注释
    # rospy.loginfo(result)


    # -------------------------- 机械臂放置目标（根据目标类别和放置次数选择放置位置） --------------------------
    # 第1次放置（init_num=0）：首次放置，记录目标类别，放置到左侧1号位置
    if init_num == 0:
        # 左侧1号放置位置：机械臂姿态（需根据实际放置区位置调试）
        angles = [-152, -73, 6, -13, -3, 58]
        mc.send_angles(angles, 30)  # 速度30
        time.sleep(2)  # 等待3秒

        # 夹爪释放：设置夹爪值为255（完全打开），释放目标
        mc.set_gripper_value(255, 30)
        time.sleep(1.2)  # 等待3秒，确保目标完全释放

        # 回到放置准备位置：为下一次放置做准备
        angles = [11, -23, -39, -29, -3, 58]
        mc.send_angles(angles, 30)  # 速度30
        time.sleep(1.5)  # 等待3秒

        # 更新状态变量：记录首次识别类别、左侧放置次数+1、放置次数+1
        num1 = outcome1
        left_num += 1
        init_num += 1

    # 第2次放置（init_num=1）：根据首次类别判断放置位置（同类放左侧，不同放右侧）
    elif init_num == 1:
        # 若当前目标类别与首次类别相同（num1 == outcome1）：放置到左侧2号位置
        if num1 == outcome1:
            # 左侧2号放置位置：机械臂姿态
            angles = [-140, -74, 6, -13, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.5)  # 等待2秒

            # 夹爪释放：完全打开
            mc.set_gripper_value(255, 40)
            time.sleep(1)  # 等待2秒

            # 回到放置准备位置
            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.2)  # 等待2秒

            print('222222')  # 调试日志：标记左侧2号放置

            # 更新状态变量：左侧放置次数+1、放置次数+1
            left_num += 1
            init_num += 1

        # 若当前目标类别与首次类别不同：放置到右侧1号位置
        else:
            # 右侧1号放置位置：机械臂姿态
            angles = [173, -74, 6, -13, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.5)  # 等待2秒

            # 夹爪释放：完全打开
            mc.set_gripper_value(255, 40)
            time.sleep(1)  # 等待2秒

            # 回到放置准备位置
            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.2)  # 等待2秒

            print('3333333')  # 调试日志：标记右侧1号放置

            # 更新状态变量：放置次数+1
            init_num += 1

    # 第3次放置（init_num=2）：根据首次类别和左侧放置次数判断位置
    elif init_num == 2:
        # 若当前目标类别与首次类别相同：放置到左侧2号位置
        if num1 == outcome1:
            # 左侧2号放置位置（与第2次同类放置相同）
            angles = [-140, -74, 6, -13, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.5)  # 等待2秒

            # 夹爪释放：完全打开
            mc.set_gripper_value(255, 40)
            time.sleep(1)  # 等待2秒

            # 回到放置准备位置
            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.2)  # 等待2秒

            # 更新状态变量：左侧放置次数+1、放置次数+1
            left_num += 1
            init_num += 1

        # 若左侧已放置2次（left_num==2）：放置到右侧1号位置
        elif left_num == 2:
            # 右侧1号放置位置（与第2次不同类放置相同）
            angles = [173, -74, 6, -13, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.5)  # 等待2秒

            # 夹爪释放：完全打开
            mc.set_gripper_value(255, 40)
            time.sleep(1)  # 等待2秒

            # 回到放置准备位置
            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.2)  # 等待2秒

            # 更新状态变量：放置次数+1
            init_num += 1

        # 其他情况：放置到右侧2号位置
        else:
            # 右侧2号放置位置：机械臂姿态
            angles = [170.15, -91.31, 4.83, 40.42, -10.72, 66.7]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.5)  # 等待2秒

            # 夹爪释放：完全打开
            mc.set_gripper_value(255, 40)
            time.sleep(1)  # 等待2秒

            # 微调姿态：确保目标平稳放置
            angles = [167.6, -37.26, 3.77, -21.88, 3.07, 28.74]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1)  # 等待2秒

            # 回到放置准备位置
            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.2)  # 等待2秒

            # 更新状态变量：放置次数+1
            init_num += 1

    # 第4次放置（init_num>=3）：根据左侧放置次数判断位置
    else:
        # 若左侧已放置2次：放置到右侧2号位置
        if left_num == 2:
            # 右侧2号放置位置（与第3次其他情况放置相同）
            angles = [170.15, -91.31, 4.83, 40.42, -10.72, 66.7]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.5)  # 等待2秒

            # 夹爪释放：完全打开
            mc.set_gripper_value(255, 40)
            time.sleep(1)  # 等待2秒

            # 微调姿态：确保目标平稳放置
            angles = [167.6, -37.26, 3.77, -21.88, 3.07, 28.74]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1)  # 等待2秒

            # 回到放置准备位置
            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.2)  # 等待2秒

        # 其他情况：放置到左侧2号位置
        else:
            # 左侧2号放置位置（与第2次同类放置相同）
            angles = [-140, -74, 6, -13, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.5)  # 等待2秒

            # 夹爪释放：完全打开
            mc.set_gripper_value(255, 40)
            time.sleep(1)  # 等待2秒

            # 回到放置准备位置
            angles = [11, -23, -39, -29, -3, 58]
            mc.send_angles(angles, 40)  # 速度40
            time.sleep(1.2)  # 等待2秒


    # -------------------------- 机械臂回到抓取准备姿态（为下一次任务做准备） --------------------------
    # 回到抓取前的准备姿态
    angles = [-90, -29, 0, 40, 0, -45]
    mc.send_angles(angles, 50)  # 速度40
    time.sleep(1.5)  # 等待2秒


    # -------------------------- 底盘移动到下一次抓取位置（根据任务次数调整） --------------------------
    # 若未完成4次任务（i<4）：移动到下一次抓取的初始位置
    if i < 4:
        # 前进2.68秒（速度0.2 m/s）：远离放置区，前往下一次抓取区
        moveforward1(2.68, 0.2)
        time.sleep(1.2)  # 等待3秒

        # 根据任务次数调整左转角度（第1次任务左转角度更大）
        if i < 1:
            # 第1次任务后：左转3.32秒（速度0.5 rad/s）
            rotate_to_left1(3.32, 0.5)
            time.sleep(1)  # 等待2秒
        else:
            # 其他任务后：左转3.18秒（速度0.5 rad/s）
            rotate_to_left1(3.18, 0.5)
            time.sleep(1)  # 等待2秒


# -------------------------- 所有任务完成后的收尾动作 --------------------------
# 设置机械臂灯光为绿色（0,255,0）：表示所有任务完成，机械臂处于空闲状态
mc.set_color(0, 255, 0)

# 机械臂回到最终空闲姿态（远离工作区，避免碰撞）
angles = [-83.23, -140.53, 140.97, 58.71, -127.61, 5.71]
mc.send_angles(angles, 60)  # 速度40
time.sleep(1.2)  # 等待3秒

# 底盘前进0.9秒（速度0.2 m/s）：离开放置区
moveforward1(0.45, 0.4)
time.sleep(1.5)  # 等待3秒

# 左转3.15秒（速度-0.5 rad/s）：调整朝向，准备返回起点
rotate_to_left1(3.15, -0.5)
time.sleep(1)  # 等待2秒

# 前进8秒（速度0.2 m/s）：返回起点方向
moveforward1(4, 0.4)
time.sleep(0.8)  # 等待1秒

# 左转0.85秒（速度-0.5 rad/s）：微调朝向，对准起点
rotate_to_left1(0.85, -0.5)
time.sleep(1)  # 等待2秒

# 前进5秒（速度0.2 m/s）：到达起点
moveforward1(2.5, 0.4)
time.sleep(0.8)  # 等待1秒

# （原代码注释）发送导航目标到终点（右侧终点），需启用可取消注释
# send_goal(1, goal3)