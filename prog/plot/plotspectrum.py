#!/usr/bin/env python
#plot the power specturm of traces
#2015.05.14 by longxin at igg,cas

#from obspy.core import Stream,read
from plotsection import GetStream
import numpy as np
from sys import argv
import pylab as pl

class PlotSpectrum(object):

    def __init__(self,**kwargs):
        self.kwargs = kwargs
        self.stream = kwargs.get('stream')
        self.freqmax = kwargs.get('fmax',5)
        self.freqmin = kwargs.get('fmin',0)
        self.row = kwargs.get('row',4)
        self.col = kwargs.get('col',3)
        self.tr_fst = []
    
    def plotmultispec(self):

        self.__InitSpecPara()

        self.__InitFreq()

        self.__fft()
        
        self.DataSmooth()

        pfn = self.row * self.col

        pn = self.tr_num / pfn
        
        lpn = self.tr_num % pfn
        
        if lpn > 0 :
            pn += 1
        
        for i in range(pn):
            
            fig, ax = pl.subplots(self.row,self.col,sharex=True,sharey=True)
            
            for j in range(self.row):
                for k in range(self.col):
                    index = i*pfn+j*self.col+k
                    ax[j][k].set_xlim(self.freqmin,self.freqmax)
                    
                    if index < self.tr_num :
                        ax[j][k].semilogy(self.tr_freq[index],self.tr_fst_sm[index])
                        ax[j][k].grid(True)
                        if k is 0:
                            ax[j][k].set_ylabel('Spectrum')
                        if j is (self.row -1):
                            ax[j][k].set_xlabel('Frequency[Hz]')
                        ax[j][k].set_title(self.stream[index].stats.station)
                    else:
                        fig.delaxes(ax[j][k])
                    
            pl.show()

    def __fft(self):

        for tr in self.stream :
            tmp = np.fft.fft(tr)
            self.tr_fst.append(np.abs(tmp))

    def __InitSpecPara(self):
        self.tr_num = len(self.stream)
        self.tr_npts = np.empty(self.tr_num)
        self.tr_delta = np.empty(self.tr_num)

        for i,tr in enumerate(self.stream):

            self.tr_npts[i] = tr.stats.npts
            self.tr_delta[i] = tr.stats.delta

    def __InitFreq(self):

        self.tr_freq = []
        
        for i in range(self.tr_num):
            tmp = np.arange(self.tr_npts[i]) /float((self.tr_npts[i]-1) *
                    self.tr_delta[i])
            self.tr_freq.append(tmp)


    def DataSmooth(self,window=5):
        '''Function to smooth the power spectrum curve'''
        self.tr_fst_sm = []

        for i in range(self.tr_num):
            tmp = np.zeros(self.tr_npts[i])

            for k in range(int(self.tr_npts[i])):
                s=0
                if k >= window/2 and k < (self.tr_npts[i]-window/2):
                    for p in range(-window/2,window/2+1):
                        s+=self.tr_fst[i][k+p]
                    tmp[k]=s/window
                else :
                    tmp[k] = self.tr_fst[i][k]

            self.tr_fst_sm.append(tmp)


        
if __name__ == '__main__' :
    
    if len(argv) !=2:
        print("usage:plotspectrum.py path")
        exit(0)
    else:
        path=argv[1]
    
    st = GetStream(path)

    spectrum = PlotSpectrum(stream=st,fmax=4,row=3,col=3)

    spectrum.plotmultispec()
