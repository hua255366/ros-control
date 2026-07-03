#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import os, threading, time

def cmd_step1():
    os.system("python /home/robuster/catkin_ws/src/mobile_fetch/scripts/step1_mapping.py")

def run_step1():
    t = threading.Thread(target=cmd_step1,name="step1")
    t.setDaemon(True)
    t.start()

def cmd_step2():
    os.system("python /home/robuster/catkin_ws/src/mobile_fetch/scripts/step2_savemap.py")

def run_step2():
    t = threading.Thread(target=cmd_step2,name="step2")
    t.setDaemon(True)
    t.start()

def cmd_exit_mapping():
    os.system("killall -9 cartographer* rviz python")

def run_exit_mapping():
    t = threading.Thread(target=cmd_exit_mapping,name="exit_mapping")
    t.setDaemon(True)
    t.start()

def cmd_step3():
    os.system("python /home/robuster/catkin_ws/src/mobile_fetch/scripts/step3_loadmap_relocalization.py")

def run_step3():
    t = threading.Thread(target=cmd_step3,name="step3")
    t.setDaemon(True)
    t.start()

def cmd_step4():
    os.system("python /home/robuster/catkin_ws/src/mobile_fetch/scripts/step4_save_goal_1.py")

def run_step4():
    t = threading.Thread(target=cmd_step4,name="step4")
    t.setDaemon(True)
    t.start()

def cmd_step5():
    os.system("python /home/robuster/catkin_ws/src/mobile_fetch/scripts/step5_save_goal_2.py")

def run_step5():
    t = threading.Thread(target=cmd_step5,name="step5")
    t.setDaemon(True)
    t.start()

def cmd_demo1():
    os.system("python /home/robuster/catkin_ws/src/mobile_fetch/scripts/demo1_pick1_place2.py")

def run_demo1():
    t = threading.Thread(target=cmd_demo1,name="demo1")
    t.setDaemon(True)
    t.start()

layout = [
          [(sg.Text('This is the mobile fetch demo of Beetle', size=[40, 1]))],
          [sg.Output(size=(80, 20))],
          [(sg.Text('Preparation work:', size=[40, 1]))],
          [sg.Button('step1 mapping', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
           sg.Button('step2 savemap', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
           sg.Button('exit mapping or navigation', button_color=(sg.YELLOWS[0], sg.GREENS[0]))],
          [sg.Button('step3 loadmap and relocalization and navigation', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
           sg.Button('step4 save goal_1', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
           sg.Button('step5 save goal_2', button_color=(sg.YELLOWS[0], sg.BLUES[0]))],
          [(sg.Text('Mobile fetch demo:', size=[40, 1]))],
          [sg.Button('demo_1: pick from goal_1 and place to goal_2', button_color=(sg.YELLOWS[0], sg.BLUES[0])),
           sg.Button('Exit', button_color=(sg.YELLOWS[0], sg.GREENS[0]))]
         ]

window = sg.Window('SZ Robot++ Beetle', layout, default_element_size=(30, 2))

while True:
    event, value = window.read()
    if event == 'step1 mapping':
        run_step1()
        print("step1 mapping...")
    elif event == 'step2 savemap':
        run_step2()
        print("step2 savemap...")
    elif event == 'exit mapping or navigation':
        run_exit_mapping()
        print("exit mapping or navigation...")
    elif event == 'step3 loadmap and relocalization and navigation':
        run_step3()
        print("step3 loadmap and relocalization and navigation...")
    elif event == 'step4 save goal_1':
        run_step4()
        print("step4 save goal_1...")
    elif event == 'step5 save goal_2':
        run_step5()
        print("step5 save goal_2...")
    elif event == 'demo_1: pick from goal_1 and place to goal_2':
        run_demo1()
        print("demo_1: pick from goal_1 and place to goal_2...")
    else:
        run_exit_mapping()
        break
window.close()