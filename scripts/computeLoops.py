#!/usr/bin/python
#Author: Peter Anderson
#Date: 11-3-16
#Read in Wilson Loop data and compute averages along with std and errors

import numpy as np
import sys
import os
import subprocess
from random import uniform



#Compute the std
def sdev(data):
    g = np.asarray(data)
    return np.absolute(avg(g**2)-avg(g)**2)**0.5

#Compute the averages
def avg(data):
    return np.sum(np.transpose(data), axis=1)/len(data)
#Computes Bootstrap
def bootstrap(G):
    N_cf = len(G)
    G_bootstrap = []
    for i in range(0,N_cf):
        alpha = int(uniform(0,N_cf))
        G_bootstrap.append(G[alpha])
    return G_bootstrap

#Bootstrap all data
#returns data in the format of [[WLavg,stdev],...]
def bootstrap_WL(G,nbstrap=100): # Delta E + errors
    avgWL = avg(G)
    # avg deltaE
    bsWL = []
    for i in range(nbstrap):
        # bs copies of deltaE
        g = bootstrap(G)
        bsWL.append(avg(g))
    bsWL = np.array(bsWL)
    sdevWL = sdev(bsWL)
    data = []
    #spread of deltaE
    print "\n%2s %10s %10s" % ("WL","<WL>","error")
    print 26*"-"
    for i in range(len(avgWL)):
        print "%2d %10g %10g" % (i+1,avgWL[i],sdevWL[i])
        data.append([avgWL[i],sdevWL[i]])

    return data

#The Binning procedure to test correlation
def bin(G,binsize):
    G_binned = []
    for i in range(0,len(G),binsize):
        G_avg = 0
        for j in range(0,binsize):
            G_avg = G_avg + G[i+j]
        G_binned.append(G_avg/binsize)
    return G_binned

#Read in data from files, assumes real values of the WL are in second column
#and the imaginary part is in the third column
def readFromWLFile(filename):
    f = open(filename)
    lines = f.readlines()
    data = []
    for line in lines:
        parts = line.split()
        realWL = float(parts[1])
        data.append(realWL)
#        imagWL = float(parts[2])
#       data.append([realWL, imagWL])
    f.close()
    return np.array(data)

#Gather the Wilson Loop data
#Finds the first numLoops
#Returns WLs with error in the format of [[WLavg,stdev],...]
def getWLs(directory, numLoops):
    data = []
    os.chdir(directory)

    files = []
    for i in range(numLoops) :
        files.append("P{:03d}".format(i+1))
    for filename in files:
        subprocess.Popen('/home/ander324/SUNLatticeGauge/scripts/loopcalc.sh {}'.format(filename), shell=True).wait()

        f = open(filename)
        data.append(readFromWLFile(filename))
        f.close()
    data = np.transpose(data)
    print avg(data)
    return bootstrap_WL(data)
#    return bootstrap_WL(bin(data,5),500)
    



    
def main():
    
    # files = sys.argv[1:]
    # print files
    data = []
    files = []
    for i in range(30) :
        files.append("P{:03d}".format(i+1))
    print files
                     
    for filename in files:
        subprocess.Popen('/home/ander324/SUNLatticeGauge/scripts/loopcalc.sh {}'.format(filename), shell=True).wait()

        f = open(filename)
        #os.popen('/home/ander324/SUNLatticeGauge/scripts/loopcalc.sh {}'.format(filename)).read()

        #        subprocess.call(['/home/ander324/SUNLatticeGauge/scripts/loopcalc.sh',filename])
        data.append(readFromWLFile(filename))
        f.close()
    data = np.transpose(data)
    print avg(data)
    bootstrap_WL(data)
    bootstrap_WL(bin(data,2),200)
    bootstrap_WL(bin(data,4),400)
    bootstrap_WL(bin(data,5),500)
    bootstrap_WL(bin(data,10),1000)





def iterDirs(PYM_dir, meas_dir, save_dir, action, L, Nt, Nc, numLoops):
    pts = []
    for i in range(2500):
        l = 0.001*i + 0.1
        Beta = Nc*Nc/l

        # if l == 2.05  or l == 2.15:
        #     continue

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
        if os.path.exists(sim_dir+meas_dir) :
            print Beta, l
            allops = getWLs(sim_dir + meas_dir, numLoops)
            #flatten allops
            allops = [x for elm in allops for x in elm]
            if allops != []:
                pts.append([l] + allops)

        else:
            print "Nothing found at Beta = {}".format(Beta)
            
        #Make the run susy simulation run script
    print "For Nc = {}".format(Nc)
    print pts

    np.savetxt(save_dir+"Ops_{}.dat".format(Nc), np.array(pts),fmt='%1.4e')

    
if __name__ == "__main__" :
#    main()
    
    # t = getWLs("/home/ander324/PureYangMills/simdata/WilsonAction/Nc10_L8T8/Beta_50.0/Meas2",30)
    # print t
    
    PYM_dir = "/home/ander324/PureYangMills/simdata/"
    save_dir = "/home/ander324/"
    meas_dir = "/Meas2/"
    
    action=0
    L=8
    Nt =8
    Nc=10
    iterDirs( PYM_dir, meas_dir, save_dir,action, L, Nt, Nc, 30)

