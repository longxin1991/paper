#!/usr/bin/env python

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

if __name__ == '__main__':

    print("this should not be appear.")
