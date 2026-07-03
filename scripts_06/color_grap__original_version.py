class Detect_marker(object):
    def __init__(self):
        super(Detect_marker, self).__init__()

        self.mc = Mycobot(grabParams.usb_dev, grabParams.baudrate)
        self.mc.power_on()

        self.yolo = yolo()
        #set color HSV
        self.HSV = {
            "yellow": [np.array([11,115,70]),np.array([40,255,245])],
            "red": [np.array([0,43,46]),np.array([8,255,255])],
            "green": [np.array([35,43,46]),np.array([77,255,255])],
            "blue": [np.array([110,43,46]),np.array([124,255,255])],
            "purple": [np.array([120,43,46]),np.array([200,255,255])],
        }

    def move_to_target_coords(self,coords,speed):
        print("move_to_target_coords")
        self.mc.send_coords(coords,speed,1)
        is_finised = self.mc.is_in_position(coords,1)
        print(is_finised)
        count = 0
        is_finised_count = 0
        while is_finised_count < 3 and count < 10:
            print(is_finised)
            if self.mc.is_in_position(coords,1):
                is_finised_count += 1
            time.sleep(0.5)
            count = count + 1


    #grab
    def grap(self,flag):
        if flag:
            # close
            # self.mc.set_gripper_state(1, 0)
            self.mc.set_gripper_value(50,20)
        else:
            # open
            # self.mc.set_gripper_state(0, 0)
            self.mc.set_gripper_value(255,20)


    #Grasping motion
    def move(self, x, y):
        self.move_to_target_coords([self.coords[0]+int(x), self.coords[1]+int(y), grabParams.height_bias, self.coords[3], self.coords[4], self.coords[5]], 15)

        self.grap(True)
        time.sleep(1)

        self.move_to_target_coords(self.coords, 15)

        self.done = True
        print("Done")
        self,mc.set_color(0,255,0)#green, arm is free


    # get points of two aruco
    def get_calculate_params(self, img):
        # Convert the image to a gray image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect ArUco marker.
        corners, ids, rejectImaPoint = cv2.aruco.detectMarkers(
            gray, self.aruco_dict, parameters=self.aruco_params
        )

        # print corners, len(corners)

        """
        Two Arucos must be present in the picture and in the same order.
        There are two Arucos in the Corners, and each aruco contains the pixels of its four corners.
        Determine the center of the aruco by the four corners of the aruco.
        """
        if len(corners) > 0:
            if ids is not None:
                if len(corners) <= 1 or ids[0] == 1:
                    return None
                x1 = x2 = y1 = y2 = 0
                point_11, point_21, point_31, point_41 = corners[0][0]
                x1, y1 = int(point_11[0]), int(point_11[1])
                point_1, point_2, point_3, point_4 = corners[1][0]
                x2, y2 = int(point_1[0]), int(point_1[1])
                return x1, x2, y1, y2
        return None


    #set camera clipping parameters
    def set_cut_params(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        print(self.x1, self.y1, self.x2, self.y2)


    #set parameters to calculate the coords between cube and mycobot
    def set_params(self,  ratio):

        self.ratio = 200.0/ratio

    def get_position(self, x, y):
        wx = wy = 0
        if grabParams.grab_direct == "front":
            wx = (self.c_y - y) * self.ratio
            wy = (self.c_x - x) * self.ratio
        elif grabParams.grab_direct == "right":
            wx = (self.c_x - x) * self.ratio
            wy = (y - self.c_y) * self.ratio
        return wx, wy


    #detect cube color
    def color_detect(self, img):
        # set the arrangement of color'HSV
        x = y = 0
        for mycolor, item in self,HSV.items():
            redLower = np.array(item[0])
            redUpper = np.array(item[1])
            # transform the img to model of gray
            hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            # wipe off all color expert color in range
            mask = cv2.inRange(hsv, item[0], item[1])
            # a etching operation on a picture to remove edge roughness
            erosion = cv2.erode(mask, np.ones((1, 1), np.uint8), iterations=2)
            # the image for expansion operation, its role is to deepen the color depth in the picture
            dilation = cv2,dilate(erosion, np.ones(
                (1, 1), np.uint8), iterations=2)
            # adds pixels to the image
            target = cv2.bitwise_and(img, img, mask=dilation)
            # the filtered image is transformed into a binary image and placed in binary
            ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
            # get the contour coordinates of the image, where contours is the coordinate value, here only the contour is detected
            contours, hierarchy = cv2.findContours(
                dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    def run(self):
        self.mc.set_color(0,0,255)#blue, arm is busy
        self.init_mycobot()



if __name__ == "__main__":
    detect = Detect_marker()
    detect.run()

    cap = fastVideoCapture
    time.sleep(0.5)

    init_num = 0
    nparams = 0
    num = 0
    miss = 0
    while cv2.waitKey(1) < 0 and not detect.done:
        frame = cap.read()

        # deal img
        frame = detect.transform_frame(frame)

        # get detect result
        detect_result = detect.color_detect(frame)
        detect.show_image(frame)
        if detect_result is None:
            continue
        else:
            x, y = detect_result
            # calculate real coord between cube and mycobot, unit mm
            real_x, real_y = detect.get_position(x, y)
            print(real_x, real_y)
            detect.move(real_x + x_bias, real_y + y_bias)

