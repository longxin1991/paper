#!/bin/bash

data=pkikp.txt

cat $data|\
	while read line
	do
		line=($line)
		evla=${line[1]}
		evlo=${line[2]}

		sta=${line[3]}

		hd=`head ~/JWEED.dir/${sta}.stations -n 1`
		stla=`echo $hd|awk -F',' '{print $3}'`
		stlo=`echo $hd|awk -F',' '{print $4}'`

		temp=(`distaz $stla $stlo $evla $evlo`)

		echo "${temp[0]}"
	done
