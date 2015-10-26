#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import pylab as pl
from numpy import loadtxt

def load_data(amp_file,cols):
    pcp,pkikp,ratio = loadtxt(amp_file,usecols=cols,unpack=True)
    return pcp,pkikp,ratio

if __name__ == '__main__':
    if len(argv) < 2:
        print("usage:{0} amp_file".format(argv[0]))
        exit(0)

    f = argv[1]
    
    msize = 100
    pcp,pkikp,ratio = load_data(f,(1,2,4))
    ax1 = pl.subplot(121)
    ax1.scatter(pcp,ratio,c='w',s=msize)

    ax1.set_xscale('log')

    ax2 = pl.subplot(122)
    ax2.scatter(pkikp,ratio,c='w',s=msize)
    ax2.set_xscale('log')

    ax1.set_xlabel('PcP Amplitude')
    ax1.set_ylabel('PKiKP/PcP Amplitude Ratio')
    ax2.set_xlabel('PKiKP Amplitude')
    ax2.set_ylabel('PKiKP/PcP Amplitude Ratio')
    
    ax1.figure.set_size_inches(10,4,forward=True)
    pl.tight_layout()
    pl.subplots_adjust(wspace=0.25)
    pl.show()
    #pl.savefig('amp_cor',bbox_inches='tight')
