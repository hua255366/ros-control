#!/usr/bin/env python

from actionlib.action_client import GoalManager
import rospy 
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def send_goals_python():
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal0 = MoveBaseGoal()
    goal1 = MoveBaseGoal() 
    # goal2 = MoveBaseGoal() 
    # goal3 = MoveBaseGoal()

    goal0.target_pose.pose.position.x = 1.073
    goal0.target_pose.pose.position.y = 0.166
    goal0.target_pose.pose.orientation.z = 0.999
    goal0.target_pose.pose.orientation.w = 0.052
    
    goal1.target_pose.pose.position.x = 0.0
    goal1.target_pose.pose.position.y = 0.0
    goal1.target_pose.pose.orientation.z = 0.999
    goal1.target_pose.pose.orientation.w = 0.052
    
    # goal2.target_pose.pose.position.x = 2.41693687439
    # goal2.target_pose.pose.position.y = 1.64631867409
    # goal2.target_pose.pose.orientation.z = 0.988149484601
    # goal2.target_pose.pose.orientation.w = 0.153494612555
    
    # goal3.target_pose.pose.position.x = -0.970185279846
    # goal3.target_pose.pose.position.y = 0.453477025032
    # goal3.target_pose.pose.orientation.z = 0.946238058267
    # goal3.target_pose.pose.orientation.w = -0.323471076121
    
    # goal_lists=[goal0, goal1, goal2, goal3]      
     
    goal_number = 0
    goal0.target_pose.header.frame_id = "map"
    goal0.target_pose.header.stamp = rospy.Time.now()
    # client.send_goal(goal0)
    str_log = "Send NO. %s Goal !!!" %str(goal_number)
    rospy.loginfo(str_log)

    goal_number = 1
    goal1.target_pose.header.frame_id = "map"
    goal1.target_pose.header.stamp = rospy.Time.now()
    client.send_goal(goal1)
    str_log = "Send NO. %s Goal !!!" %str(goal_number)
    rospy.loginfo(str_log)

    wait = client.wait_for_result(rospy.Duration.from_sec(600.0))  
    if not wait:
        str_log="The NO. %s Goal Planning Failed for some reasons" %str(goal_number)
        rospy.loginfo(str_log)
    else:
        str_log="The NO. %s Goal achieved success !!!" %str(goal_number)
        rospy.loginfo(str_log)

    return "Mission Finished."

if __name__ == '__main__':
        rospy.init_node('send_goals_python',anonymous=True)    
        result = send_goals_python()
        rospy.loginfo(result)