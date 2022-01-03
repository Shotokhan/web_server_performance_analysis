#!/bin/bash
if [ $# -ne 2 ] 
then
	echo "Usage: $0 <interval> <total_period>"
else
	nohup vmstat -n $1 $2 -t > vmstat_log_file.txt &
	nohup iostat -d $1 $2 sdb -o JSON -t > iostat_log_file.txt & 
fi

