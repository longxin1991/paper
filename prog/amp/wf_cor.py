#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plotsection import GetStream
from wfutils import sum_traces
import pylab as pl
from scipy.signal import resample
from numpy import arange,correlate
from sys import argv

if __name__ == '__main__':
    if len(argv) < 3:
        print("usage:{0} nv_dir pd_dir".format(argv[0]))
        exit(0)

    nv = argv[1]
    pd = argv[2]

    st1 = GetStream(nv)
    st2 = GetStream(pd)

    s1,t1 = sum_traces(st1)
    s2,t2 = sum_traces(st2)

    s3 = resample(s1,len(s2))

    lw = 3
    rw = 2
    delta = 0.05

    ind1 = s3.argmax()
    ind2 = s2.argmax()

    d1 = s3[int(ind1 - lw/delta):int(ind1 + rw/delta)+1]
    d2 = s2[int(ind2 - lw/delta):int(ind2 + rw/delta)+1]

    t = arange(-1*lw,rw+delta,delta)
    md1 = d1/d1.max()
    md2 = d2/d2.max()

    cor = correlate(md1,md2,'full')
    tc = arange(-1*(lw+rw),lw+rw+delta,delta)

    ax1 = pl.subplot(121)
    ax1.plot(t,md1,'r',alpha=0.8,label='NVAR')
    ax1.plot(t,md2,'g',alpha=0.8,label='PDAR')
    ax1.set_xlabel('Time[s]')
    ax1.legend()

    ax2 = pl.subplot(122)
    ax2.plot(tc,cor,'k')
    ax2.set_xlabel('Time[s]')
    ax2.set_xlim(-1*(lw+rw),lw+rw)

    ax1.figure.set_size_inches(12,4,forward=True)
    pl.tight_layout()
    pl.subplots_adjust(wspace=0.25)
    #pl.show()
    pl.savefig('wf_cor.eps',bbox_inches='tight')
