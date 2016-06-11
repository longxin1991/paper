#!/usr/bin/env python

import pylab as pl
import numpy as np
import argparse
import matplotlib.gridspec as gridspec
from obspy.core import read,Stream
from wfutils import get_max_amp 

def get_amp(ind,data):

    return data[ind]

def set_ticklabel_size(axes,size):
    for tick in axes.xaxis.get_major_ticks():
        tick.label.set_fontsize(size)
    for tick in axes.yaxis.get_major_ticks():
        tick.label.set_fontsize(size)

def print_amp(a1,a2):

    print('{0:.3f} {1:.3f} {2:.3f}'.format(a1,a2,a1/a2))

if __name__ == '__main__':

        parser = argparse.ArgumentParser()
        parser.add_argument('-f',nargs='+',
                required=True,type=file,metavar='FILE',help='sacfile')
        parser.add_argument('-t',nargs=2,type=float,help='time span,pre=t1,post=t2')
        parser.add_argument('-m',nargs=1,metavar='Marker',help='phase marker')
        parser.add_argument('-n',action='store_true',help='Normalize the trace according to markered phase.')
        args = parser.parse_args()

        st = Stream()

        for sac in args.f:
            st += read(sac.name)
    
        t1 = args.t[0]
        t2 = args.t[1]

        m = args.m[0]
        ind1 = get_max_amp(st[0],m,0.5,0.5)
        ind2 = get_max_amp(st[1],m,0.5,0.5)

        a1 = get_amp(ind1,st[0].data)
        a2 = get_amp(ind2,st[1].data)
        
        b1 = st[0].stats.sac.b
        b2 = st[1].stats.sac.b

        dt1 = st[0].stats.delta
        dt2 = st[1].stats.delta

        s1 = ind1 - int(t1/dt1)
        e1 = ind1 + int(t2/dt1)

        s2 = ind2 - int(t1/dt2)
        e2 = ind2 + int(t2/dt2)


        d1 = st[0].data[s1:e1]
        d2 = st[1].data[s2:e2]

        hsp = 0.1
        ylm = 2
        if args.n is True:
            d1 = d1/a1
            d2 = d2/a2
            hsp = 0
        n1 = len(d1)
        n2 = len(d2)

        #fig = pl.figure(figsize=(12,3))
        fig = pl.figure(figsize=(8,6))
        gs = gridspec.GridSpec(2,1,wspace=0,hspace=hsp)

        ax1 = pl.subplot(gs[0])
        pl.plot(dt1*np.arange(n1)-t1,d1,'k')
        ax1.set_xticklabels([])
        ax1.set_xlim(-1*t1,t2)
        if args.n is True:
            ax1.set_ylim(-1*ylm,ylm)
        ylim=ax1.get_ylim()
        #ax1.text(t1/2,ylim[1]/2,'PKiKP')
        ax1.text(t2/2,ylim[1]/2,'Observation')
        
        ax2 = pl.subplot(gs[1])
        pl.plot(dt2*np.arange(n2)-t1,d2,'r')
        ax2.set_xlim(-1*t1,t2)
        if args.n is True:
            ax2.set_ylim(-1*ylm,ylm)
        ylim=ax2.get_ylim()
        ax2.text(t2/2,ylim[1]/2,'Synthetic')
        ax2.set_xlabel('Time[s]',fontsize=20)

        if args.n is True:
            ax1.set_axis_off()
            ax2.set_axis_off()
            ax2.get_xaxis().set_visible(False)
            ax2.get_yaxis().set_visible(False)
            ax1.get_yaxis().set_visible(False)
        else:
            set_ticklabel_size(ax1,16)
            set_ticklabel_size(ax2,16)
            ax1.locator_params(axis='y',prune='both',tight=True)
            ax2.locator_params(axis='y',prune='both',tight=True)
            ax1.minorticks_on()
            ax2.minorticks_on()

        print_amp(a1,a2) 
        pl.savefig('tmp.eps',bbox_inches='tight',pad_inches=0.1)
        #pl.tight_layout()
        #pl.show()

