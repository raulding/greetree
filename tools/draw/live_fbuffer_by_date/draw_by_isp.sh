#! /usr/bin/env bash

date=$1

isplist=('电信' '联通' '移动')
for isp in ${isplist[@]}
do
    # for LIVE
    plist=($(cat tv_live_*${isp}_${date} | awk -F"|" '{c[$3]+=$16}END{for(i in c)print i, c[i];}' | sort -k2,2 -nr | awk '{print $1}' | head -10))
    for p in ${plist[@]}
    do
	    echo "Part-2: processing for" ${isp} ${p}
        python live_qos.py ${date} ${isp}_${p} tv_live_qos_${p}_${isp}_${date}
    done
done

mkdir -p png
mv *.png png
