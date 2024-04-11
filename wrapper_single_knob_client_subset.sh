#!/bin/bash

####################################################################################################
# This script is used as a wrapper for the single knob experiments of the client configuration that
# appear to have great variability. 
# We assume server configuration remains the same and we just change the client configuration.
# Possible configurations are the following:
# 
# C1: c1-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C0: c0-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# INTEL_PSTATE_OFF: cstates-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-dynamic/core-ondemand/
# INTEL_PSTATE_OFF_FREQ_GOVERNOR_USERSPACE: cstates-on/intel-pstate-off/tickless-on/smt-on/turbo-on/uncore-dynamic/core-userspace/
# INTEL_PSTATE_OFF_FREQ_GOVERNOR_PERFORMANCE: cstates-on/intel-pstate-off/tickless-on/smt-on/turbo-on/uncore-dynamic/core-performance/

cd ~/mcperf-client-conf/client-conf-scripts/
ssh ganton12@node0 "mkdir ~/data/memcached-client-single-knob-variability-sleep-40"

# #### Exp3: Set C1 client configuration: #### 

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 1101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob-variability-sleep-40/C1

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob-variability-sleep-40/C1 >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

#### Exp4: Set C0 client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob-variability-sleep-40/C0

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob-variability-sleep-40/C0 >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

# #### Exp5: Set INTEL_PSTATE_OFF client configuration: #### 

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3001301 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob-variability-sleep-40/INTEL_PSTATE_OFF

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob-variability-sleep-40/INTEL_PSTATE_OFF >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done


# #### Exp10: Set INTEL_PSTATE_OFF_FREQ_GOVERNOR_USERSPACE client configuration: #### 

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3001201 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob-variability-sleep-40/INTEL_PSTATE_OFF_FREQ_GOVERNOR_USERSPACE

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob-variability-sleep-40/INTEL_PSTATE_OFF_FREQ_GOVERNOR_USERSPACE >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

# #### Exp11: Set INTEL_PSTATE_OFF_FREQ_GOVERNOR_PERFORMANCE client configuration: #### 

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3001101 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob-variability-sleep-40/INTEL_PSTATE_OFF_FREQ_GOVERNOR_PERFORMANCE

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob-variability-sleep-40/INTEL_PSTATE_OFF_FREQ_GOVERNOR_PERFORMANCE >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done