#!/usr/bin/env python

import sys
import numpy as np
from numpy import float32,fromfile
import pylab as pl

sbin=sys.argv[1]

ar=fromfile(sbin,float32)

ar=ar.reshape((100,3001))

ax=pl.imshow(ar,extent=[930,960,2,-2],aspect='auto')

pl.show()


