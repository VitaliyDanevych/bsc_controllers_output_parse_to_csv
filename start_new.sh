#!/bin/sh

echo "start!"
wdir=/home/fmuser2/scripts/eric_bsc_utiliz

echo "removing old file"
cd ${wdir}
rm bsc_output.csv

echo "The script has been started to work at" `date` >> ${wdir}/script_time2.log

echo "getting data from NEs..."
#echo "starting first python module"
#start parsing license data
cd ${wdir} 
python 1_new.py

echo "The script has been finished to work at" `date` >> ${wdir}/script_time2.log
