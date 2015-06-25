#!/usr/bin/env python

from os import popen
import numpy as np
import pylab as pl

def get_travel_time(evdp,deg,mod,phase):
    cmd="taup_time -mod {0} -deg {1:f} -h {2:f} -ph {3}"
    tmp=popen(cmd.format(mod,deg,evdp,phase))
    tmp=tmp.read()
    tmp=tmp.split('\n')[5]
    time=tmp.split()[3]
    return float(time)

def calttime(path,model):

    tf = open(path,'w')

    deg = np.linspace(0,60,500)
    for i,d in enumerate(deg) :

        t2 = get_travel_time(0,d,model,'PKiKP')
        t1 = get_travel_time(0,d,model,'PcP')
        diff = t2 - t1

        tf.write('{0:.3f} {1:.3f} {2:.3f}\n'.format(t2,t1,diff))

def plotdiff():

    deg = np.linspace(0,60,500)

    d1 = np.loadtxt('ttime_prem.txt',usecols=(2,),unpack=True)
    d2 = np.loadtxt('ttime_ak135.txt',usecols=(2,),unpack=True)
    d3 = np.loadtxt('ttime_iasp91.txt',usecols=(2,),unpack=True)

    d4 = np.loadtxt('diff.txt',unpack=True)
    
    d5 = np.loadtxt('diff2.txt',unpack=True)
    d6 = np.loadtxt('diff3.txt',unpack=True)

    fig = pl.figure(1,figsize=(6,8))

    ax = fig.gca()

    ax.plot(deg,d1,label='PREM')
    ax.plot(deg,d2,label='AK135')
    ax.plot(deg,d3,label='IASP91')

    ax.plot(d4[0],d4[1],'o')
    ax.plot(d5[0],d5[1],'o')
    ax.plot(d6[0],d6[1],'o')
    
    ax.set_xlabel('Distance[$^\circ$]')
    ax.set_ylabel('Time[s]')
    
    ax.legend()
    ax.grid(True)

    pl.show()

if __name__ == '__main__' :

    plotdiff()
    exit(0)
    deg = np.linspace(0,60,500)
    
    calttime('ttime_iasp91.txt','iasp91')
    data = np.loadtxt('ttime.txt',unpack=True)
    

    line=pl.plot(deg,data[0],label='PKiKP')

    ax=line[0].axes


    ax.plot(deg,data[1],label='PcP')
    ax.plot(deg,data[2],label='PKiKP-PcP')
    
    ax.set_xlabel('Distance[$^\circ$]')
    ax.set_ylabel('Time[s]')

    ax.legend(loc=10)

    ax.grid(True)
    ax.figure.set_size_inches(6,8,forward=True)
    pl.show()
