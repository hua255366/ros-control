#encoding: UTF-8

#!/usr/bin/env python2
import rospy
from sensor_msgs.msg import Range

class SonarDistanceListener:
    def __init__(self):
        self.distance = None
        #rospy.init_node('sonor_distance_listener', anonymous=True)
        rospy.Subscriber("/sonor_range", Range, self.callback)
    
    def callback(self, data):
        self.distance = data.range
    
    def get_distance(self):
        return self.distance

def listen_for_distance():
    listener = SonarDistanceListener()
    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        if listener.distance is not None:
            return listener.distance
        rate.sleep()

if __name__ == '__main__':
    distance = listen_for_distance()
    print("Distance: {:.2f}".format(distance))