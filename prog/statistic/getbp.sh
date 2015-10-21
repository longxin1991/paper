#!/bin/bash
#
# getbp.sh [options] array_name event_array_list
#
# 给定台阵位置，和事件列表，获得指定反射相位的bounce point位置。
#
# array_name: IMS台阵名列表，如"YKA NVAR",为全部台阵生成则使用GL
# event_array_list: 事件台阵对列表，生成方法如下
#	for array in $GL
#	do
#		if [ -d $array ];then
#		for evid in `cat $array/save.txt`
#		do
#			if [ -d $array/$evid ];then
#			grep $evid $array/evtlst.txt|awk -F'|' -v a=$array\
# '{print $1,$3,$3,a}'
#			fi
#		done
#		fi
#	done
#
# Options:
#    -h|--help   显示本帮助。
#
####
#
# longxin Oct. 2015
#
PROGNAME=`type $0 | awk '{print $3}'`  # search for executable on path
PROGDIR=`dirname $PROGNAME`            # extract directory of program
PROGNAME=`basename $PROGNAME`          # base name of program
Usage() {                              # output the script comments as docs
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -n '/^###/q; /^#/!q; s/^#//; s/^ //; 3s/^/Usage: /; 2,$ p' \
		"$PROGDIR/$PROGNAME"
	exit 10;
} 

while [ $# -gt 0 ]; do
	case "$1" in
	--help|-h*) Usage ;;
	--) shift; break ;;    # end of user options
	-*) Usage "Unknown option \"$1\"" ;;
	*)  break ;;           # end of user options
	esac
	shift   # next option
done

[ $# -lt 2 ] && Usage "Too few arguments."
[ $# -gt 2 ] && Usage "Too many arguments."

array=$1
evarlst=$2
###############################
#IMS台阵location
###############################
BCAR='-141.8277 63.0617'
BMAR='-144.5271 67.4507'
IMAR='-153.7225 65.9969'
ILAR='-146.8861 64.7716'
YKA='-114.606 62.6059'

NVAR='-118.3037 38.4295'
PDAR='-109.5831 42.7765'
TXAR='-103.6669 29.3337'

ASAR='133.9508 -23.6647'
PSAR='119.8458 -21.5725'
WRA='134.3927 -19.7671'

BURAR='25.2168 47.6148'
GERES='13.7039 48.8363'
EKB='-3.1923 55.3339'

SPB='16.3906 78.1795'
ABKAR='59.9431 49.2556'
KKAR='70.5601 43.1054'
MKAR='82.3003 46.77'
##############################
GL='BURAR GERES EKB ABKAR KKAR MKAR ASAR BCAR BMAR ILAR IMAR NVAR PDAR PSAR WRA YKA SPB TXAR'

cat $evarlst|\
    while read line
    do
        line=($line)
        evtid=${line[0]}
        evla=${line[1]}
        evlo=${line[2]}
        
		ar=${line[4]}
		if [ $array = "GL" ];
		then
			pattern=`echo $GL|grep -o $ar `
		else
			pattern=`echo $array|grep -o $ar `
		fi

		if [[ $pattern != '' ]];then
			loc=(${!ar})
			stla=${loc[1]}
			stla=${loc[1]}
			stlo=${loc[0]}
    
			bp_loc=`taup_pierce -mod prem -ph PKiKP -evt $evla $evlo -sta \
$stla $stlo -turn|tail -n 1|awk  '{print $4,$5}'`
			echo "$bp_loc ${line[3]} $ar"
		fi
    done
