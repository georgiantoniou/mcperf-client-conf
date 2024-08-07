#!/bin/bash

##########################################################################################################
# This script is used as a wrapper to investigate whether single record memcached with a modified version
# of memcached can be used to investigate at which point client side overhead does not impact
# the accuracy or the trends. At which point means at which response time. As the modified version of 
#  memcached can be configured to respond after a certain time.

# Create Result Dir
ssh ganton12@node0 "mkdir ~/data/memcached-modified-single-record-iiswc-24-synthetic-bench"
cd ~/mcperf-client-conf/client-conf-scripts/

# # #### Exp1: Set Server Side single record client side Default: ####


# ## Client Side DEFAULT ##
# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-modified-single-record-iiswc-24-synthetic-bench/LP

# ## Run experiment
# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-modified-single-record-iiswc-24-synthetic-bench/LP >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#      sleep 5m

# done

#### Exp3: Set Server Side SMT ON client side C0-FG_PE-TICKS_ON-UNC_FIXED: ####

## Client Side C0-FG_PE-TICKS_ON-UNC_FIXED ##
~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0001111 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-modified-single-record-iiswc-24-synthetic-bench/HP

## Run experiment
ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-modified-single-record-iiswc-24-synthetic-bench/HP >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

     sleep 5m

done
