#!/usr/bin/python

import threading
import os
import time


class PYMThread(threading.Thread):
    def __init__ (self, binary):
        self.binary = binary
        threading.Thread.__init__(self)

    def run(self):
        print "Running " + self.binary
        os.system(self.binary)

maxThreads = 4


PYM_dir = "/home/ander324/PureYangMills/simdata/"
run_bin = "meas_PYM_metro.py 20000 100"
action=0
L=8
Nt =8

for Nc in range(10,11):
    for i in range(1500):
        l = 0.001*i + 0.701
        Beta = Nc*Nc/l

        if action == 0:
            sim_dir = PYM_dir + "WilsonAction/"
        elif action == 1:
            sim_dir = PYM_dir + "Improved/"
        else:
            print "Not setup to handle this action"
            exit()


        tag = "Beta_{}".format(Beta)
        sim_dir += "Nc{}_L{}T{}/".format(Nc,L,Nt) + tag + "/"
        sim_bin = sim_dir + run_bin

        if not os.path.exists(sim_dir):
            print "skipping {}, does not exist".format(sim_dir)
            continue
        
        #see if the directory exists, if it doesn't make them
        if os.path.exists(sim_dir) :
            flag = True

            while flag:
                if threading.active_count() <= maxThreads:
                    PYMThread(sim_bin).start()
                    flag = False
                else :
                    time.sleep(10)
        else:
            print "Nothing found at Beta = {}".format(Beta)
            
