#!/usr/bin/python

import os
from subprocess import call


#Directory where the executable is and where the directory will be made
PYM_dir = "/home/ander324/PureYangMills/simdata/"
bin_dir = "/home/ander324/PureYangMills/bin/"

action=0
L=8
Nt =8
dim=4
eps=0.38
n_cor=100
n_cf=1
numRandSUN=150
UpdatesPerLink=10
numGlueOps=4
gpuid=1
u0=0.797
sqaq_run=0
xi=1
ans="y"

for Nc in range(10,11):
    eps = 0.04
    for i in range(401):
#        i = i+1
        Beta = Nc*Nc/(0.001*i + 2.05)
        if i%2 :
            gpuid = 1
        else:
            gpuid = 1
        if action == 0:
            sim_dir = PYM_dir + "WilsonAction/"
        elif action == 1:
            sim_dir = PYM_dir + "Improved/"
        else:
            print "Not setup to handle this action"
            exit()
        meas_bin = bin_dir + "Nc{}/PYM_meas2".format(Nc)
        sim_bin = bin_dir + "Nc{}/PYM_sim".format(Nc)

        tag = "Beta_{}".format(Beta)
        sim_dir += "Nc{}_L{}T{}/".format(Nc,L,Nt) + tag + "/"



        #see if the directory exists, if it doesn't make them
        if not os.path.exists(sim_dir) :
            print "Skipping because does not exist, {}".format(sim_dir)
            continue
        else :
            answer = ans
            if answer.lower().startswith("y") :
                print "Ok, let's do it"
            else:
                print "Ok, getting outta here"
                sys.exit()

        os.chdir(sim_dir)
        os.makedirs(sim_dir + "/Meas2")
        
        #Make the run susy simulation run script
        f = open("meas2_PYM_metro.py", 'w')
        
        f.write('''#!/usr/bin/python

import os
import sys

if len(sys.argv) != 3 :
   print "Format is: ./run_PYM_metro.py start_config number_configs"
   exit()

startconfig = int(sys.argv[1])
number_configs = int(sys.argv[2])

sim_dir = "{}"
meas_bin = "{}"

L = {}
Nt = {}
dim = {}

action = {}
Beta = {}
eps = {}
n_cor = {}
n_cf = {}
numRandSUN = {}
UpdatesPerLink = {}
numGlueOps = {}
gpuid = {}
u0 = {}
sqaq_run = {}
xi = {}

configs = range(startconfig, startconfig + n_cor*number_configs, n_cor)

os.chdir(sim_dir)
'''.format(sim_dir, meas_bin, L, Nt, dim,action, Beta, eps, n_cor, n_cf, numRandSUN, UpdatesPerLink, numGlueOps, gpuid, u0, sqaq_run, xi) + '''
for config in configs:
   f = open("parameters", 'w')
   f.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(L, L, L, Nt, dim, Beta, eps, n_cor, n_cf, numRandSUN, UpdatesPerLink, numGlueOps, gpuid, action, u0, sqaq_run, xi, sim_dir, config, config))
   f.close()

   os.system("{} > {}/Meas2/meas.{}".format(meas_bin, sim_dir,config))


''')

        f.close()

        #make it executable
        os.chmod(sim_dir+"/meas2_PYM_metro.py", 0775)
