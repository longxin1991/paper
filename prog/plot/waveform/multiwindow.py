#!/usr/bin/env python

import pylab as pl
import numpy as np
import matplotlib.gridspec as gridspec
import argparse
from obspy.core import read,Stream

class MultiWindow(object):

    def __init__(self,stream,**kwargs):
        self.stream = stream
        self.kwargs = kwargs

        self.normalize = kwargs.get('norm',False)
        self.log = kwargs.get('log',False)

    def InitTrace(self):
        self.tr_num = len(self.stream)
        self.tr_data = []
        self.tr_npts = np.empty(self.tr_num)
        self.tr_delta = np.empty(self.tr_num)
        self.tr_b = np.empty(self.tr_num)
        self.tr_normfac = np.empty(self.tr_num)
        
        for i,tr in enumerate(self.stream):

            self.tr_data.append(tr.data)
            self.tr_npts[i] = tr.stats.npts
            self.tr_delta[i] = tr.stats.delta
            self.tr_b[i] = tr.stats.sac.b

        self.InitTime()
    
    def InitTime(self):
        self.tr_times = []

        for tr in range(self.tr_num):
            self.tr_times.append(np.arange(self.tr_npts[tr])*self.tr_delta[tr]+self.tr_b[tr])

        self.time_min = np.concatenate(self.tr_times).min()
        self.time_max = np.concatenate(self.tr_times).max()

    def NormalizeTraces(self):
        self.tr_normfac = np.ones(self.tr_num)
        for tr in range(self.tr_num):
            self.tr_normfac[tr] = np.abs(self.tr_data[tr]).max()
   
    def PlotInfo(self,ax,tr):
        otime = tr.stats.starttime
        info = otime.strftime('%Y/%m/%d %H:%M:%S')
        b = tr.stats.sac.b
        e = tr.stats.sac.e
        ax.set_ylim(top=2)
        ax.text(b+(e-b)/2,1,info)

    def InitPlot(self):
        fig = pl.gcf()
        #fig.set_size_inches(6,4)
        fig.set_size_inches(8,4)
        self.axs = []
        gs = gridspec.GridSpec(self.tr_num,1,wspace=0,hspace=0)
        
        self.NormalizeTraces()
        for i in range(self.tr_num):
            ax = pl.subplot(gs[i])
            self.axs.append(ax)


            if self.normalize:
                if self.log is True:
                    ax.semilogy(self.tr_times[i],self.tr_data[i]/self.tr_normfac[i],'k')
                else:
                    ax.plot(self.tr_times[i],self.tr_data[i]/self.tr_normfac[i],'k')
            else:
                ax.plot(self.tr_times[i],self.tr_data[i],'k')

            #if self.tr_num is 1:
            #    self.PlotInfo(ax,self.stream[0])
            ax.set_xlim(self.time_min,self.time_max)
            
            ax.locator_params(axis='y',nbins=6,prune='both')
            ax.minorticks_on()


            if i is not  (self.tr_num-1): 
                ax.set_xticklabels([])
            #ax.set_yticklabels([])

            if i is (self.tr_num -1):
                ax.set_xlabel('Time [s]')
        pl.savefig('mul.eps',bbox_inches='tight')
        #pl.show()

    def plotmultiwindow(self):
        self.InitTrace()

        self.InitPlot()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',nargs='+',
            required=True,type=file,metavar='FILE',help='sacfile')
    parser.add_argument('-d',nargs='+',help='sacfile directory.')
    args = parser.parse_args()

    st = Stream()

    for sac in args.f :
        st += read(sac.name)

    multiwin=MultiWindow(st,norm=True)

    multiwin.plotmultiwindow()
