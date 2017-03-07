#!/usr/bin/python

import os
from subprocess import call


#Directory where the executable is and where the directory will be made
PYM_dir = "/home/ander324/PureYangMills/simdata/3D/"
bin_dir = "/home/ander324/PureYangMills/bin/3D/"

action=0
L=32
Nt =1
dim=3
eps=0.02
n_cor=500
n_cf=1
numRandSUN=150
UpdatesPerLink=10
numGlueOps=4
gpuid=1
u0=1.00
sqaq_run=0
xi=1
ans="y"

for Nc in range(10,11):
    for i in range(31):
#        i = i+1
        Beta = Nc*Nc/(0.1*i + 0.01)
        eps = 0.02 + i*0.01
        if i%2 :
            gpuid = 1
        else:
            gpuid = 0
        if action == 0:
            sim_dir = PYM_dir + "WilsonAction/"
        elif action == 1:
            sim_dir = PYM_dir + "Improved/"
        else:
            print "Not setup to handle this action"
            exit()
        meas_bin = bin_dir + "Nc{}/PYM_meas".format(Nc)
        sim_bin = bin_dir + "Nc{}/PYM_sim".format(Nc)

        tag = "Beta_{}".format(Beta)
        sim_dir += "Nc{}_L{}T{}/".format(Nc,L,Nt) + tag + "/"



        #see if the directory exists, if it doesn't make them
        if not os.path.exists(sim_dir) :
            print "Making Directory structure"
            os.makedirs(sim_dir + "/Out")
            os.makedirs(sim_dir + "/Meas")
            os.makedirs(sim_dir + "/Configs")
        else :
            answer = ans
            if answer.lower().startswith("y") :
                print "Ok, let's do it"
            else:
                print "Ok, getting outta here"
                sys.exit()

        os.chdir(sim_dir)

        #Make the run susy simulation run script
        f = open("run_PYM_metro.py", 'w')

        f.write('''#!/usr/bin/python

import os
import sys

if len(sys.argv) != 3 :
   print "Format is: ./run_PYM_metro.py start_config number_configs"
   exit()

startconfig = int(sys.argv[1])
number_configs = int(sys.argv[2])

sim_dir = "{}"
sim_bin = "{}"

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
'''.format(sim_dir, sim_bin, L, Nt, dim,action, Beta, eps, n_cor, n_cf, numRandSUN, UpdatesPerLink, numGlueOps, gpuid, u0, sqaq_run, xi) + '''
for config in configs:
   if config != 0:
      f = open("{}/Out/out.{}".format(sim_dir,config))
      lines = f.readlines()
      for line in lines:
         if line.find("KEEPEPS") != -1:
            eps = float(line.split()[1])
      f.close()

   f = open("parameters", 'w')
   f.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(L, L, L, Nt, dim, Beta, eps, n_cor, n_cf, numRandSUN, UpdatesPerLink, numGlueOps, gpuid, action, u0, sqaq_run, xi, sim_dir, config, config))
   f.close()

   os.system("{} > {}/Out/out.{}".format(sim_bin,sim_dir,config+n_cor))

''')

        f.close()

        #make it executable
        os.chmod(sim_dir+"/run_PYM_metro.py", 0775)
        
        
        #Make the run susy simulation run script
        f = open("meas_PYM_metro.py", 'w')
        
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

   os.system("{} > {}/Meas/meas.{}".format(meas_bin, sim_dir,config))


''')

        f.close()

        #make it executable
        os.chmod(sim_dir+"/meas_PYM_metro.py", 0775)
