import threading
import os, time

def openSonor():
    os.system("roslaunch sonor_node sonor_node.launch")

t = threading.Thread(target=openSonor,name='openSonor')
t.setDaemon(True)
t.start()