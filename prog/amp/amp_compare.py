#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plotsection import GetStream
from wfutils import sum_traces
import pylab as pl
from sys import argv
import numpy as np

def align_acd_maxamp(data,delta,pre=10,post=10):

    tmp = np.abs(data)
    ind = tmp.argmax()
    print("avg amp:{0:f}".format(data[ind]))
    b = int(ind - round(pre/delta))
    e = int(ind + round(post/delta))
    seg = data[b:e]
    return seg

def set_ticklabel_size(axes,size):
    for tick in axes.xaxis.get_major_ticks():
        tick.label.set_fontsize(size)
    for tick in axes.yaxis.get_major_ticks():
        tick.label.set_fontsize(size)

if __name__ == '__main__':
    if len(argv) < 3:
        print("usage:{0} pcp_dir pkikp_dir".format(argv[0]))
        exit(0)

    pcp = argv[1]
    pkikp = argv[2]

    st1 = GetStream(pcp)
    st2 = GetStream(pkikp)
    
    s1,t1 = sum_traces(st1)
    s2,t2 = sum_traces(st2)

    d1 = align_acd_maxamp(s1,t1[1]-t1[0])
    d2 = align_acd_maxamp(s2,t2[1]-t2[0])
    npts = len(d1)
    t = np.arange(npts)*(t1[1]-t1[0]) - 10.0

    ax1 = pl.subplot(211)
    ax1.plot(t,d1,'k')
    ax1.set_xlim(xmin=t[0]-0.1,xmax=t[-1]+0.1)

    ax1.locator_params(axis='y',prune='both',tight=True)
    ax1.minorticks_on()


    ax2 = pl.subplot(212)
    ax2.plot(t,d2,'k')
    ax2.set_xlim(xmin=t[0]-0.1,xmax=t[-1]+0.1)
    ax2.locator_params(axis='y',prune='both',tight=True)
    ax2.minorticks_on()
    ax2.set_xlabel('Time[s]',fontsize=20)
   
    set_ticklabel_size(ax1,16)
    set_ticklabel_size(ax2,16)

    pl.tight_layout()
    #pl.show()
    pl.savefig('amp_comp.eps',bbox_inches='tight')
