import os,time

os.system("killall -9  python2")
time.sleep(0.5)

os.system("killall -9  sonor_range")
time.sleep(2)


os.system("killall -9  python && python followPersonWithSonor.py")
# os.system("python followPersonWithSonor.py")