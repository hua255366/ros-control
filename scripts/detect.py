import cv2
import time
from opencv_yolo import yolo
from VideoCapture import FastVideoCapture
from GrabParams import grabParams

CLASSES = ("apple", "clock", "banana", "cat", "bird")


class DetectOnly(object):
    def __init__(self):
        self.yolo = yolo()
        self.net = cv2.dnn.readNetFromONNX(
            "/home/robuster/beetle_ai/scripts/beetle_obj.onnx"
        )
        self.c_x, self.c_y = grabParams.IMG_SIZE / 2, grabParams.IMG_SIZE / 2

    def transform_frame(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(
            frame, (grabParams.IMG_SIZE, grabParams.IMG_SIZE))
        return frame

    def transform_frame_128(self, frame):
        frame, ratio, (dw, dh) = self.yolo.letterbox(frame, (128, 128))
        return frame

    # 跟 obj_detect 逻辑一致，只是不触发任何机械臂动作，纯返回检测结果
    def obj_detect(self, img):
        x = y = 0
        class_name = None

        img_ori = self.transform_frame(img)
        img = self.transform_frame_128(img)

        blob = cv2.dnn.blobFromImage(
            img, 1 / 255.0, (128, 128), [0, 0, 0], swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.net.getUnconnectedOutLayersNames())[0]

        boxes, classes, scores = self.yolo.yolov5_post_process_simple(outputs)

        if boxes is not None:
            boxes = boxes * 5
            self.yolo.draw_single(img_ori, boxes[0], scores[0], classes[0])
            left, top, right, bottom = boxes[0]
            x = int((left + right) / 2)
            y = int((top + bottom) / 2)
            class_name = CLASSES[classes[0]]

        cv2.imshow("detect only (press q to quit)", img_ori)

        if x + y > 0:
            return x, y, class_name
        else:
            return None


if __name__ == "__main__":
    detect = DetectOnly()
    cap = FastVideoCapture(grabParams.cap_num)
    time.sleep(0.5)

    try:
        while True:
            frame = cap.read()
            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)

            result = detect.obj_detect(frame)
            if result is not None:
                x, y, class_name = result
                # 跟画面中心的像素差，标定 ratio 就是要这两个数(dx, dy)
                dx = detect.c_x - x
                dy = y - detect.c_y
                print("识别到: %-6s 像素坐标(x,y)=(%d,%d)  跟中心的像素差(dx,dy)=(%.1f,%.1f)"
                      % (class_name, x, y, dx, dy))

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.close()
        cv2.destroyAllWindows()
