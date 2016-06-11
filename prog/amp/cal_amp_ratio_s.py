#!/usr/bin/env python

from plotsection import GetStream
from obspy.core import read,Stream
import argparse
from wfutils import get_max_amp
from amp_res import get_takeoff_angle,cmt2aki,cal_rad_amp
from numpy import log10,loadtxt,linspace,corrcoef,arange
import numpy as np
from scipy import interpolate
from os.path import join
import pylab as pl
import shutil
from subprocess import check_output

def get_tratio(dis):

    data_path='/home/longxin/data/CN_NET/20110204'
    d1,a1 = loadtxt(join(data_path,'pcp_prem.dat'),usecols=(0,2),unpack=True)
    d2,a2 = loadtxt(join(data_path,'pkikp_prem.dat'),usecols=(0,2),unpack=True)
    d1 = d1[::-1]
    d2 = d2[::-1]
    a1 = a1[::-1]
    a2 = a2[::-1]

    ratio_t = a2/a1
    ratio_t = ratio_t[0:89]
    d = d1[0:89]
    tck = interpolate.splrep(d,ratio_t,s=0)
    r_new = interpolate.splev(dis,tck,der=0)
    return r_new

def pick_amp(tr,marker):
    data = tr.data
    delta = tr.stats.delta
    b = tr.stats.sac.b
    t_mk = tr.stats.sac[marker]
    ind = int((t_mk-b)/delta+1)
    amp = data[ind]
    #print t_mk,amp
    return amp

def cut_data(tr,ind,pre=1.0,post=1.2):
    
    delta = tr.stats.delta
    i1 = ind - int(pre/delta)
    i2 = ind + int(post/delta) + 1
    seg = tr.data[i1:i2]
    #print len(seg)
    return seg

def cal_bp_loc(stla,stlo,evla,evlo):

    cmd = "taup_pierce -mod prem -ph PcP -evt {0:.4f} {1:.4f} -sta {2:.4f} {3:.4f} -turn|tail -n 1|awk '{{print $4,$5}}'".format(stla,stlo,evla,evlo)
    loc = check_output(cmd,shell=True)
    return loc

def snr(tr,ind,window=10.0,pre=5.0,post=5.0):

    delta = tr.stats.delta
    w1 = ind - int((pre+window)/delta)
    w2 = ind - int(pre/delta)
    w3 = ind + int(pre/delta)
    w4 = ind + int((pre+window)/delta)
    
    pre_seg = np.abs(tr.data[w1:w2])
    post_seg = np.abs(tr.data[w3:w4])

    signal = np.abs(tr.data[ind])
    n1 = pre_seg.max()
    n2 = post_seg.max()

    if n1 > n2:
        noise = n1
    else:
        noise = n2

    r = signal/noise

    return r

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',nargs='+',
            required=True,type=file,metavar='FILE',help='sacfile')

    args = parser.parse_args()

    st = Stream()
    flist = []
    for sac in args.f:
        st += read(sac.name)
        flist.append(sac.name)

    #m0 = [-1.27,0.54,0.73,-0.24,-0.95,0.52]
    #m0 = [1.81,-2.68,0.87,0.05,-1.37,1.47]
    m0 = [0.42,-0.69,0.27,-0.43,-0.28,0.38]
    m = cmt2aki(m0)
    evdp = st[0].stats.sac.evdp
    evla = st[0].stats.sac.evla
    evlo = st[0].stats.sac.evlo

    for i,tr in enumerate(st):
        m1 = get_max_amp(tr,'t3',pre=0.25,post=0.25)
        m2 = get_max_amp(tr,'t4',pre=0.25,post=0.25)

        #estimate SNR of PcP and PKiKP
        snr1 = snr(tr,m1,10,5,5)
        snr2 = snr(tr,m2,5,5,5)

        if snr1 > 2.5 and snr2 > 2.5:
            s = 1
            rsnr = snr2/snr1
        else:
            s = 0

        a1 = tr.data[m1]
        a2 = tr.data[m2]
        s1 = cut_data(tr,m1)
        n1 = s1.max()
        s2 = cut_data(tr,m2)
        n2 = s2.max()
        R = corrcoef(s1/n1,s2/n2)
        cor = R[0][1]
        npts = len(s1)
        delta = tr.stats.delta
        t0 = tr.stats.sac.b
        #Time res
        t1 = tr.stats.sac.t1
        t3 = m1*delta + t0 
        t2 = tr.stats.sac.t2
        t4 = m2*delta + t0
        t_res = t4 - t3 - t2 + t1

        #########
        r = a2/a1
        sta = tr.stats.station
        stla = tr.stats.sac.stla
        stlo = tr.stats.sac.stlo
        dis = tr.stats.sac.gcarc
        az = tr.stats.sac.az
        t = arange(npts)*delta-1.0

        ang1 = get_takeoff_angle(evdp,dis,'prem','PcP')
        ang2 = get_takeoff_angle(evdp,dis,'prem','PKiKP')
        rad1 = cal_rad_amp(az,ang1,m)
        rad2 = cal_rad_amp(az,ang2,m)
        rad_corr = rad1/rad2

        r_n = get_tratio(dis)
        res = log10(r*rad_corr/r_n)

        if cor > 0.90 and s == 1 :
            #print('{0} {1:.3f} {2:.3f} {3:.3f} {4:.3f} {5:.3f} {6:.3f}'.format(sta,dis,a1,a2,r,res,cor))
            #loc = cal_bp_loc(stla,stlo,52.222,151.515)
            loc = cal_bp_loc(stla,stlo,evla,evlo)
            loc = loc.strip()
            loc = loc.split(' ')
            lat = loc[0]
            lon = loc[1]
            print('{0} {1} {2:.4f} {3:.4f} {4:.4f} {5:.2f} {6:.3f} {7:.3f}'.format(lat,lon,res,r*rad_corr,dis,t_res,snr1,snr2))
            print sta
            #print('{0:.3f} {1:.3f} {2:.3f}'.format(rad_corr,ang1,ang2))
            #shutil.copy(flist[i],'A')
            #print('PcP: {0:.3f} PKiKP: {1:.3f}'.format(snr1,snr2))
            pl.plot(t,s1/n1,'b')
            pl.plot(t,s2/n2,'r')
            pl.xlim(t[0],t[-1])
            pl.text(0.6*t[-1],0.7,sta)
            pl.text(0.65*t[-1],0.6,'cor: {0:.4f}'.format(cor))
            pl.text(0.3*t[-1],0.6,'ratio: {0:.4f}'.format(r))
            pl.text(0.3*t[-1],0.5,'snr1 {0:.3f}  snr2: {0:.3f}'.format(snr1,snr2))
            pl.xlabel('Time[s]')
            pl.minorticks_on()
            pl.show()
        #break
        continue
        #a1 = pick_amp(tr,'t3')
        #a2 = pick_amp(tr,'t4')
    #exit(0)
    #d_t = linspace(1,80,500)
    #r_t = get_tratio(d_t)
    #pl.plot(d_t,r_t)
    #pl.show()
    #for i in range(500):
    #    print d_t[i],r_t[i]
