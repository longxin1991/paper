#!/usr/bin/env python 
#########################################
#Align traces according to specific phase.
#########################################

from plotsection import GetStream
from wfutils import get_max_amp
import argparse
import numpy as np
import subprocess
import os
from fnmatch import fnmatch


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d',nargs=1,
            required=True,metavar='DIR',help='sacfile directory.')
    
    parser.add_argument('-m',nargs=1,
            required=True,metavar='MARKER',help='time marker.')


    args = parser.parse_args()

    path = args.d[0]
    marker = args.m[0]
    st = GetStream(path)

    tr_num = len(st)

    degs = np.empty(tr_num)
    atimes = np.empty(tr_num)

    for i,tr in enumerate(st) :

        degs[i] = tr.stats.sac.gcarc
        delta = tr.stats.delta
        b = tr.stats.sac.b
        atimes[i] = get_max_amp(tr,marker,0.2,0.2)*delta + b

        #print("{0:.2f}".format(atimes[i]))

    mdeg_index = atimes.argmax()
    a_master = atimes[mdeg_index]

    flst = os.listdir(path)

    for i in range(tr_num):

        shift = a_master - atimes[i]
        net = st[i].stats.network
        sta = st[i].stats.station

        pattern = net+'.'+sta+'*'

        for f in flst :
            if fnmatch(f,pattern):
                sacfile = f

        p = subprocess.Popen('sac',
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE,
                stderr=subprocess.STDOUT)

        cmd = '''
echo on
r {0}/{1}
ch allt {2:.2f}
wh
q
'''.format(path,sacfile,shift)

        sacout=p.communicate(cmd)
        print sacout[0]
