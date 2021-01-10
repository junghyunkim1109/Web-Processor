# Accidentally deleted, so re-writing 
# 12/3/2020 @ 0449

# CS 288 Web Processor bash script


#!/bin/bash

# Run the script for 25 times every minute
for ((i=0 ; i<25 ; ++i))
do

    # Save current date & time to be used as filename/tablename
    date=`date +"%Y_%m_%d_%H_%M_%S"`
    echo $date

    # Fetch stock page
    page='https://finance.yahoo.com/most-active'
    wget -O yahoo_${date}.html $page

    # Call python script (data_extractor.py)
    python2 data_extractor.py yahoo_${date}.html

    # Sleep for a minute
    sleep 60
done
