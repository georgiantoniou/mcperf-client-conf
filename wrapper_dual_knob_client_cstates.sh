#!/bin/bash

####################################################################################################
# This script is used as a wrapper for the dual knob experiments of c-state we change the c-state and 
# all the other configurations one at a time.
# We assume server configuration remains the same and we just change the client configuration.
# Possible configurations are the following:
# C1E-IP_OFF: cstates-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C1E-TICKS_OFF:
# C1E-SMT_OFF:
# C1E-FG_PE:
# C1E-UNC_FIXED:
# C1E-TURBO_OFF:
# C1-IP_OFF: cstates-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C1-TICKS_OFF:
# C1-SMT_ON
# C1-FG_PE
# C1-UNC_FIXED:
# C1-TURBO_OFF:
# C0-IP_OFF: cstates-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C0-TICKS_OFF:
# C0-SMT_ON
# C0-FG_PE
# C0-UNC_FIXED:
# C0-TURBO_OFF:


ssh ganton12@node0 "mkdir ~/data/memcached-client-dual-knobs"

#### Exp1: Set C1E-IP_OFF client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 2001001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1E-IP_OFF

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1E-IP_OFF >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

# #### Exp2: Set C1E-TICKS_OFF client configuration: #### 
# cd ~/mcperf-client-conf/client-conf-scripts/

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 2111001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1E-TICKS_OFF

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1E-TICKS_OFF >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

# #### Exp3: Set C1E-SMT_OFF client configuration: #### 
# cd ~/mcperf-client-conf/client-conf-scripts/

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 2100001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1E-SMT_OFF

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1E-SMT_OFF >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

# #### Exp4: Set C1E-FG_PE client configuration: #### 
# cd ~/mcperf-client-conf/client-conf-scripts/

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 2101101 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1E-FG_PE

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1E-FG_PE >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

# #### Exp5: Set C1E-UNC_FIXED client configuration: #### 
# cd ~/mcperf-client-conf/client-conf-scripts/

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 2101011 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1E-UNC_FIXED

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1E-UNC_FIXED >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

# #### Exp6: Set C1E-TURBO_OFF client configuration: #### 
# cd ~/mcperf-client-conf/client-conf-scripts/

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 2101000 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1E-TURBO_OFF

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1E-TURBO_OFF >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

# #### Exp7: Set C1-IP_OFF client configuration: #### 
# cd ~/mcperf-client-conf/client-conf-scripts/

# ~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 1001001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1-IP_OFF

# # Run experiment

# ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1-IP_OFF >> ~/nohup.out 2>&1 &"

# sleep 105m

# while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
# do

#     sleep 5m

# done

#### Exp8: Set C1-TICKS_OFF client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 1111001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1-TICKS_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1-TICKS_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp9: Set C1-SMT_OFF client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 1100001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1-SMT_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1-SMT_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp10: Set C1-FG_PE client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 1101101 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1-FG_PE

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1-FG_PE >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp11: Set C1-UNC_FIXED client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 1101011 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1-UNC_FIXED

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1-UNC_FIXED >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp12: Set C1-TURBO_OFF client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 1101000 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C1-TURBO_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C1-TURBO_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp13: Set C0-IP_OFF client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0001001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C0-IP_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C0-IP_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp14: Set C0-TICKS_OFF client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0111001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C0-TICKS_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C0-TICKS_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp15: Set C0-SMT_OFF client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0100001 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C0-SMT_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C0-SMT_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp16: Set C0-FG_PE client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0101101 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C0-FG_PE

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C0-FG_PE >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp17: Set C0-UNC_FIXED client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0101011 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C0-UNC_FIXED

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C0-UNC_FIXED >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp18: Set C0-TURBO_OFF client configuration: #### 
cd ~/mcperf-client-conf/client-conf-scripts/

~/mcperf-client-conf/client-conf-scripts/set-client-configuration.sh main 0101000 node0,node2,node3,node4,node5 ~/mcperf-client-conf/client-conf-scripts/ node0,~/data/memcached-client-dual-knobs/C0-TURBO_OFF

# Run experiment

ssh ganton12@node0 "cd ~/mcperf-client-conf/; nohup python3 ./run_experiment.py memcached-client-dual-knobs/C0-TURBO_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done