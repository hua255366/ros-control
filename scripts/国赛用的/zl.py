#任务一、二路径
cd ~/LGJ
#任务三路径
cd LGJ/catkin_ws/src/mobile_fetch/scripts/
cd xunliandemo

#运行任务一
python pro_1_1.py

python task1_left_kkk.py


#运行任务二
python pro_2.py
#运行任务三
python task3_1_right.py

python task3_1_langshe_kkkkk.py
python task3_1_hongshe_kkkkk.py

#建图
python step1_mapping.py
#保存地图
python step2_savemap.py
#打开地图
python step3_loadmap_relocalization.py


#保存第一个点（中点）
！！！！！！！！！！！！！！！
！！！请问你重定位了吗！！！！
！！！！！！！！！！！！！！！
python save_goal_right_center.py

#保存第二个点（定位点）
python save_goal_right_dingwei.py
#保存第三个点（终点）
python save_goal_right_end.py


#任务二低头动作
python move_zuobiao.py