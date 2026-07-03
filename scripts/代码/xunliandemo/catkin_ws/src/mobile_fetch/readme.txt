//step1:
//mapping
roslaunch robuster_mr_navigation mapping.launch

//save map
rosservice call /finish_trajectory 0
rosservice call /write_state "{filename: '${HOME}/Downloads/mymap.pbstream'}"
rosrun cartographer_ros cartographer_pbstream_to_ros_map -map_filestem=${HOME}/Downloads/mymap -pbstream_filename=${HOME}/Downloads/mymap.pbstream -resolution=0.05




roslaunch robuster_mr_navigation navigation.launch