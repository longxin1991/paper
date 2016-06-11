#!/usr/bin/env python

from plotsection import GetStream
from wfutils import get_max_amp
from sys import argv
import numpy as np
from scipy import interpolate
import pylab as pl
import os
from distaz import DistAz

def get_takeoff_angle(evdp,deg,mod,phase):
    cmd="taup_time -mod {0} -deg {1:f} -h {2:f} -ph {3}"
    tmp=os.popen(cmd.format(mod,deg,evdp,phase))
    tmp=tmp.read()
    tmp=tmp.split('\n')[5]
    angle=tmp.split()[5]
    return float(angle)

def cmt2aki(m0):

    m1 = np.zeros((3,3))

    m1[2][2] = m0[0]
    m1[0][0] = m0[1]
    m1[1][1] = m0[2]

    m1[2][0] = m0[3]
    m1[0][2] = m0[3]

    m1[2][1] = -1*m0[4]
    m1[1][2] = m1[2][1]

    m1[0][1] = -1*m0[5]
    m1[1][0] = m1[0][1]

    return m1

def cal_rad_amp(az,i,m):
    az = az*np.pi/180
    i = i*np.pi/180
    p = np.empty(3)
    p[0] = np.sin(i)*np.cos(az)
    p[1] = np.sin(i)*np.sin(az)
    p[2] = np.cos(i)

    amp = 0

    for k in range(3):
        for l in range(3):
            amp += p[k]*m[k][l]*p[l]
    return amp

if __name__ == '__main__':

    pcp_dir = argv[1]
    pkikp_dir = argv[2]
    
    m0 = [1.81,-2.68,0.87,0.05,-1.37,1.47]
    m = cmt2aki(m0)

    st1 = GetStream(pcp_dir)
    st2 = GetStream(pkikp_dir)

    d1,a1 = np.loadtxt('pcp_prem.dat',usecols=(0,2),unpack=True)
    d2,a2 = np.loadtxt('pkikp_prem.dat',usecols=(0,2),unpack=True)

    d1 = d1[::-1]
    d2 = d2[::-1]
    a1 = a1[::-1]
    a2 = a2[::-1]

    ratio_t = a2/a1

    ratio_t = ratio_t[0:89]
    d = d1[0:89]
    tck = interpolate.splrep(d,ratio_t,s=0)
    d_t = np.linspace(1,80,200) 
    r_t = interpolate.splev(d_t,tck,der=0)
    pl.plot(d_t,r_t,'r')
    #pl.show()
    #exit(0)


    tr_num = len(st1)

    amp1 = np.empty(tr_num)
    amp2 = np.empty(tr_num)
    ratio = np.empty(tr_num)
    dist = np.empty(tr_num)
    cor = np.empty(tr_num)
    sta = [' ']*tr_num
    net = [' ']*tr_num

    for i in range(tr_num):
        m1 = get_max_amp(st1[i],'t3',pre=0.5,post=0.5)
        m2 = get_max_amp(st2[i],'t4',pre=0.5,post=0.5)

        amp1[i] = st1[i].data[m1]
        amp2[i] = st2[i].data[m2]

        ratio[i] = amp2[i]/amp1[i]

        dist[i] = st1[i].stats.sac.gcarc
        sta[i] = st1[i].stats.station
        sta2 = st2[i].stats.station
        net[i] = st1[i].stats.network
        az = st1[i].stats.sac.az
        evdp = st1[i].stats.sac.evdp
        ang1 = get_takeoff_angle(evdp,dist[i],'prem','PcP')
        ang2 = get_takeoff_angle(evdp,dist[i],'prem','PKiKP')
        
        rad1 = cal_rad_amp(az,ang1,m)
        rad2 = cal_rad_amp(az,ang2,m)
        cor[i] = rad1/rad2

        if (sta[i] != sta2):
            print("error")
        #print('{0} {1:.3f} {2:.3f}'.format(sta[i],dist[i],ratio[i]))

    r_new = interpolate.splev(dist,tck,der=0)
    for i in range(tr_num):
        print('{0} {1} {2:.3f} {3:.3f}'.format(sta[i],net[i],dist[i],cor[i]*ratio[i]-r_new[i]))

    #pl.scatter(dist,ratio-r_new)
    #pl.show()
