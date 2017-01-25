#!/usr/bin/python

import os
import glob
import numpy

PYM_dir = "/home/ander324/PureYangMills/simdata/"
save_dir = "/home/ander324/"
meas_dir = "/Out/"

action=0
L=8
Nt =8
operators = ["PLAQ"]

for Nc in range(10,11):
    pts = []
    for i in range(2010):
        l = 0.001*i + 0.1
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
        
        #see if the directory exists, if it doesn't make them
        if os.path.exists(sim_dir) :
            allops = []
            os.chdir(sim_dir + meas_dir)
            for op in operators:
                x = os.popen("grep {} ".format(op) + "out.*[2-9]???? | awk \'BEGIN{x=0}{x+= $2}END{print x/NR}\'").read()
                if x != '':
                    allops.append(float(x))
            if allops != []:
                pts.append([l] + allops)

        else:
            print "Nothing found at Beta = {}".format(Beta)
            
        #Make the run susy simulation run script
    print "For Nc = {}".format(Nc)
    print pts

    numpy.savetxt(save_dir+"Ops_{}.dat".format(Nc), numpy.array(pts),fmt='%1.4e')
