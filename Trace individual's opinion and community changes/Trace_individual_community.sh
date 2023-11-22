#!/bin/sh

map_com_trt(){
    path=$1
    path1=$2
    d1=$3
    d=$4
    i=$5

    # convert com code
    awk -v ii=$i '{if ($1==ii) print $0}' $path1/node_profile3.csv > $path1/node_profile_temp.csv 
    awk 'BEGIN {FS=OFS=" "} NR==FNR{a[$2]=$4; next} {print $1,$2, a[$2]? a[$2] : 0}'   $path1/node_profile_temp.csv $path1/louv_result_w/com_${dd1}_r${d}_${d1}_adjust.csv  |sed 's/\r//g'> $path1/louv_result_w/u_com_r${d}_${d1}_adjust.csv
    cp $path1/date_u_rtuser_com_summary.txt $path/date_u_rtuser_com_temp.txt 
    awk 'BEGIN {FS=OFS=" "} NR==FNR{a[$1]=$3+1; next} {print $0, a[$1]? a[$1] : 0}' $path1/louv_result_w/u_com_r${d}_${d1}_adjust.csv $path/date_u_rtuser_com_temp.txt | awk '{$NF = $NF - 1}1'|sed 's/\r//g' > $path1/date_u_rtuser_com_summary.txt
}


md=90;
echo $md
dd1="ud_w"
path="daily_"$md
path1="daily_"$md

da='2020-01-01'
for ((i=0; i<29; i++))
    do 
    echo $d1;
    let i2=$i;   
    d1=$(date -d "$da + $i months" +'%Y-%m-%d') ; 
    d=1.0 # resolution
    map_com_trt $path $path1 $d1 $d $i
done
