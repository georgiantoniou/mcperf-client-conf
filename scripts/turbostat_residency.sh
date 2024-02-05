#!/bin/bash

# **************************Need to fix this before running with turbostat
###########################################################################################
# This script takes residency measurements using the turbostat tool. It accepts as a parameter
# the interval of measurements and the number of iterations and prints the output on the screen.
#############################################################################################

##################################################
# Start measuring system C-State residency
# argument 1: Password
# argument 2: Username
# argument 3: Hostname
# argument 4: Command
##################################################
start_measurements () {
    
    sshpass -p "$1" ssh -f $2@$3 "hostname; $4 &> ./turbostat_output &"
}

##################################################
# Stop measuring system C-State residency
##################################################
stop_measurements () {
   
   sshpass -p "$1" ssh -f $2@$3 "sudo pkill turbostat"
    
}

##################################################
# Report C-State residency measurements
# argument 1: Password
# argument 2: Username
# argument 3: Hostname
##################################################
report_measurements () {

    sshpass -p "$1" ssh -f $2@$3 "cat turbostat_output;" 
    #rm turbostat_output"

}


main () {

    if [[ -z "$1" || -z "$2" || -z "$3" || -z "$4" || -z "$5" ]]; then

        echo "***ERROR: Wrong Arguments***"
        echo "***SYNTAX: ./turbostat_residency.sh iterations interval username password hostname"
        exit;   
    fi 

    iter=$1
    interval=$2
    
    username=$3
    password=$4
    host=$5

    ############################################################################################
    # Passed Flags:
    #       Interval:         Duration between measurements
    #       Num_iterations:   Number of measurements
    #       Quiet:            Do not decode and print the system configurations 
    #       Enable:           show hided build in counters like Time of Day in Seconds
    #############################################################################################
    command="sudo turbostat --interval "$interval" --num_iterations "$iter" --quiet" 
    #--enable Time_Of_Day_Seconds"   
    #echo "$command"

    start_measurements $password $username $host "$command"
    
}
"$@"