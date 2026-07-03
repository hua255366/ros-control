#encoding: UTF-8
#!/usr/bin/env python2
from pymycobot.mycobot import MyCobot
import time
import dnn_grab_2
from VideoCapture import FastVideoCapture
from GrabParams import grabParams

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
boxes
        # The coordinates of the cube relative to the mycobot
        self.c_x, self.c_y = grabParams.IMG_SIZE/2, grabParams.IMG_SIZE/2
        # The ratio of pixels to actual values
        self.ratio = grabParams.ratio


    # Grasping motion
    def move(self, x, y):
        global height_bias, done
        #coords_target = [(coords[0]+int(x)-15), -(coords[1]+int(y)-10), height_bias, coords[3], coords[4], coords[5]]
        coords_target = [(coords[0]+int(x)), (coords[1]+int(y)), height_bias, coords[3], coords[4], coords[5]]
        basic.move_to_target_coords(coords_target, grabParams.GRAB_MOVE_SPEED)
        print(coords_target)

        basic.grap(True)

        angles = [0,10,-50,10,0,0]
        self.mc.send_angles(angles,30)
        time.sleep(1)

        done = True
        print("Done")
        #self.mc.set_color(0,255,0)#green, arm is free


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
        img_ori = img
        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        #加载模型
        net = cv2.dnn.readNetFromONNX("/home/robuster/beetle_ai/scripts/beetle_obj.onnx")
        #net = cv2.dnn.readNetFromONNX(grabParams.ONNX_MODEL)

        t1 = time.time()
        #输入数据处理
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)#128
        #blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (grabParams.IMG_SIZE, grabParams.IMG_SIZE), [0, 0, 0], swapRB=True, crop=False)
        net.setInput(blob)
        
        #推理
        outputs = net.forward(net.getUnconnectedOutLayersNames())[0]

        
        #获得识别结果
        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)
        t2 = time.time()

        # img_0 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if boxes(top+bottom)/2
            # print x, y

        self.show_image(img_ori)  

        # Print time (inference-only)
        print("time: " + str(t2-t1) + "s")  

      
        if x+y > 0:
            return x, y
        else:
            return None

    def run(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.init_mycobot()

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(50) 
        
 is not None:
            boxes = boxes*5
            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])
            #self.yolo.draw_single(img, boxes, scores, classes)
            left, top, right, bottom = boxes[0]
            x = int((left+right)/2)
            y = int((top+bottom)/2)
            # print x, y

        self.show_image(img_ori)  

        # Print time (inference-only)
        print("time: " + str(t2-t1) + "s")  

      
        if x+y > 0:
            return x, y
        else:
            return None

    def run(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.init_mycobot()

    def show_image(self, img):
        if grabParams.debug and args.debug:
            cv2.imshow("figure", img)
            cv2.waitKey(50) 
        

if __name__ == "__main__":

	mc = MyCobot('/dev/arm',115200)
	#将LED变色
	mc.set_color(200,200,200)
	#到达上层初始位置
	mc.send_coords([(-64.6) , (-154.2) , 381.4 , (-89.62) , (-44.89) , 176.13 ],25,0)

	detect = Detect_marker()
	detect.run()

	time.sleep(5)
	cap = FastVideoCapture(grabParams.cap_num)
	time.sleep(0.5) 
	while(1):
		frame = cap.read()
	        #frame = cv2.flip(frame,0)
	        #frame = cv2.flip(frame,1)
		frame = detect.transform_frame(frame)
	detect.show_image(frame)
