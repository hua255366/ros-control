#!/usr/bin/env python

import subprocess, threading
import os,signal
class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            print 'Thread started'
            self.process = subprocess.Popen(self.cmd, shell=True, preexec_fn=os.setsid)
            self.process.communicate()
            print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            print 'Terminating process'
            os.killpg(self.process.pid, signal.SIGTERM)
            thread.join()
        print self.process.returncode

command = Command("rosrun tf tf_echo /map /base_link")
command.run(timeout=2)


