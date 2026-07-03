#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <nav_msgs/Odometry.h>


void callback_odom(const nav_msgs::Odometry::ConstPtr& odom)
{
	// transform from "odom" to "map"
    tf::TransformListener listener;

    geometry_msgs::PoseStamped odom_pose;
    odom_pose.header = odom->header;
    odom_pose.pose = odom->pose.pose;

    geometry_msgs::PoseStamped map_pose;

    // try{
    //     listener.transformPose("map", odom_pose, map_pose);
    // }
    // catch( tf::TransformException ex)
    // {
    //     ROS_WARN("transfrom exception : %s",ex.what());
    //     return;
    // }



    tf::StampedTransform transform;
   	try
   	{
      listener.waitForTransform("base_link",
		              "odom",
		              ros::Time(0), ros::Duration(0.2));
      listener.lookupTransform("base_link", "odom",
                               ros::Time(0), transform);
    }
    catch (tf::TransformException &ex) {
      ROS_ERROR("%s",ex.what());
    }

    // ROS_INFO_STREAM(map_pose);
}
 
int main(int argc, char** argv){

	ros::init(argc, argv, "get_current_map_pose");

	 
	ros::NodeHandle n;

	ros::Subscriber odom_sub = n.subscribe("odom", 100, callback_odom);


	ros::spin();

	ROS_INFO("ok");

	 
	return 0;

}
