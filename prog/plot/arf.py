#!/usr/bin/env python
#plot array response function(ARF)
#2015.05.09 by longxin at igg,cas

import numpy as np
import pylab as pl
from numpy import cos, sin, abs,exp,pi
from distaz import DistAz
from sys import argv

def cart(cla,clo,stla,stlo):
    distaz = DistAz(cla,clo,stla,stlo)
    dis=distaz.getDelta()*111.19
    baz=distaz.getBaz()

    x=1*dis*sin(baz*pi/180);
    y=1*dis*cos(baz*pi/180);

    return x,y

def stloc(stname):
    f=open(stname,'r')
    cst=f.readline().strip()
    tmp=cst.split()
    cla=float(tmp[1])
    clo=float(tmp[2])

    slst=f.readlines()

    N=len(slst)
    x=np.zeros(N)
    y=np.zeros(N)
    for i in range(N):
        item=slst[i].split()
        stla=float(item[1])
        stlo=float(item[2])
        x[i],y[i] = cart(cla,clo,stla,stlo)

    return N,x,y


def getcor(array_name):

    if array_name == 'cross' :
        N=22
        x=np.zeros(N)
        y=np.zeros(N);
        
        for i in range(N):
            if i<=10:
                x[i]=-10+i*2
            else:
                y[i]=-10+(i-11)*2;
    elif array_name == 'circle' :
        N=22
        a=np.linspace(0,2*pi,N)
        x=20*cos(a)
        y=20*sin(a)
    elif array_name == 'dcircle' :
        N=22
        a1=np.linspace(0,2*pi,16)
        xo=20*cos(a1)
        yo=20*sin(a1)

        a2=np.linspace(0,2*pi,5)+pi/6
        xi=10*cos(a2)
        yi=10*sin(a2)

        x=np.hstack((xo,xi,[0]))
        y=np.hstack((yo,yi,[0]))
    else :
        [N,x,y]=stloc(array_name)

    return N,x,y


def arf(name):
    M=100
    [N,x,y]=getcor(name)

    th=np.linspace(0,2*pi,M)
    w=1
    u=np.linspace(0,10,M)
    u=u.reshape((M,1))
    kx=w*u*sin(th)/111.19
    ky=w*u*cos(th)/111.19

    ux=5/111.19*sin(pi*225/180)
    uy=5/111.19*cos(pi*225/180)

    ux=uy=0

    A=np.zeros((M,M))

    for i in range(N):
        A=A+exp(1j*2*pi*((ux-kx)*x[i]+(uy-ky)*y[i]))

    A=abs((A-1)/(N-1))

    TH, U = np.meshgrid(th,u)

    fig, ax = pl.subplots(subplot_kw=dict(projection='polar'))
    ax.contour(TH,U,A,10,colors='k',linestyles='dashed',linewidths=0.5)
    ax.contourf(TH,U,A,10)

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    pl.show()

    return U,TH,A

if __name__ == "__main__":
    if len(argv) != 2 :
        print("usage:arf.py ArrayName")
        exit(0)
    else:
        array=argv[1]
        [U,TH,A]=arf(array)

