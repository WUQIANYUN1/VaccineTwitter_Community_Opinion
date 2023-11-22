#!/bin/sh


tweet_user_class(){
    path=$1
    path1=$2
    d1=$3
    b=$4
    
    cat $path/WIP/uid_class_${path1}_${d1}.txt | awk '{print $1}' | uniq  |tail -n+2 > $path/WIP/u_${path1}_${d1}.txt
    #summarize number of anti/pro/neutral retweets per user
    cat $path/WIP/uid_class_${path1}_${d1}.txt | awk '{print $1,$3}' | sort | uniq -c | sed 's/  //g' > $path/WIP/temp_all.txt
    cat $path/WIP/temp_all.txt | awk '{if ($3==0) print $2,$3,$1}'> $path/WIP/temp0.txt
    cat $path/WIP/temp_all.txt | awk '{if ($3==1) print $2,$3,$1}'> $path/WIP/temp1.txt
    cat $path/WIP/temp_all.txt | awk '{if ($3==2) print $2,$3,$1}'> $path/WIP/temp2.txt
    
    
    awk 'BEGIN {FS=OFS=" "} NR==FNR{a[$1]=$3; next} {print $1, a[$1]? a[$1] : 0}' $path/WIP/temp0.txt $path/WIP/u_${path1}_${d1}.txt > $path/WIP/u_class_sum_${path1}_${d1}.txt
    cp $path/WIP/u_class_sum_${path1}_${d1}.txt $path/WIP/u_temp.txt
    awk 'BEGIN {FS=OFS=" "} NR==FNR{a[$1]=$3; next} {print $0, a[$1]? a[$1] : 0}' $path/WIP/temp1.txt $path/WIP/u_temp.txt > $path/WIP/u_class_sum_${path1}_${d1}.txt
    cp $path/WIP/u_class_sum_${path1}_${d1}.txt $path/WIP/u_temp.txt
    awk 'BEGIN {FS=OFS=" "} NR==FNR{a[$1]=$3; next} {print $0, a[$1]? a[$1] : 0}' $path/WIP/temp2.txt $path/WIP/u_temp.txt > $path/WIP/u_class_sum_${path1}_${d1}.txt
    cp $path/WIP/u_class_sum_${path1}_${d1}.txt $path/WIP/u_temp.txt
    awk '{max=$4; col=4; if ($2>max) {max=$2; col=2}; if ($3>max) {max=$3; col=3}; print $0,col-2}'  $path/WIP/u_temp.txt > $path/WIP/u_class_sum_${path1}_${d1}.txt 

    awk '{print $0,$3+$4+$5}' $path/WIP/u_class_sum_${path1}_${d1}.txt  > $path/WIP/u_class_sum_${path1}_${d1}_2.txt 
    cp $path/louv_result_w/u_com_class_r${d}_${d1}_2.csv $path/louv_result_w/temp.csv
    awk '{if($3+$4+$5>0) printf "%s %.1f\n",$0,(-$3+$5)/($3+$4+$5);else print $0,0}' $path/louv_result_w/temp.csv  > $path/louv_result_w/u_com_class_r${d}_${d1}_2.csv
}


map_opn_trt(){
    # summarize monthly user opinions: 
    
    path=$1
    path1=$2
    d1=$3
    b=$4

    echo $path,$path1,$d1,$b
    
    join -o "2.1 1.2 1.3" $path/WIP/uid_class_${path1}_${d1}.txt retweet_uid.txt > $path/WIP/uid_rtuser_class_${path1}_${d1}.txt
    cat $path/WIP/uid_rtuser_class_${path1}_${d1}.txt | awk '{print $1}' | uniq  |tail -n+2 > $path/WIP/u_rtuser_${path1}_${d1}.txt
    #summarize number of anti/pro/neutral retweets per user
    cat $path/WIP/uid_rtuser_class_${path1}_${d1}.txt | awk '{print $1,$3}' | sort | uniq -c | sed 's/  //g' > $path/WIP/temp_all.txt
    cat $path/WIP/temp_all.txt | awk '{if ($3==0) print $2,$3,$1}'> $path/WIP/temp0.txt
    cat $path/WIP/temp_all.txt | awk '{if ($3==1) print $2,$3,$1}'> $path/WIP/temp1.txt
    cat $path/WIP/temp_all.txt | awk '{if ($3==2) print $2,$3,$1}'> $path/WIP/temp2.txt
    
    
    awk 'BEGIN {FS=OFS=" "} NR==FNR{a[$1]=$3; next} {print $1, a[$1]? a[$1] : 0}' $path/WIP/temp0.txt $path/WIP/u_rtuser_${path1}_${d1}.txt > $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt
    cp $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt $path/WIP/u_temp.txt
    awk 'BEGIN {FS=OFS=" "} NR==FNR{a[$1]=$3; next} {print $0, a[$1]? a[$1] : 0}' $path/WIP/temp1.txt $path/WIP/u_temp.txt > $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt
    cp $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt $path/WIP/u_temp.txt
    awk 'BEGIN {FS=OFS=" "} NR==FNR{a[$1]=$3; next} {print $0, a[$1]? a[$1] : 0}' $path/WIP/temp2.txt $path/WIP/u_temp.txt > $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt
    cp $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt $path/WIP/u_temp.txt
    awk '{max=$4; col=4; if ($2>max) {max=$2; col=2}; if ($3>max) {max=$3; col=3}; print $0,col-2}'   $path/WIP/u_temp.txt > $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt 

    wc -l $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt 

    awk '{print $5}' $path/WIP/u_rtuser_class_sum_${path1}_${d1}.txt | sort | uniq -c | sed 's/  //g' | awk -v dat=$d1 '{print dat,$2,$1}' >> $path/date_u_rtuser_class_summary.txt
}
