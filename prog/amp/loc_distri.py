#!/usr/bin/env python
# -*- coding: utf-8 -*-
#plot global distribution of bounce points and earthquakes
#which are marked according whether PcP and PKiKP are both
#observed.

import argparse
from sys import argv
import pylab as pl
from numpy import loadtxt
from mpl_toolkits.basemap import Basemap

def load_data(loc_file,cols):
    lat,lon,mark = loadtxt(loc_file,usecols=cols,unpack=True)
    return lat,lon,mark

def plot_loc(gmap,x,y,flag,ma):
    locs=zip(x,y,flag)
    for p in locs:
        if p[2] == 1:
            gmap.plot(p[0],p[1],'r',marker=ma)
        else:
            gmap.plot(p[0],p[1],'b',marker=ma)

if __name__ == '__main__':
    if len(argv) < 3:
        print("usage:{0} loc_file1 loc_file2".format(argv[0]))
        exit(0)

    f1 = argv[1]
    f2 = argv[2]

    lat1,lon1,flag1 = load_data(f1,(1,2,3))
    lat2,lon2,flag2 = load_data(f2,(0,1,2))
    
    ax1 = pl.subplot(121)
    map1 = Basemap(projection='hammer',lon_0=180,resolution='l')
    map1.drawcoastlines()
    x1,y1 = map1(lon1,lat1)
    plot_loc(map1,x1,y1,flag1,'*')

    ax2 = pl.subplot(122)
    map2 = Basemap(projection='hammer',lon_0=180,resolution='l')
    map2.drawcoastlines()
    x2,y2 = map2(lon2,lat2)

    plot_loc(map2,x2,y2,flag2,'o')

    ax1.figure.set_size_inches(10,4,forward=True)
    pl.tight_layout()
    #pl.show()
    pl.savefig("loc_distri.eps",bbox_inches="tight")
