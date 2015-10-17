#!/bin/bash
#bash script to plot histogram
#for gcarc distance statistic etc.
#
#

ps=hist.ps
data=dist.txt

#configure the figure
xlabel="Distance[deg]"
ylabel="Frequency"


pshistogram -Ba10f5:$xlabel:/a10f5:$ylabel::,%:WSne $data \
	-R10/70/0/30 -JX6i/4i -Ggray -Lthinner -Z1 -W5 -V -P > $ps


