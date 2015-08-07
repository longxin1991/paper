#!/usr/bin/env python
# -*- coding: utf-8 -*-

from obspy.core.stream import Stream,read
import pylab as pl
import numpy as np
from sys import argv
import os


class PlotSection(object):

    def __init__(self,**kwargs):
        self.kwargs = kwargs
        self.stream = kwargs.get('stream')
        self.stream = self.stream.copy()
        self.sect_plot_dx = kwargs.get('plot_dx')
        self.marker = kwargs.get('marker','t2')
        self.smallaperture = kwargs.get('sa',False)
        self.margin_shrink_fac = kwargs.get('msf',3)
        self.cut = kwargs.get('tlim',())
        self.fig = pl.figure(1,figsize=(6,8))
        # Background, face and grid color.
        self.background_color = kwargs.get('bgcolor', 'w')
        self.face_color = kwargs.get('face_color', 'w')
        self.grid_color = kwargs.get('grid_color', 'black')
        self.grid_linewidth = kwargs.get('grid_linewidth', 0.5)
        self.grid_linestyle = kwargs.get('grid_linestyle', ':')
        
        self.sect_user_scale = kwargs.get('scale', 1.0)
        
        self.alpha = kwargs.get('alpha', 0.5)
        self.color = kwargs.get('color', 'k')
        # plot parameters options
        self.x_labels_size = kwargs.get('x_labels_size', 8)
        self.y_labels_size = kwargs.get('y_labels_size', 8)
        self.title_size = kwargs.get('title_size', 10)
        self.linewidth = kwargs.get('linewidth', 0.5)
        self.linestyle = kwargs.get('linestyle', '-')
        self.subplots_adjust_left = kwargs.get('subplots_adjust_left', 0.12)
        self.subplots_adjust_right = kwargs.get('subplots_adjust_right', 0.88)
        self.subplots_adjust_top = kwargs.get('subplots_adjust_top', 0.95)
        self.subplots_adjust_bottom = kwargs.get('subplots_adjust_bottom', 0.1)
        self.right_vertical_labels = kwargs.get('right_vertical_labels', False)
        self.one_tick_per_line = kwargs.get('one_tick_per_line', False)
        self.show_y_UTC_label = kwargs.get('show_y_UTC_label', True)
        self.title = kwargs.get('title', self.stream[0].id)

        #plot Ttime or not
        self.ttime = kwargs.get('ttime',True)

    def Cut(self,data, b, delta, cut):

        t1 = (cut[0] - b)/delta + 1
        t2 = (cut[1] - cut[0])/delta + t1 + 1

        return data[int(t1):int(t2)]


    def InitTraces(self):
        self.tr_num = len(self.stream)
        self.tr_b = np.empty(self.tr_num)
        self.tr_data = []
        self.tr_offsets = np.empty(self.tr_num) 

        for i,tr in enumerate(self.stream):
            self.tr_offsets[i] = tr.stats.sac.gcarc

        self.offset_min = self.tr_offsets.min()
        self.offset_max = self.tr_offsets.max()

        self.tr_offsets_norm = self.tr_offsets / self.offset_max
        self.tr_starttimes = []
        self.tr_max_count = np.empty(self.tr_num)
        self.tr_npts = np.empty(self.tr_num)
        self.tr_delta = np.empty(self.tr_num)

        self.stalst = ['']*self.tr_num
        
        for i,tr in enumerate(self.stream):
            #self.tr_starttimes.append(tr.stats.starttime)
            self.tr_max_count[i] = tr.data.max()
            self.tr_npts[i] = tr.stats.npts
            self.tr_delta[i] = tr.stats.delta
            self.tr_b[i] = tr.stats.sac.b
            self.stalst[i] = tr.stats.station
            
            if self.cut is not ():
                self.tr_data.append(self.Cut(tr.data, self.tr_b[i],self.tr_delta[i], self.cut))
            else:
                self.tr_data.append(tr.data)

        self.InitTime()

    def InitTime(self):
        self.tr_times = []

       
        if self.cut is not ():
            self.time_min = self.cut[0]
            self.time_max = self.cut[1]
            for tr in range(self.tr_num):
                npts = int((self.cut[1] - self.cut[0])/self.tr_delta[tr] + 1)
                self.tr_times.append(np.arange(npts)*self.tr_delta[tr] + self.cut[0])
        else:
            for tr in range(self.tr_num):
                self.tr_times.append(np.arange(self.tr_npts[tr])*self.tr_delta[tr]+self.tr_b[tr])
            self.time_min = np.concatenate(self.tr_times).min()
            self.time_max = np.concatenate(self.tr_times).max()

    def NormalizeTraces(self):
        self.tr_normfac = np.ones(self.tr_num)
        for tr in range(self.tr_num):
            self.tr_normfac[tr] = np.abs(self.tr_data[tr]).max()

    def InitPlot(self):
        ax = self.fig.gca()
        self.NormalizeTraces()
        
        if self.smallaperture :

            for tr in range(self.tr_num):
                self.tr_data[tr] = self.tr_data[tr]/self.tr_normfac[tr]
            temp = zip(self.stalst,self.tr_data)
            temp.sort(key=lambda x:x[0])
            
            stalst,data=zip(*temp)
            
            tl = self.time_max -self.time_min
            for tr in range(self.tr_num):
                #print len(self.tr_times[tr]),len(data[tr])
                #exit(0)
                ax.plot(self.tr_times[tr],data[tr]+tr*1.5)
                strlen=len(stalst[tr])
                ax.text(self.time_min-tl/(strlen*2.5),tr*1.5,stalst[tr],
                        horizontalalignment='left',
                        verticalalignment='center')

            ax.set_yticklabels([])
            ax.set_yticks([])
        else:
            self.ScaleTraces()
            
            for tr in range(self.tr_num):
                ax.plot(self.tr_times[tr],self.tr_data[tr]/self.tr_normfac[tr]*
                        (self.sect_scale) +
                        self.tr_offsets_norm[tr])
        return ax

    def PlotSectionSA(self,*args,**kwargs):

        self.InitTraces()

        ax = self.InitPlot()

        # Setting up line properties
        for line in ax.lines:
            line.set_linewidth(0.5)
            line.set_color('darkblue')

        if self.ttime is True:
            self.PlotTtimeLine(ax)
    
        ax.set_xlabel('Time [s]')

        ax.set_ylim(-1.5,(self.tr_num)*1.5)
        ax.set_xlim(self.time_min,self.time_max)
        #ax.figure.set_size_inches(12,8)
        #pl.savefig('sec.eps',bbox_inches='tight')
        pl.show()

    def PlotSection(self,*args,**kwargs):

        self.InitTraces()

        ax = self.InitPlot()

        # Setting up line properties
        for line in ax.lines:
            #line.set_alpha(self.alpha)
            line.set_linewidth(self.linewidth)
            line.set_color(self.color)

        if self.ttime is True:
            self.PlotTtimeLine(ax)

        ax.set_ylim(top=self.OffsetToFraction(self.offset_min-self.sect_plot_dx/self.margin_shrink_fac))
        ax.set_ylim(bottom=self.OffsetToFraction(self.offset_max+self.sect_plot_dx/self.margin_shrink_fac))

        ax.set_xlim(self.time_min,self.time_max)
         # Set up offset ticks
        tick_max, tick_min = \
            self.FractionToOffset(np.array(ax.get_ylim()))

        #Setting tick location
        if tick_min != 0.0 and self.sect_plot_dx is not None:
            tick_min += self.sect_plot_dx - (tick_min % self.sect_plot_dx)
        
        ticks = np.arange(tick_min,tick_max,self.sect_plot_dx)
        ax.set_yticks(self.OffsetToFraction(ticks))
        # Setting up tick labels
        ax.set_xlabel('Time [s]')
        ax.set_ylabel(u'Distance [°]')
        ax.set_yticklabels(ticks)

        ax.minorticks_on()
        
        #ax.grid(
        #        color=self.grid_color,
        #        linestyle=self.grid_linestyle,
        #        linewidth=self.grid_linewidth)
        #pl.savefig('sec.pdf',bbox_inches='tight')
        pl.show()

    def OffsetToFraction(self, offset):
        return offset / self.tr_offsets.max()
    
    def FractionToOffset(self, fraction):
        return fraction * self.tr_offsets.max()

    def ScaleTraces(self,scale=None):
        if scale:
            self.sect_user_scale = scale
        #self.sect_scale = self.tr_num * 1.5 * (1. / self.sect_user_scale)
        maxoffset=self.tr_offsets_norm.max()
        minoffset=self.tr_offsets_norm.min()
        self.sect_scale = (maxoffset-minoffset)*self.sect_user_scale/self.tr_num 

    def PlotTtimeLine(self,ax):
        
        if self.smallaperture is True:
            ttime = np.empty(self.tr_num)
            
            for i,tr in enumerate(self.stream):
                ttime[i] = tr.stats.sac[self.marker]
        

            tmp1=zip(self.stalst,ttime)
            tmp1.sort(key=lambda x:x[0])

            stalst,time = zip(*tmp1)
            if self.ttime:
                for i in range(self.tr_num):
                    ax.plot(time[i],1.5*i+0.5,'ro')
        else :
            mks=self.marker.split()
            #定义相位字典
            pdic = {'a':'P','t1':'PcP','t2':'PKiKP','t3':'ScS','t4':'S','t5':'ScP','t6':'pPcP'}
            #pdic = {'a':'p','t1':'PcP','t2':'PKiKP','t3':'ScS','t4':'s','t5':'ScP','t6':'pPcP'}
            for m in mks:
                ttime = np.empty(self.tr_num)
                
                for i,tr in enumerate(self.stream):
                    ttime[i] = tr.stats.sac[m]
        
                tmp1=self.tr_offsets_norm.copy()
                #tmp1.sort()
                tmp2=ttime.copy()
                tmp3=zip(tmp1,tmp2)
                tmp3.sort(key = lambda x:x[0])
                #tmp2.sort()
                tloc = tmp3[0]
                dist,time = zip(*tmp3)
                ax.plot(time,dist,'r--')
                ax.text(tloc[1], tloc[0] - 0.005, pdic[m],
                        horizontalalignment='center',fontsize=10)

def GetStream(path):

    st=Stream()
    if os.path.isfile(path) is True:
        f=open(path,'r')
        flst=f.readlines()
        
        for line in flst:
            sacfile=line.strip()
            st += read(sacfile)
    elif os.path.isdir(path) is True:
        flst = os.listdir(path)

        for item in flst:
            sacfile = os.path.join(path,item)
            st += read(sacfile)
    else :
        print("Parameter Error!")
        exit(0)

    return st

    

if __name__ == '__main__':
    
    if len(argv) !=2:
        print("usage:plotsection.py path")
        exit(0)
    else:
        path=argv[1]
        
    #f=open(path,'r')
    
    #flst=f.readlines()
    
    #st=Stream()
    
    #for line in flst:
    #    sacfile=line.strip()
    #    st += read(sacfile)
    
    st = GetStream(path)
    mks = 'a t1 t2 t3 t4 t5 t6'
    #mks = 't1 t2 t3 t5 t6'
    #section = PlotSection(stream=st,scale=4,plot_dx=0.5,msf=3,ttime=False,marker=mks)
    section = PlotSection(stream=st,sa=True,ttime=False,marker='t2',tlim=(990,1020))
    #section.PlotSection()
    section.PlotSectionSA()
