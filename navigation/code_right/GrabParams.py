#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):

    pace_apple_site = "left"
    # pace_apple_site = "right"

    # get the results by calibration

    ###以下是左边的偏移量
    # get the results by calibration
    ratio = 0.223 #0.223 #0.196    0.230      # 像素到实际坐标的转换比例230,219
    
    # increase x_bias to move front, or decrease x_bias to move back
    x_bias =  18#     18   -9    14        # X轴偏移校准

    # increase y_bias to move left, or decrease y_bias to move right
    y_bias = 8   #9、-3 15              # Y轴偏移校准

    ##以下是右边的偏移量
    # ratio = 0.223 #0.196
    # # increase x_bias to move front, or decrease x_bias to move back
    # x_bias = -5 #-8
    # # increase y_bias to move left, or decrease y_bias to move right
    # y_bias = -2

    #                    (-x)front
    #                     
    #                     :
    #                     :
    #                     :
    # (-y)< ..............o..............(y)right
    #                     :
    #                     :
    #                     :
    #                     :
    #                    (x)

    # increase height_bias to move higher, or decrease height_bias to move lower
    height_bias = 264.1 + 70  #50  原来的是：264.1 + 72         # 抓取高度偏移
    y = -120   #-120

    # 映射关系控制参数
    mapping_mode = 1  # 映射模式: 0=三段式, 1=线性映射, 2=阶梯映射
    linear_range_low = 85  # 线性映射区间下限
    linear_range_high = 240  # 线性映射区间上限
    step_count = 10  # 阶梯映射的阶梯数量

    y_far = -120
    y_middle = -90
    y_near = -62

    #机械臂在左边
    # coords_ready = [-60.3, 66.4, 324.7, 84.71, 45.99, 171.69]
    # angles_ready = [-88.59, -35.94, 110.03, -77.78, 174.11, 133.5]
    ##机械臂在右边
    # coords_ready = [63.9, 73.3, 314.0, 82.19, 50.05, 172.58]
    # angles_ready = [91.14, -69.52, 116.54, -42.01, -2.54, 129.46]


##左边地图的准备姿态！！！！！！！！！！！！！！！
    angles_ready = [-88.33, -64.59, 107.84, -47.02, -1.58, 131.3]
    coords_ready = [-62.1, -79.3, 315, 91.96, 47.9, 2]
    angles_finish = [-87.36, -64.16, 69.34, 23.46, -2.81, 133.76]
    coords_finish = [-61.2, -97.5, 362.6, 52.49, 38.12, -25.92]

    angles_back = [-82.08, -139.83, 138.95, 59.76, -128.67, 5.0]
    coords_back = [-98.9, -7.3, 157.2, -139.53, 45.31, 35.63]

    # 根据放置位置设置目标坐标
    if pace_apple_site == "left":
        coords_place_apple = [-278.1, -87.0, 145, -145.11, -27.32, 146.66]  #放我的右边
        coords_place_clock = [-234.5, 114.6, 150, 135.87, 42.76, -65.28]  #放我的左边
    if pace_apple_site == "right":
        coords_place_apple = [252.8, -114.8, 139.8, 157.4, 23.51, 100.7]
        coords_place_clock = [267.3, 76.5, 149.5, 153.88, 24.93, 138.77]

    # 运动控制参数
    max_moves = 50                              # 最大移动次数
    GRAB_MOVE_SPEED = 20                        # 抓取移动速度
    stop_back = 310 #480             # 物体检测前停止阈值(像素)
    stop_middle = 350  #350,410，420 460          # 物体检测后停止阈值(像素)
    debug = True #True          

    # please do not change the parameter values below
    IMG_SIZE = 640
    done = False
    cap_num = 2
    usb_dev = "/dev/arm"
    baudrate = 115200

grabParams = GrabParams()

