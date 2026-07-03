# ros-control
A robotic arm control project completed by a junior (third-year) student during a 10-day on-campus internship

这是一个我实践可用的物体识别代码，主要在于识别（手眼标定）加yolo以及夹取，本人夹取（控制机器人部分比较熟悉）,后期我会上传一个ros的版本，由于刚接手用的mycobot所以暂时只能先接着用下去.

# 📘 `README.md`（GitHub版本）

```md
# 🦾 Vision-Based Robotic Grasping & Sorting System (MyCobot)

一个基于 **YOLO目标检测 + 机械臂控制（MyCobot）** 的实时视觉抓取与分拣系统。

系统实现了从：

> 📷 摄像头图像 → 🧠 目标识别 → 📍 坐标映射 → 🤖 机械臂抓取 → 📦 分类放置

的完整闭环机器人操作流程。

---

# 🎯 项目目标

本项目旨在实现一个低成本、可扩展的：

> 视觉驱动机械臂自动抓取与分类系统

核心能力包括：

- 实时目标检测（YOLO / OpenCV DNN）
- 图像坐标 → 机械臂空间坐标映射
- 机械臂 Pick & Place 控制
- 基于类别的自动分拣策略

---

# 🧠 系统架构

```

摄像头图像
↓
YOLO / DNN目标检测
↓
目标像素坐标 (x, y)
↓
坐标转换（pixel → mm）
↓
机械臂运动控制（MyCobot）
↓
夹爪抓取 / 放置策略
↓
分拣结果输出

````

---

# 🧩 核心模块

## 1️⃣ 视觉识别模块（Object Detection）

使用 OpenCV DNN + ONNX 模型：

```python
self.net = cv2.dnn.readNetFromONNX("beetle_obj.onnx")
````

### 功能：

* 实时检测图像中的目标物体
* 输出：

  * bounding box
  * class label
  * confidence score

### 支持类别：

```text
apple, clock, banana, cat, bird
```

其中：

* `banana → cat`（项目内类别映射规则）

---

## 2️⃣ 坐标映射模块（核心）

```python
def get_position(x, y):
```

### 作用：

将图像中的像素坐标转换为机械臂工作空间坐标（mm）

### 核心思想：

```text
pixel space → robot workspace
```

转换基于：

* 图像中心点
* 标定比例系数（ratio）
* 机械臂运动方向（front / right）

---

## 3️⃣ 机械臂控制模块（MyCobot）

底层控制封装在 `basic.py`

### 功能包括：

* 位置移动（send_coords）
* 夹爪控制（open / close）
* 关节释放 / 控制
* 运动状态反馈

---

### 抓取核心流程：

```python
1. 移动到目标物体上方
2. 下降到抓取高度
3. 关闭夹爪
4. 抬升避免碰撞
5. 移动到目标放置点
6. 松开夹爪
7. 返回初始位置
```

---

## 4️⃣ 分拣策略模块

基于类别的规则映射：

```python
CLASS_TO_PLACE_POINT = {
    "cat":  right_side_position,
    "bird": left_side_position
}
```

### 行为逻辑：

* cat → 右侧放置点
* bird → 左侧放置点

---

# 🦾 Pick & Place 工作流程

完整流程如下：

```text
检测到目标
↓
获取像素坐标
↓
转换为机械臂坐标
↓
移动到目标上方
↓
下降抓取
↓
夹爪闭合
↓
抬升避障
↓
移动到分类区域
↓
释放物体
↓
返回待机点
```

---

# ⚙️ 技术细节

## 📷 图像处理

* OpenCV DNN
* YOLO post-processing
* letterbox resize
* center-based coordinate extraction

---

## 🤖 机械臂控制

* MyCobot SDK
* 串口通信
* 坐标系控制（Cartesian control）

---

## 📦 抓取优化设计

### ✔ 抬升策略（防碰撞）

```python
LIFT_OFFSET = 40  # mm
```

避免抓取过程中拖拽物体

---

### ✔ 运动确认机制

通过：

```python
mc.is_in_position()
mc.get_coords()
```

确认到位

---

# 📊 系统特点

* ✔ 实时视觉识别
* ✔ 端到端抓取控制
* ✔ 类别驱动分拣
* ✔ 简单可扩展结构
* ✔ 低成本机械臂实现

---

# ⚠️ 当前局限

* 坐标映射为经验比例（未标定相机模型）
* 非ROS架构（单进程控制）
* 无轨迹规划（直接send_coords）
* 无视觉跟踪（单帧检测）

---

# 🚀 可扩展方向

* ROS2模块化改造
* MoveIt轨迹规划
* 相机标定（Hand-Eye Calibration）
* 多目标追踪（Tracking）
* 强化学习控制策略替换规则系统

---

# 📂 项目结构

```
basic.py              # 机械臂底层控制封装
dnn_grab_2.py         # 视觉 + 控制主流程
GrabParams.py         # 参数配置
opencv_yolo.py        # YOLO后处理工具
VideoCapture.py       # 视频输入
```

---

# 🧠 项目本质

本项目本质是：

> 一个基于视觉的工业级 Pick & Place 原型系统

实现了：

* 计算机视觉
* 坐标系统转换
* 机器人控制闭环
* 自动分拣策略

---

# 👨‍💻 作者理解重点

本项目重点在：

> 🧠 “如何把视觉模型输出变成物理世界动作”

而不是单纯的目标检测或机械臂控制。

---






