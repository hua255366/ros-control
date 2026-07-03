#!/usr/bin/env python

import subprocess, threading
import os,signal,time
#save map
os.system("rosservice call /finish_trajectory 0")
os.system('''rosservice call /write_state "{filename: '${HOME}/Downloads/mymap.pbstream'}"''')
os.system("rosrun cartographer_ros cartographer_pbstream_to_ros_map -map_filestem=${HOME}/Downloads/mymap -pbstream_filename=${HOME}/Downloads/mymap.pbstream -resolution=0.05")

os.system("killall cartographer* rviz python")



