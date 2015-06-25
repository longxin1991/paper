#!/usr/bin/env python

from obspy.core import read,Stream
from sys import argv
import numpy as np
import pylab as pl

def get_max_amp(trace,tmark,pre=10,post=10):

    ttime = trace.stats.sac[tmark]
    delta = trace.stats.delta

    tloc = ttime/delta + 1

    b = tloc - pre/delta
    e = tloc + post/delta

    seg = trace.data[b:e]
    ind = seg.argmax()

    mind = b + ind

    return mind

def plot_seg(trace,index,axes,pre=50,post=150):

    delta = trace.stats.delta
    b = index - pre/delta
    e = index + post/delta

    seg = trace.data[b:e]
    seg_norm = normlize(seg)

    npts = len(seg)

    time = np.arange(npts)
    time = time * delta - pre

    axes.plot(time,seg_norm,'k')
    axes.set_xlim(-1*pre,post)
    axes.minorticks_on()

def normlize(trace):

    maxium = trace.max()

    tr_norm = trace.copy()

    tr_norm = tr_norm/maxium

    return tr_norm


if __name__ == '__main__':

    if len(argv) != 2:
        print("usage:coda_comp.py sacfile")
        exit(0)
    else:
        path=argv[1]

    st = read(path)

    ph = ['PcP','ScP','PKiKP']

    fig, ax = pl.subplots(3,1,sharex=True)

    for i,mark in enumerate(['t1','t3','t2']):
        
        ind = get_max_amp(st[0],mark)
        plot_seg(st[0],ind,ax[i])
        ax[i].text(-15,0.5,ph[i])
        ax[i].set_ylabel('Amplitude')

    ax[2].set_xlabel('Time(s)')

    pl.show()

