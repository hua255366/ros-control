#include <ros/ros.h>

#include <move_base_msgs/MoveBaseAction.h>

#include <actionlib/client/simple_action_client.h>

 
typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

 
int main(int argc, char** argv){

	ros::init(argc, argv, "simple_navigation_goals");

	if(argc > 1)
    {
        for(int i=1; i<argc; i++)
        {
            std::cout<<"argv["<<i<<"] "<<argv[i]<<std::endl;
        }
    }
	 
	//tell the action client that we want to spin a thread by default

	MoveBaseClient ac("move_base", true);

	 
	//wait for the action server to come up

	while(!ac.waitForServer(ros::Duration(5.0))){

	ROS_INFO("Waiting for the move_base action server to come up");

	}

	 
	move_base_msgs::MoveBaseGoal goal;

	 

	goal.target_pose.header.frame_id = "odom";

	goal.target_pose.header.stamp = ros::Time::now();

	 
	goal.target_pose.pose.position.x = -8.47992528454;
	goal.target_pose.pose.position.y = 4.62600193804;

	goal.target_pose.pose.orientation.z = 0.906004466162;
	goal.target_pose.pose.orientation.w = 0.419868954986;

	 
	ROS_INFO("Sending goal and waiting");

	ac.sendGoal(goal);

	 
	ac.waitForResult();

	 
	if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)

	ROS_INFO("The robot successed to reach the targe position");

	else

	ROS_INFO("The robot failed to reach the targe position for some reason");

	 
	return 0;

}