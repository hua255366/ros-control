#!/usr/bin/env python
# coding: utf-8
from pymycobot.mycobot import MyCobot
from actionlib.action_client import GoalManager
import rospy
from geometry_msgs.msg import Twist
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import re
import os
import glob  
import test_lzm
from move_control import movement
import time
import dnn_grab_2

def send_goal(goal_number, goal):
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    client.send_goal(goal)
    str_log = "Send NO. %s Goal !!!" %str(goal_number)
    rospy.loginfo(str_log)

    wait = client.wait_for_result(rospy.Duration.from_sec(60.0))  
    if not wait:
        str_log="The NO. %s Goal Planning Failed for some reasons" %str(goal_number)
        rospy.loginfo(str_log)
    else:
        str_log="The NO. %s Goal achieved success !!!" %str(goal_number)
        rospy.loginfo(str_log)

def read_goal(filename):
    goal = MoveBaseGoal() 

    file_to_read = open(filename)
    index = 0
    for line in file_to_read.readlines():
        line = line.strip()
        index += 1
        if index == 2:
            pattern = re.compile(r"(?<=\[).*?(?=\])")
            query = pattern.search(line)
            listFromLine = query.group().split(',')
            goal.target_pose.pose.position.x = float(listFromLine[0])
            goal.target_pose.pose.position.y = float(listFromLine[1])
        if index == 3:
            pattern = re.compile(r"(?<=\[).*?(?=\])")
            query = pattern.search(line)
            listFromLine = query.group().split(',')
            goal.target_pose.pose.orientation.z = float(listFromLine[2])
            goal.target_pose.pose.orientation.w = float(listFromLine[3])


    print(goal.target_pose.pose)
    
    return goal



def backward():
    print("backward...")
    move_cmd = Twist()
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

    count = 20
    rate = rospy.Rate(count) # 20hz      


    while count > 0:
        move_cmd.linear.x = -0.2
        pub.publish(move_cmd)
        rate.sleep()
        print("backward...")
        count -= 1

def moblie_fetch_demo():
    #goal_1 = read_goal("goal_1.txt")
    #goal_2 = read_goal("goal_2.txt")
    #goal_3 = read_goal("goal_3.txt")
    goal_files = glob.glob('goal*.txt')
    num_files = len(goal_files)
    # 循环从1到max_num 
    
    for i in range(1, num_files + 1):  
	if(i==4):
		#mc=MyCobot('/dev/arm',115200)
		#mc.send_coords([67.6,96.5,375.6,(-99.76),(-43.07),4.24],25,0)
		time.sleep(3)
		
		for mo in range(1,7) :
			
			m=movement()
			m.moveforward(1)
			time.sleep(0.3)
			rospy.Subscriber('nav_ck', String, CKcallback)







		rospy.loginfo("ready to trige")
        	#rospy.spin()
        #filename = f"goal_{i}.txt"    
        goal = read_goal("goal_%d.txt" % i)
        goal_number = i 
        send_goal(goal_number,goal)
    #goal_number = 1
    #send_goal(goal_number,goal_1)



    #goal_number = 2
    #send_goal(goal_number,goal_2)


    #goal_number = 3
    #send_goal(goal_number,goal_3)



 



    return "Mission Finished."
rospy.init_node('navigation')
if __name__ == '__main__':
        rospy.init_node('send_goals_python',anonymous=True)    
        result = moblie_fetch_demo()
        rospy.loginfo(result)
