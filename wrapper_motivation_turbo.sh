#!/bin/bash

####################################################################################################
# This script is used as a wrapper to investigate whether performance of specific feautures of the
# server side are misinderpreted due to variabilities caused by the hardware configuration of the 
# client side. In thi script we examine Turbo/noTurbo with 2 client configurations DEFAULT and 
# C0 + governor Performance + Ticks. Total 4  experiments:
# 
# DEFAULT-S-TURBO_ON: cstates-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# DEFAULT-S-TURBO_OFF: cstates-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C0-FG_PE-TICKS_ON-UNC_FIXED-S-TURBO_ON: c0-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-fixed/core-performance/
# C0-FG_PE-TICKS_ON-UNC_FIXED-S-TURBO_OFF: c0-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-fixed/core-performance/

# Create Result Dir
ssh ganton12@node0 "mkdir ~/data/memcached-motivation-turbo"
cd ~/mcperf-client-conf/client-conf-scripts/

# #### Exp1: Set Server Side Turbo ON client side Default: ####

# ## Server TURBO ON ##
# ssh ganton12@node1 "~/mcperf-client-conf/turbo-boost.sh enable"

# ## Client Side DEFAULT ##
# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-motivation-turbo/DEFAULT-S-TURBO_ON

# ## Run experiment
# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-motivation-turbo/DEFAULT-S-TURBO_ON >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

#### Exp2: Set Server Side TURBO OFF client side Default: ####

# ## Server TURBO OFF ##
# ssh ganton12@node1 "~/mcperf-client-conf/turbo-boost.sh disable"

# ## Client Side DEFAULT ##
# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-motivation-turbo/DEFAULT-S-TURBO_OFF

# ## Run experiment
# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-motivation-turbo/DEFAULT-S-TURBO_OFF >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

#### Exp3: Set Server Side TURBO ON client side C0-FG_PE-TICKS_ON-UNC_FIXED: ####

# ## Server TURBO ON ##
# ssh ganton12@node1 "~/mcperf-client-conf/turbo-boost.sh enable"

# ## Client Side C0-FG_PE-TICKS_ON-UNC_FIXED ##
# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0001111 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-motivation-turbo/C0-FG_PE-TICKS_ON-UNC_FIXED-S-TURBO_ON

# ## Run experiment
# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-motivation-turbo/C0-FG_PE-TICKS_ON-UNC_FIXED-S-TURBO_ON >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

#### Exp4: Set Server Side TURBO OFF client side C0-FG_PE-TICKS_ON-UNC_FIXED: ####

## Server TURBO OFF ##
ssh ganton12@node1 "~/mcperf-client-conf/turbo-boost.sh disable"

## Client Side C0-FG_PE-TICKS_ON-UNC_FIXED ##
~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0001111 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-motivation-turbo/C0-FG_PE-TICKS_ON-UNC_FIXED-S-TURBO_OFF

## Run experiment
ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-motivation-turbo/C0-FG_PE-TICKS_ON-UNC_FIXED-S-TURBO_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done