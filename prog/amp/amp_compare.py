#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plotsection import GetStream
from wfutils import sum_traces
import pylab as pl
from sys import argv


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



    ax1 = pl.subplot(211)
    ax1.plot(t1,s1,'k')
    ax1.set_xlim(xmin=t1[0])

    ax1.locator_params(axis='y',prune='both',tight=True)
    ax1.minorticks_on()

    ax2 = pl.subplot(212)
    ax2.plot(t2,s2,'k')
    ax2.set_xlim(xmin=t2[0])
    ax2.locator_params(axis='y',prune='both',tight=True)
    ax2.minorticks_on()
    ax2.set_xlabel('Time[s]')
    
    pl.tight_layout()
    #pl.show()
    pl.savefig('amp_comp.eps',bbox_inches='tight')
