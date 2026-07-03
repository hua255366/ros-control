#encoding: UTF-8
#!/usr/bin/env python2

from movement import Movement

import rospy
from sensor_msgs.msg import Range

class Sonor(object):

    def __init__(self):
        super(Sonor, self).__init__()
        self.data = rospy.wait_for_message('sonor_range',Range)
    # 获取超声波数据    
    def get_sonor_data(self):
        # data = rospy.wait_for_message('sonor_range',Range)
        distance = self.data.range
        # print(distance)
        return distance

    def sonor_control_goal_1(self):
        distance = self.get_sonor_data()

        if distance > 0.30:   # default: 0.31 0.34
            Movement().moveforward(0.05, 0.3)
        elif distance < 0.28: # default: 0.27 0.31
            Movement().moveback(0.05, 0.3)
        else:
            Movement().stop()

    def sonor_control_goal_2(self):
        distance = self.get_sonor_data()

        if distance > 0.66:
            Movement().moveforward(0.05, 0.3)
        elif distance < 0.64:
            Movement().moveback(0.05, 0.3)
        else:
            Movement().stop()
        
    def sonor_control_goal_3(self):
        distance = self.get_sonor_data()

        if distance > 0.24:
            Movement().moveforward(0.05, 0.3)
        elif distance < 0.21:
            Movement().moveback(0.05, 0.3)
        else:
            Movement().stop()

    def sonor_control_goal_4(self):
        distance = self.get_sonor_data()

        if distance > 0.20:
            Movement().moveforward(0.05, 0.5)
        elif distance < 0.18:
            Movement().moveback(0.05, 0.5)
        else:
            Movement().stop()

    def sonor_control_goal_5(self):
            distance = self.get_sonor_data()

            if distance > 0.58: #60，0.56
                Movement().moveforward(0.03, 0.5)#0.05,0.3
            elif distance < 0.56: #58，0.54
                Movement().moveback(0.03, 0.5)
            else:
                Movement().stop()