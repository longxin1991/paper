#!/usr/bin/env python

import numpy as np

def get_max_amp(trace,tmark,pre=0.5,post=0.5):

    ttime = trace.stats.sac[tmark]
    delta = trace.stats.delta

    t1 = trace.stats.sac.b
    tloc = int((ttime - t1)/delta + 1)

    #tloc = int(ttime/delta + 1)

    b = int(tloc - pre/delta)
    e = int(tloc + post/delta)
    seg = trace.data[b:e]
    ind = seg.argmax()

    mind = b + ind

    return mind

def sum_traces(stream):
    '''
    Sum all the traces in the stream, start time of each trace should
    be the same.
    '''
    tr_num = len(stream)

    delta = stream[0].stats.delta
    b = stream[0].stats.sac.b
    npts = stream[0].stats.npts
    tr_sum = np.zeros_like(stream[0].data)
    t = np.arange(npts)*delta + b

    for tr in stream:
        tr_sum += tr.data

    tr_sum = tr_sum/tr_num

    return tr_sum,t

if __name__ == '__main__':

    print("this should not be appear.")
