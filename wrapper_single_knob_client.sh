#!/bin/bash

####################################################################################################
# This script is used as a wrapper for the single knob experiments of the client configuration.
# We assume server configuration remains the same and we just change the client configuration.
# Possible configurations are the following:
# DEFAULT: cstates-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C1E: c1e-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C1: c1-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C0: c0-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# INTEL_PSTATE_OFF: cstates-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-dynamic/core-ondemand/
# TICKLESS_ON: cstates-on/intel-pstate-on/tickless-on/smt-on/turbo-on/uncore-dynamic/core-powersave/
# SMT_OFF: cstates-on/intel-pstate-on/tickless-off/smt-off/turbo-on/uncore-dynamic/core-powersave/
# FREQ_GOVERNOR_PERFORMANCE: cstates-on/intel-pstate-on/tickless-on/smt-on/turbo-on/uncore-dynamic/core-performance/ 
# INTEL_PSTATE_OFF_FREQ_GOVERNOR_POWERSAVE: cstates-on/intel-pstate-off/tickless-on/smt-on/turbo-on/uncore-dynamic/core-powersave/
# INTEL_PSTATE_OFF_FREQ_GOVERNOR_USERSPACE: cstates-on/intel-pstate-off/tickless-on/smt-on/turbo-on/uncore-dynamic/core-userspace/
# INTEL_PSTATE_OFF_FREQ_GOVERNOR_PERFORMANCE: cstates-on/intel-pstate-off/tickless-on/smt-on/turbo-on/uncore-dynamic/core-performance/
# UNCORE_FREQ_FIXED: cstates-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-fixed/core-powersave/
# TURBO_OFF: cstates-on/intel-pstate-on/tickless-off/smt-on/turbo-off/uncore-dynamic/core-powersave/

#### Exp1: Set DEFAULT client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/DEFAULT

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/DEFAULT >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp2: Set C1E client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 2101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/C1E

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/C1E >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp3: Set C1 client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 1101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/C1

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/C1 >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp4: Set C0 client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0101001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/C0

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/C0 >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp5: Set INTEL_PSTATE_OFF client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3001301 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/INTEL_PSTATE_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/INTEL_PSTATE_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp6: Set TICKLESS_ON client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3111001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/TICKLESS_ON

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/TICKLESS_ON >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp7: Set SMT_OFF client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3100001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/SMT_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/SMT_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp8: Set FREG_GOVERNOR_PERFORMANCE client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3101101 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/FREG_GOVERNOR_PERFORMANCE

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/FREG_GOVERNOR_PERFORMANCE >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp9: Set INTEL_PSTATE_OFF_FREQ_GOVERNOR_POWERSAVE client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3001001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/INTEL_PSTATE_OFF_FREQ_GOVERNOR_POWERSAVE

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/INTEL_PSTATE_OFF_FREQ_GOVERNOR_POWERSAVE >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp10: Set INTEL_PSTATE_OFF_FREQ_GOVERNOR_USERSPACE client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3001201 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/INTEL_PSTATE_OFF_FREQ_GOVERNOR_USERSPACE

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/INTEL_PSTATE_OFF_FREQ_GOVERNOR_USERSPACE >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp11: Set INTEL_PSTATE_OFF_FREQ_GOVERNOR_PERFORMANCE client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3001101 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/INTEL_PSTATE_OFF_FREQ_GOVERNOR_PERFORMANCE

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/INTEL_PSTATE_OFF_FREQ_GOVERNOR_PERFORMANCE >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp12: Set UNCORE_FREQ_FIXED client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3101011 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/UNCORE_FREQ_FIXED

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/UNCORE_FREQ_FIXED >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp13: Set TURBO_OFF client configuration: #### 

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 3101000 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-single-knob/TURBO_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-single-knob/TURBO_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done