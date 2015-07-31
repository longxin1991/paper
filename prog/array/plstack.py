#!/usr/bin/env python
#plot vespgram after stacking,datafile and infofile need to be
#provided..
#2015.05.04 by longxin
#2015.05.07 add marker of theoretical value and using different
#color map is available.

import sys
import numpy as np
from numpy import float32,fromfile
import pylab as pl
from matplotlib import gridspec,ticker
from string import atof,atoi

if len(sys.argv) != 3:
    print("usage:plstack.py datafile infofile.")
    exit(0)
else:
    sbin=sys.argv[1]
    info=sys.argv[2]

f=open(info,'r')

l1=f.readline().strip()
l2=f.readline().strip()
l3=f.readline().strip()

lim=l1.split()
dim=l2.split()
the=l3.split()

print("station number: {0:d}".format(atoi(dim[0])))

ar=fromfile(sbin,float32)
ar1=fromfile(sbin+'_wf',float32)

#find index of max value.
i=ar.argmax()
#ix=i%atoi(dim[1])
iy=i/atoi(dim[1])
print("max row: {0:d}".format(iy))

ar=ar.reshape(200,atoi(dim[1]))
ar1=ar1.reshape(200,atoi(dim[1]))


#perform the plotting.
gs=gridspec.GridSpec(2,1,height_ratios=[1,4])
#ax=pl.imshow(ar,extent=[atof(lim[0]),atof(lim[1]),atof(lim[3]),atof(lim[2])],aspect='auto')
t=np.linspace(atof(lim[0]),atof(lim[1]),atoi(dim[1]))
ax1=pl.subplot(gs[0])
ax1.plot(t,ar1[iy],'k')
ax1.ticklabel_format(axis='y',style='sci',scilimits=(-1,1));
ax1.locator_params(axis='y',nbins=6)

ax2=pl.subplot(gs[1])
ax2.imshow(ar,extent=[atof(lim[0]),atof(lim[1]),atof(lim[3]),atof(lim[2])],aspect='auto')
ax2.set_xlabel('Time(s)')
ax2.set_ylabel('Slowness(s/deg)')

#cb=ax2.figure.colorbar(ax2.images[0],orientation='horizontal',shrink=0.5,extend='both')
#cb.formatter.set_powerlimits((0,0))
#cb.update_ticks()


#mark theoretical slowness and arrival time.
if len(the)!=0:
    t2=atof(the[0])
    p=atof(the[1])
    print t2,p
    ax2.plot(t2,p,marker='o',alpha=0.8,markerfacecolor='w',markersize=10.0)

#pl.set_cmap('bwr')
pl.savefig("vesp.eps",bbox_inches='tight')
#pl.show()
