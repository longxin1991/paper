#!/bin/bash
#shell script to back up data.
#2015.06.27  initiated code, longxin,igg,cas

NO_ARGS=0
E_OPTERROR=85
E_DIRERROR=1
E_FILEERROR=2


dir_exist()
{
    if [ ! -d $1 ]
    then
        echo "directory $1 not exists."
        exit $E_DIRERROR
    fi
}

file_exist()
{
    if [ ! -f $1 ]
    then
        echo "file $1 not exists."
        exit $E_FILEERROR
    fi
}

if [ $# -eq "$NO_ARGS" ]
then
    echo "Usage: `basename $0` -oorigin -ddestination AR"
    exit $E_OPTERROR
fi

while getopts ":o:d:" option
do
    case $option in 
        o   ) 
            origin=$OPTARG
            dir_exist $origin ;;
        d   )
            dest=$OPTARG
            dir_exist $dest ;;
        *   )
            echo "unknow option."
            exit E_OPTERROR ;;
    esac
done

if [[ $dest = '' ]] || [[ $origin = '' ]]
then
	echo "No destination or origin dir specified."
	exit $E_OPTERROR
fi


shift $(($OPTIND - 1))

if [ $# -eq $NO_ARGS ]
then
    echo "No array name specified."
    exit $E_OPTERROR
else
    AR=$@
fi


cd $origin

cdir=`pwd`
echo "cd to $cdir"

for array in $AR
do
    if [ -d $array ]
    then
        echo "make directory for $array"
        mkdir $dest/$array
       
        file_exist $array/save.txt

		cp $array/save.txt $dest/$array

        for event in `cat $array/save.txt`
        do
            echo "make directory for $event"
            mkdir $dest/$array/$event
            
            echo "copy mseed file."
            for mseed in $array/$event/*.mseed
            do
                echo "copy $mseed"
                cp $mseed $dest/$array/$event
            done

            if [ -d $array/resp ] && [ -d $array/meta ]
            then
                echo "copy response and statoin meta file."
                cp -rv $array/resp $dest/$array
                cp -rv $array/meta $dest/$array
            fi

            echo "copy sacfiles."
            cp -rv $array/$event/sac $dest/$array/$event

            echo "copy filtered sacfiles."
            cp -rv $array/$event/out $dest/$array/$event
        done

        echo "$array finished."
    else
        exit $E_DIRERROR
    fi

done
            
