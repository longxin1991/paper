#!/bin/bash

if [ $# -lt 3 ]
then
	echo "usage:calradp.sh evid stla stlo [evtlst] [evcmt]"
	exit 0
else
	evid=$1
	stla=$2
	stlo=$3
	evtlst=$4
	evcmt=$5
fi

if [ -n $evtlst  ] && [ -n $evtcmt ]
then
	evtlst=evtlst.txt
	evcmt=evcmt.txt
fi

evla=`grep $evid $evtlst|awk -F"|" '{print $3}'`
evlo=`grep $evid $evtlst|awk -F"|" '{print $4}'`

cmt=`grep $evid $evcmt|awk -F"|" '{print $4}'`

dtz=(`distaz $stla $stlo $evla $evlo`)
az=${dtz[2]}

raddata=${evid}_${az}.dat
output=${evid}_${az}.ps

cmd1="radsec $cmt $az $raddata"
cmd2="plrad.sh $raddata 5.6 1.2 $output"

if [ ! -f $raddata ] 
then
	echo $cmd1
	$cmd1
fi

if [ ! -f $output ]
then
	echo $cmd2
	$cmd2
fi

gv $output
