#!/usr/bin/python
#Author: Peter Anderson
#Date: 5-17-15
# This is a script to setup the directory structure of my simulations
#Second time having to make this =(


import os
import sys



#Directory where the executable is and where the directory will be made
PYM_dir = "/home/ander324/PureYangMills/simdata/"
bin_dir = "/home/ander324/PureYangMills/bin/"


Nc = int(raw_input("Enter the number of colors: "))
action = int(raw_input("Enter the version of action, 0(Wilson) 1(Improved) 2(AnisoImproved) : "))
L = int(raw_input("Enter the number of spatial nodes: "))
Nt = int(raw_input("Enter the number of temporal nodes: "))
dim = int(raw_input("Enter the number of dimensions: "))
Beta = float(raw_input("Enter the size of Beta: "))
eps = float(raw_input("Enter the size of the epsilon factor for Metro Algorithm: "))
n_cor = int(raw_input("Enter the number updates before saving: "))
n_cf = int(raw_input("Enter the number of configurations: "))
numRandSUN = int(raw_input("Enter the number of random matrices used: "))
UpdatesPerLink = int(raw_input("Enter the number of Updates for each link: "))
numGlueOps = int(raw_input("Enter the number of glueball operators: "))
gpuid = int(raw_input("Enter which GPU to be used (0 or 1): "))
u0 = float(raw_input("Enter the expectation value for the link: "))
sqaq_run = int(raw_input("Calculate SQAQ potential (0 no, 1 yes): "))
xi = float(raw_input("Enter the anisotropy ratio: "))

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
    answer = str(raw_input("It looks like the directory structure is already set up, overwrite the run scripts? (y/n)"))
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
   f = open("parameters", 'w')
   f.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(L, L, L, Nt, dim, Beta, eps, n_cor, n_cf, numRandSUN, UpdatesPerLink, numGlueOps, gpuid, action, u0, sqaq_run, xi, sim_dir, config, config))
   f.close()

   os.system("{} > {}/Out/out.{}".format(sim_bin,sim_dir,config+n_cor))
   f = open("{}/Out/out.{}".format(sim_dir,config+n_cor))
   lines = f.readlines()
   for line in lines:
      if line.find("KEEPEPS") != -1:
         eps = float(line.split()[1])
   f.close()

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


