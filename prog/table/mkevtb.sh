#!/bin/bash

if [ $# -ne 1 ]
then
	echo "usage:mkevtb.sh evtlst"
	exit 0
else
	evtlst=$1
fi

#输出表头
echo "\begin{tabular}{*{3}{l}*{2}{c}*{2}{l}}"
echo "\hline"
echo "n & Date & Hour & Latitude & Longitude & Depth & Magnitude\\\\"
echo "\hline"

#
i=0

cat $evtlst|\
	while read line
	do
		i=$((i+1))
		lat=`echo $line|awk -F"|" '{print $3}'`
		lon=`echo $line|awk -F"|" '{print $4}'`
		dep=`echo $line|awk -F"|" '{print $5}'`

		temp=`echo $line|awk -F"|" '{print $9}'`
		temp=(${temp//,/ })
		mag=${temp[1]}
		datetime=(`echo $line|awk -F"|" '{print $2}'`)

		date=${datetime[0]}
		hour=`echo ${datetime[1]} | cut -b 1-10`

		echo "$i & $date & $hour & $lat & $lon & $dep & $mag\\\\"
	done

echo "\hline"
echo "\end{tabular}"
