#encoding: UTF-8
#!/usr/bin/env python3
import os
import urllib
import traceback
import time
import sys
import numpy as np
import cv2

class yolo(object):

    def __init__(self, OBJ_THRESH, NMS_THRESH, CLASSES):
        super(yolo, self).__init__()
        self.OBJ_THRESH = OBJ_THRESH
        self.NMS_THRESH = NMS_THRESH
        self.CLASSES = CLASSES

    def xywh2xyxy(self, x):
        # Convert [x, y, w, h] to [x1, y1, x2, y2]
        y = np.copy(x)
        y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
        y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
        y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
        y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
        return y


    def nms_boxes(self, boxes, scores):
        """Suppress non-maximal boxes.

        # Arguments
            boxes: ndarray, boxes of objects.
            scores: ndarray, scores of objects.

        # Returns
            keep: ndarray, index of effective boxes.
        """
        x = boxes[:, 0]
        y = boxes[:, 1]
        w = boxes[:, 2] - boxes[:, 0]
        h = boxes[:, 3] - boxes[:, 1]

        areas = w * h
        order = scores.argsort()[::-1]

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)

            xx1 = np.maximum(x[i], x[order[1:]])
            yy1 = np.maximum(y[i], y[order[1:]])
            xx2 = np.minimum(x[i] + w[i], x[order[1:]] + w[order[1:]])
            yy2 = np.minimum(y[i] + h[i], y[order[1:]] + h[order[1:]])

            w1 = np.maximum(0.0, xx2 - xx1 + 0.00001)
            h1 = np.maximum(0.0, yy2 - yy1 + 0.00001)
            inter = w1 * h1

            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = np.where(ovr <= self.NMS_THRESH)[0]
            order = order[inds + 1]
        keep = np.array(keep)
        return keep

    def yolov5_post_process_simple(self, prediction):
        nc = prediction.shape[2] - 5
        xc = prediction[..., 4] > self.OBJ_THRESH
        valid_object = prediction[xc]
        valid_object[:,5:] *= valid_object[:,4:5]

        boxes = self.xywh2xyxy(valid_object[:,:4])
        best_score_class = np.max(valid_object[:,5:],axis=-1)
        box_classes = np.argmax(valid_object[:,5:], axis=-1)
        
        nboxes, nclasses, nscores = [], [], []
        for c in set(box_classes):
            inds = np.where(box_classes == c)
            b = boxes[inds]
            c = box_classes[inds]
            s = best_score_class[inds]


            keep = self.nms_boxes(b, s)
            if s[keep][0] < self.OBJ_THRESH:
                print(s[keep])
                continue
            nboxes.append(b[keep])
            nclasses.append(c[keep])
            nscores.append(s[keep])

        if not nclasses and not nscores:
            return None, None, None

        boxes = np.concatenate(nboxes)
        classes = np.concatenate(nclasses)
        scores = np.concatenate(nscores)

        return boxes, classes, scores


    def draw(self, image, boxes, scores, classes):
        """Draw the boxes on the image.

        # Argument:
            image: original image.
            boxes: ndarray, boxes of objects.
            classes: ndarray, classes of objects.
            scores: ndarray, scores of objects.
            all_classes: all classes name.
        """
        # print("draw boxes: ", boxes, np.shape(boxes), len(boxes))
        # print("draw scores: ", scores, np.shape(scores), len(scores))
        # print("draw classes: ", classes, np.shape(classes), len(classes))
        for box, score, cl in zip(boxes, scores, classes):
            self.draw_single(image, box, score, cl)

    def draw_single(self, image, box, score, cl):    
        
        left, top, right, bottom = box
        print('class: {}, score: {}'.format(self.CLASSES[int(cl)], float(score)))
        print('box coordinate left,top,right,down: [{}, {}, {}, {}]'.format(left, top, right, bottom))
        top = int(top)
        left = int(left)
        right = int(right)
        bottom = int(bottom)

        cv2.rectangle(image, (left,top), (right, bottom), (255, 0, 0), 2)
        cv2.putText(image, '{0} {1:.2f}'.format(self.CLASSES[int(cl)], float(score)),
                    (left, top - 6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255), 2)


    def letterbox(self, im, new_shape=(640, 640), color=(0, 0, 0)):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / float(shape[0]), new_shape[1] / float(shape[1]))

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return im, ratio, (dw, dh)

