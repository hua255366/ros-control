#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

"""
机器人任务收尾动作独立测试代码
功能：执行所有抓取-放置任务完成后的收尾流程，包括：
1. 机械臂灯光设置为绿色（空闲状态）
2. 机械臂回到最终空闲姿态
3. 底盘移动到起点位置
"""

import time
import rospy
from pymycobot.mycobot import MyCobot
from GrabParams import grabParams
from geometry_msgs.msg import Twist


def main():
    # 初始化ROS节点
    rospy.init_node('robot_cleanup_test', anonymous=True)

    # 创建底盘运动指令发布者
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    move_cmd = Twist()
    rate = rospy.Rate(20)  # 20Hz发布频率

    # 初始化机械臂
    try:
        mc = MyCobot(grabParams.usb_dev, grabParams.baudrate)
        print("机械臂连接成功")
    except Exception as e:
        print(f"机械臂连接失败: {e}")
        return

    # 1. 设置机械臂灯光为绿色（表示任务完成，空闲状态）
    print("设置机械臂灯光为绿色...")
    mc.set_color(0, 255, 0)  # RGB绿色
    time.sleep(1)

    # 2. 机械臂回到最终空闲姿态（远离工作区，避免碰撞）
    print("机械臂回到最终空闲姿态...")
    final_angles = [-83.23, -140.53, 140.97, 58.71, -127.61, 5.71]
    mc.send_angles(final_angles, 40)  # 速度40
    time.sleep(1.2)  # 等待姿态到位

    # 3. 底盘离开放置区
    print("底盘离开放置区...")
    move_cmd.linear.x = 0.4  # 前进速度0.4m/s
    for _ in range(int(0.45 * 20)):  # 持续0..45秒
        pub.publish(move_cmd)
        rate.sleep()
    move_cmd.linear.x = 0  # 停止前进
    pub.publish(move_cmd)
    time.sleep(1.2)

    # 4. 左转调整朝向，准备返回起点
    print("调整朝向...")
    move_cmd.angular.z = -0.5  # 左转角速度-0.5rad/s
    for _ in range(int(3.15 * 20)):  # 持续3.15秒
        pub.publish(move_cmd)
        rate.sleep()
    move_cmd.angular.z = 0  # 停止旋转
    pub.publish(move_cmd)
    time.sleep(1)

    # 5. 前进返回起点方向
    print("返回起点方向...")
    move_cmd.linear.x = 0.4  # 前进速度0.4m/s
    for _ in range(int(4 * 20)):  # 持续8秒
        pub.publish(move_cmd)
        rate.sleep()
    move_cmd.linear.x = 0  # 停止前进
    pub.publish(move_cmd)
    time.sleep(0.8)

    # 6. 微调朝向，对准起点
    print("微调朝向对准起点...")
    move_cmd.angular.z = -0.5  # 左转角速度-0.5rad/s
    for _ in range(int(0.85 * 20)):  # 持续0.85秒
        pub.publish(move_cmd)
        rate.sleep()
    move_cmd.angular.z = 0  # 停止旋转
    pub.publish(move_cmd)
    time.sleep(1)

    # 7. 前进到达起点
    print("到达起点...")
    move_cmd.linear.x = 0.4  # 前进速度0.3m/s
    for _ in range(int(2.5 * 20)):  # 持续5秒
        pub.publish(move_cmd)
        rate.sleep()
    move_cmd.linear.x = 0  # 停止前进
    pub.publish(move_cmd)
    time.sleep(0.8)

    print("所有收尾动作完成!")


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        print("程序被ROS中断")
    except Exception as e:
        print(f"发生错误: {e}")
