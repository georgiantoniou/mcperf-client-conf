import os
import pandas as pd
import json
import statistics
import csv 

# Set the parent directory where experiment directories are located
parent_directory = "/home/ganton12/data/mcperf_data/memcached-c6-wall-ilo-hints-interrupts-rapl-mpstat-raplperf-turbostat-socwatch-workerthread-1"

overall_transitions = {}
overall_residency = {}
overall_rapl = {}
overall_interrupts = {}
overall_perf_rapl = {}
overall_mpstat = {}
overall_queries = {}
overall_response_time = {}
overall_residency_soc = {}

avg_rapl = {}
avg_residency = {}
avg_transitions = {}
avg_interrupts = {}
avg_perf_rapl = {}
avg_mpstat = {}
avg_queries = {}
avg_response_time  = {}
avg_residency_soc = {}

temp_name = ""

# Iterate through subdirectories
for directory_name in os.listdir(parent_directory):
    directory_path = os.path.join(parent_directory, directory_name)
    
    # check if name is directory
    if not os.path.isdir(directory_path):
        continue

    #check if profiler output is in directory
    # check if name is directory
    profiler_path = os.path.join(directory_path, "memcached")
    if not os.path.isdir(profiler_path):
        continue

    temp_name=directory_name
    # Initialize an empty dictionary to store residency, transitions and power measurements
    run_transitions = {}
    run_residency = {}
    run_rapl = {}

    run_mpstat = {}
    run_interrupts = {}
    run_queries = {}
    run_response_time = {}
    run_residency_soc = {}

    # Process each file in the experiment directory
    for j in range(0, 1):
        profiler_files = directory_path  + "/memcached"
        
        mcperf_file = directory_path + "/mcperf"

        socwatch_file = directory_path + "/memcachedserversocwatch"

        
        if not os.path.isfile(mcperf_file):
            continue

    
        #extract queries and response time and 99th tail latency
        run_response_time['avg'] = []
        run_response_time['99th'] = []
        run_queries['qps'] = []
        with open(mcperf_file, 'r') as f:
            for line in f:
                
                if "read" in line:
                    run_response_time['avg'].append(float(line.split()[1]))
                    run_response_time['99th'].append(float(line.split()[13]))
                if "Total QPS" in line:
                    run_queries['qps'].append(float(line.split()[3]))
        header = []
        #extract socwatch hardware core c-state residency from it'summary file
        with open(socwatch_file, 'r') as f:
            for line in f:
                if "Core C-State Summary: Residency (Percentage and Time)" in line:
                    header  = next(f).split(",")
                    continue
                if "---" in line:
                    continue
                if header:
                    run_residency_soc[line.split(",")[0].strip()] = {}
                    for i in range(1,41):
                        run_residency_soc[line.split(",")[0].strip()]["CPU" + str(i-1)] = []
                        run_residency_soc[line.split(",")[0].strip()]["CPU" + str(i-1)].append(float(line.split(",")[i].strip()))
                    if "CC6" in line.split(",")[0]:
                        break
       
        # Put file contents into a dictionary
        for profiler_file in os.listdir(profiler_files):
            prev_time, prev_meas = 0, 0
            cur_time, cur_meas = 0, 0
            with open(profiler_files + "/" + profiler_file, 'r') as file:
                
                header = next(file) 
                
                for line in file:
                    cur_time = line.split(',')[0]
                    cur_meas = line.split(',')[1]

                    if prev_time != 0:
                        break

                    prev_time = line.split(',')[0]
                    prev_meas = line.split(',')[1]

            # if it is a residency
            if profiler_file.startswith("CPU") and (profiler_file.endswith(".time")):
                CPU = profiler_file.split('.')[0]
                state = profiler_file.split('.')[1]
                
                if CPU in run_residency:
                    if state in run_residency[CPU]:
                        print(profiler_files)
                        print(CPU)
                        print(state)
                        run_residency[CPU][state].append((int(cur_meas)-int(prev_meas))/((int(cur_time)-int(prev_time))*1000000)) 
                    else:
                        run_residency[CPU][state] = []
                        run_residency[CPU][state].append((int(cur_meas)-int(prev_meas))/((int(cur_time)-int(prev_time))*1000000))
                else:
                    run_residency[CPU] = {}
                    run_residency[CPU][state] = []
                    run_residency[CPU][state].append((int(cur_meas)-int(prev_meas))/((int(cur_time)-int(prev_time))*1000000))
            # if it is a transition file
            elif profiler_file.startswith("CPU") and (profiler_file.endswith(".usage")):
                CPU = profiler_file.split('.')[0]
                state = profiler_file.split('.')[1]
                if CPU in run_transitions:
                    if state in run_transitions[CPU]:
                        run_transitions[CPU][state].append((int(cur_meas)-int(prev_meas)))
                    else:
                        run_transitions[CPU][state] = []
                        run_transitions[CPU][state].append((int(cur_meas)-int(prev_meas)))
                else:
                    run_transitions[CPU] = {}
                    run_transitions[CPU][state] = []
                    run_transitions[CPU][state].append((int(cur_meas)-int(prev_meas)))
            # if it is an interrupt file
            elif profiler_file.startswith("INTR"):
                intr_type = profiler_file.split('.')[1]
                run_interrupts[intr_type] = {}
                intr_before = prev_meas.split()
                intr_after = cur_meas.split()
                for i in range(0,len(intr_before)):
                    run_interrupts[intr_type]["CPU" + str(i)]= int(intr_after[i]) - int(intr_before[i])
            # if it is a rapl file
            elif "package-0" in profiler_file or "package-1" in profiler_file :
                if "package-0" in profiler_file:
                    if "package-0" in run_rapl:
                        run_rapl['package-0'].append((int(cur_meas)-int(prev_meas))/(int(cur_time)-int(prev_time))/1000000)
                    else:
                        run_rapl['package-0'] = []
                        run_rapl['package-0'].append((int(cur_meas)-int(prev_meas))/(int(cur_time)-int(prev_time))/1000000)
                elif "package-1" in profiler_file:
                    if "package-1" in run_rapl:
                        run_rapl['package-1'].append((int(cur_meas)-int(prev_meas))/(int(cur_time)-int(prev_time))/1000000)
                    else:
                        run_rapl['package-1'] = []
                        run_rapl['package-1'].append((int(cur_meas)-int(prev_meas))/(int(cur_time)-int(prev_time))/1000000)
            elif "power-energy-pkg-" in profiler_file:
                prev_time, prev_meas, interval = 0, 0, 0
                cur_time, cur_meas = 0, 0
                first_meas = 0
                run_rapl['power-energy-pkg'] = []
                with open(profiler_files + "/" + profiler_file, 'r') as file:
                
                    #skip header line
                    header = next(file) 
                    prev_time = 0
                    for line in file:
                        cur_time = line.split(',')[0]
                        cur_meas = line.split(',')[1] 
                        if not (int(cur_time) - int(prev_time) > 120):
                            run_rapl['power-energy-pkg'].append( float(cur_meas) / 10)
                            interval = int(cur_time) - int(prev_time)
                        else:
                            first_meas = cur_meas
                        prev_time = cur_time
                    
                    run_rapl['power-energy-pkg'].insert(0, float(first_meas) / 10)
                   
                    #remove 0 from last measurement
                    run_rapl['power-energy-pkg'].pop() 
            #mpstat file
            elif "MPSTAT" in profiler_file:
                if profiler_file=="MPSTAT":
                    continue        
                CPU = profiler_file.split('.')[1]
                run_mpstat[CPU] = {}
                run_mpstat[CPU]['usr'] = []
                run_mpstat[CPU]['nice'] = []
                run_mpstat[CPU]['sys'] = []
                run_mpstat[CPU]['iowait'] = []
                run_mpstat[CPU]['irq'] = []
                run_mpstat[CPU]['soft'] = []
                run_mpstat[CPU]['steal'] = []
                run_mpstat[CPU]['quest'] = []
                run_mpstat[CPU]['gnice'] = []
                run_mpstat[CPU]['idle'] = []
                with open(profiler_files + "/" + profiler_file, 'r') as file:
                
                    #skip header line
                    header = next(file) 
                    prev_time = 0
                    for line in file:
                        cur_meas = line.split(',')[1] 
                        run_mpstat[CPU]['usr'].append(float(cur_meas.split(' ')[0]))
                        run_mpstat[CPU]['nice'].append(float(cur_meas.split(' ')[1]))
                        run_mpstat[CPU]['sys'].append(float(cur_meas.split(' ')[2]))
                        run_mpstat[CPU]['iowait'].append(float(cur_meas.split(' ')[3]))
                        run_mpstat[CPU]['irq'].append(float(cur_meas.split(' ')[4]))
                        run_mpstat[CPU]['soft'].append(float(cur_meas.split(' ')[5]))
                        run_mpstat[CPU]['steal'].append(float(cur_meas.split(' ')[6]))
                        run_mpstat[CPU]['quest'].append(float(cur_meas.split(' ')[7]))
                        run_mpstat[CPU]['gnice'].append(float(cur_meas.split(' ')[8]))
                        run_mpstat[CPU]['idle'].append(float(cur_meas.split(' ')[9].strip()))
        #measure C0 residency
        for CPU in run_residency:
            C0_res = 1
            for state in run_residency[CPU]:
                if state != 'C0':
                    C0_res = C0_res - run_residency[CPU][state][(j-1)]
            if not "C0" in run_residency[CPU]: 
                run_residency[CPU]['C0'] = []
            run_residency[CPU]['C0'].append(C0_res)  

    cstates_config = '-'.join(directory_name.split("-")[0:-1]).split('=')[1].replace("-qps","").replace("-workerthreads", "")
    qps = '-'.join(directory_name.split("-")[0:-1]).split('=')[-1] 

    if cstates_config not in avg_residency:
        avg_residency[cstates_config] = {}
        avg_transitions[cstates_config] = {}
    if qps not in avg_residency[cstates_config]:
        avg_residency[cstates_config][qps] = {}
        avg_transitions[cstates_config][qps] = {}


    # Average for all run 
    for CPU in run_residency:
        if CPU not in avg_residency[cstates_config][qps]:
            avg_residency[cstates_config][qps][CPU] = {}
            avg_transitions[cstates_config][qps][CPU] = {}
        for state in run_residency[CPU]:
            if state not in avg_residency[cstates_config][qps][CPU]:
                avg_residency[cstates_config][qps][CPU][state] = []
                avg_transitions[cstates_config][qps][CPU][state] = []
            avg_residency[cstates_config][qps][CPU][state].append(run_residency[CPU][state][0])
            if state != "C0":    
                avg_transitions[cstates_config][qps][CPU][state].append(run_transitions[CPU][state][0])
    
    #rapl avg_rapl
    if cstates_config not in avg_rapl:
        avg_rapl[cstates_config] = {}
    if qps not in avg_rapl[cstates_config]:
        avg_rapl[cstates_config][qps] = {}
    for domain in run_rapl:
        if not domain in avg_rapl[cstates_config][qps]:
            avg_rapl[cstates_config][qps][domain] = []
        avg_rapl[cstates_config][qps][domain].append(run_rapl[domain][0])

   
    #interrupt avg_interrupts
    if cstates_config not in avg_interrupts:
        avg_interrupts[cstates_config] = {}
    if qps not in avg_interrupts[cstates_config]:
        avg_interrupts[cstates_config][qps] = {}
    for CPU in run_interrupts:
        if CPU not in avg_interrupts[cstates_config][qps]:
            avg_interrupts[cstates_config][qps][CPU] = {}
        for interrupt in run_interrupts[CPU]:
            if interrupt not in avg_interrupts[cstates_config][qps][CPU]:
                avg_interrupts[cstates_config][qps][CPU][interrupt] = []
            avg_interrupts[cstates_config][qps][CPU][interrupt].append(run_interrupts[CPU][interrupt])


    #rapl perf average rapl perf
    if cstates_config not in avg_perf_rapl:
        avg_perf_rapl[cstates_config] = {}
    if qps not in avg_perf_rapl[cstates_config]:
        avg_perf_rapl[cstates_config][qps] = []
    if "power-energy-pkg" in run_rapl:
        avg_perf_rapl[cstates_config][qps].append(run_rapl['power-energy-pkg'])
    
    #mpstat average
    if cstates_config not in avg_mpstat:
        avg_mpstat[cstates_config] = {}
    if qps not in avg_mpstat[cstates_config]:
        avg_mpstat[cstates_config][qps] = {}
    for CPU in run_mpstat:
        if CPU not in avg_mpstat[cstates_config][qps]:
            avg_mpstat[cstates_config][qps][CPU] = {}
        for utilization in run_mpstat[CPU]:
            if utilization not in avg_mpstat[cstates_config][qps][CPU]:
                avg_mpstat[cstates_config][qps][CPU][utilization] = []
            avg_mpstat[cstates_config][qps][CPU][utilization].append(statistics.mean(run_mpstat[CPU][utilization]))


   #avg 99th and queries average
    if cstates_config not in avg_response_time:
        avg_response_time[cstates_config] = {}
        avg_queries[cstates_config] = {}
    if qps not in avg_response_time[cstates_config]:
        avg_response_time[cstates_config][qps] = {}
        avg_queries[cstates_config][qps] = {}
        avg_response_time[cstates_config][qps]['avg'] = []
        avg_response_time[cstates_config][qps]['99th'] = []
        avg_queries[cstates_config][qps]['qps'] = []
    
    for response_time in run_response_time['avg']:
        avg_response_time[cstates_config][qps]['avg'].append(response_time)

    for response_time in run_response_time['99th']:
        avg_response_time[cstates_config][qps]['99th'].append(response_time)
   
    for queries in run_queries['qps']:
        avg_queries[cstates_config][qps]['qps'].append(queries)

    #avg socwatch 
    if cstates_config not in avg_residency_soc:
        avg_residency_soc[cstates_config] = {}
    if qps not in avg_residency_soc[cstates_config]:
        avg_residency_soc[cstates_config][qps] = {}
    for state in run_residency_soc:
        if state not in avg_residency_soc:
            avg_residency_soc[cstates_config][qps][state] = {}
            for i in range(0,40):
                if ("CPU" + str(i)) not in avg_residency_soc[cstates_config][qps][state]:
                    avg_residency_soc[cstates_config][qps][state]["CPU" + str(i)] = []
                avg_residency_soc[cstates_config][qps][state]["CPU" + str(i)].append(run_residency_soc[state]["CPU" + str(i)][0])
    
    
# Average per core , per socket 0 , per socket 1 per overall
overall_residency[directory_name] = {}
overall_transitions[directory_name] = {}

overall_residency[directory_name]['all'] = {}
overall_residency[directory_name]['0'] = {}
overall_residency[directory_name]['1'] = {}

overall_transitions[directory_name]['all'] = {}
overall_transitions[directory_name]['0'] = {}
overall_transitions[directory_name]['1'] = {}

for cstates in avg_residency:
    overall_residency[cstates] = {}
    overall_transitions[cstates] = {}

    for queries in avg_residency[cstates]:
        
        overall_residency[cstates][queries] = {}
        overall_transitions[cstates][queries] = {}

        overall_residency[cstates][queries]['all'] = {}
        overall_residency[cstates][queries]['0'] = {}
        overall_residency[cstates][queries]['1'] = {}

        overall_transitions[cstates][queries]['all'] = {}
        overall_transitions[cstates][queries]['0'] = {}
        overall_transitions[cstates][queries]['1'] = {}   

        if avg_residency[cstates][queries]:
            for state in avg_residency[cstates][queries]['CPU0']:    
                overall_residency[cstates][queries]['all'][state] = 0
                overall_residency[cstates][queries]['0'][state] = 0
                overall_residency[cstates][queries]['1'][state] = 0

                overall_transitions[cstates][queries]['all'][state] = 0
                overall_transitions[cstates][queries]['0'][state]  = 0
                overall_transitions[cstates][queries]['1'][state]  = 0

                #socket 0
                for i in range(0,20):
                    overall_residency[cstates][queries]['all'][state] = overall_residency[cstates][queries]['all'][state] + statistics.mean(avg_residency[cstates][queries]['CPU' + str(i)][state])
                    overall_residency[cstates][queries]['0'][state] = overall_residency[cstates][queries]['0'][state] + statistics.mean(avg_residency[cstates][queries]['CPU' + str(i)][state])
                    if state != "C0":
                        overall_transitions[cstates][queries]['all'][state] = overall_transitions[cstates][queries]['all'][state] + statistics.mean(avg_transitions[cstates][queries]['CPU' + str(i)][state])
                        overall_transitions[cstates][queries]['0'][state] = overall_transitions[cstates][queries]['0'][state] + statistics.mean(avg_transitions[cstates][queries]['CPU' + str(i)][state])

                #socket 1
                for i in range(20,40):
                    overall_residency[cstates][queries]['all'][state] = overall_residency[cstates][queries]['all'][state] + statistics.mean(avg_residency[cstates][queries]['CPU' + str(i)][state])
                    overall_residency[cstates][queries]['1'][state] = overall_residency[cstates][queries]['1'][state] + statistics.mean(avg_residency[cstates][queries]['CPU' + str(i)][state])
                    if state != "C0":
                        overall_transitions[cstates][queries]['all'][state] = overall_transitions[cstates][queries]['all'][state] + statistics.mean(avg_transitions[cstates][queries]['CPU' + str(i)][state])
                        overall_transitions[cstates][queries]['1'][state] = overall_transitions[cstates][queries]['1'][state] + statistics.mean(avg_transitions[cstates][queries]['CPU' + str(i)][state])

                overall_residency[cstates][queries]['all'][state] = overall_residency[cstates][queries]['all'][state] / 40
                overall_residency[cstates][queries]['0'][state] = overall_residency[cstates][queries]['0'][state] / 20
                overall_residency[cstates][queries]['1'][state] = overall_residency[cstates][queries]['1'][state] / 20

                if state != "C0":
                    overall_transitions[cstates][queries]['all'][state] = overall_transitions[cstates][queries]['all'][state] #/ 40
                    overall_transitions[cstates][queries]['0'][state] = overall_transitions[cstates][queries]['0'][state] #/ 20
                    overall_transitions[cstates][queries]['1'][state] = overall_transitions[cstates][queries]['1'][state] #/ 20

#overall rapl
for cstates_config in avg_rapl:
    if cstates_config not in overall_rapl:
            overall_rapl[cstates_config] = {}
    for queries in avg_rapl[cstates_config]:
        if queries not in overall_rapl[cstates_config]:
            overall_rapl[cstates_config][queries] = {}
        for domain in avg_rapl[cstates_config][queries]:
            if domain not in overall_rapl[cstates_config][queries]:
                overall_rapl[cstates_config][queries][domain] = 0
            overall_rapl[cstates_config][queries][domain] = statistics.mean(avg_rapl[cstates_config][queries][domain])

#overall interrupts
for cstates_config in avg_interrupts:
    if cstates_config not in overall_interrupts:
            overall_interrupts[cstates_config] = {}
    for queries in avg_interrupts[cstates_config]:
        if queries not in overall_interrupts[cstates_config]:
            overall_interrupts[cstates_config][queries] = {}
        for state in avg_interrupts[cstates_config][queries]:
            if state not in overall_interrupts[cstates_config][queries]:
                overall_interrupts[cstates_config][queries][state] = 0
            for i in range(0,40):
                id = "CPU" + str(i) 
                if id in avg_interrupts[cstates_config][queries][state]:
                    overall_interrupts[cstates_config][queries][state] = overall_interrupts[cstates_config][queries][state] + statistics.mean(avg_interrupts[cstates_config][queries][state]['CPU' + str(i)])
       
# overall perf stats
for cstates_config in avg_perf_rapl:
    if cstates_config not in overall_perf_rapl:
            overall_perf_rapl[cstates_config] = {}
    for queries in avg_perf_rapl[cstates_config]:
        if queries not in overall_perf_rapl[cstates_config]:
            overall_perf_rapl[cstates_config][queries] = {}
        temp_list = []
        for power_meas in avg_perf_rapl[cstates_config][queries]:
            temp_list.append(statistics.mean(power_meas))
        if temp_list:
            overall_perf_rapl[cstates_config][queries] = statistics.mean(temp_list)

#overall mpstat
for cstates_config in avg_mpstat:
    if cstates_config not in overall_mpstat:
            overall_mpstat[cstates_config] = {}
    for queries in avg_mpstat[cstates_config]:
        if queries not in overall_mpstat[cstates_config]:
            overall_mpstat[cstates_config][queries] = {}
        for CPU in avg_mpstat[cstates_config][queries]:
            if CPU not in overall_mpstat[cstates_config][queries]:
                overall_mpstat[cstates_config][queries][CPU] = {}
            for utilization in avg_mpstat[cstates_config][queries][CPU]:
                overall_mpstat[cstates_config][queries][CPU][utilization] = statistics.mean(avg_mpstat[cstates_config][queries][CPU][utilization])

            
#overall average response time and 99th and queries
for cstates_config in avg_response_time:
    if cstates_config not in overall_response_time:
            overall_response_time[cstates_config] = {}
            overall_queries[cstates_config] = {}
    for queries in avg_response_time[cstates_config]:
        if queries not in overall_response_time[cstates_config]:
            overall_response_time[cstates_config][queries] = {}
            overall_queries[cstates_config][queries] = {}
            overall_response_time[cstates_config][queries]['avg'] = 0
            overall_response_time[cstates_config][queries]['avg-stdev'] = 0
            overall_response_time[cstates_config][queries]['99th'] = 0
            overall_response_time[cstates_config][queries]['99th-stdev'] = 0
            overall_queries[cstates_config][queries]['qps'] = 0 

        overall_response_time[cstates_config][queries]['avg'] = statistics.mean(avg_response_time[cstates_config][queries]['avg'])
        overall_response_time[cstates_config][queries]['avg-stdev'] = statistics.stdev(avg_response_time[cstates_config][queries]['avg'])

        overall_response_time[cstates_config][queries]['99th'] = statistics.mean(avg_response_time[cstates_config][queries]['99th'])
        overall_response_time[cstates_config][queries]['99th-stdev'] = statistics.stdev(avg_response_time[cstates_config][queries]['99th'])

        overall_queries[cstates_config][queries]['qps'] =  statistics.mean(avg_queries[cstates_config][queries]['qps'])

#overall socwatch
for cstates_config in avg_residency_soc:
    if cstates_config not in overall_residency_soc:
            overall_residency_soc[cstates_config] = {}
    for queries in avg_residency_soc[cstates_config]:
        if queries not in overall_residency_soc[cstates_config]:
            overall_residency_soc[cstates_config][queries] = {}
            overall_residency_soc[cstates][queries]['all'] = {}
            overall_residency_soc[cstates][queries]['0'] = {}
            overall_residency_soc[cstates][queries]['1'] = {}

        for state in avg_residency_soc[cstates_config][queries]:
            if state not in overall_residency_soc[cstates_config][queries]:
                overall_residency_soc[cstates][queries]['all'][state] = 0
                overall_residency_soc[cstates][queries]['0'][state] = 0
                overall_residency_soc[cstates][queries]['1'][state] = 0
    
            #socket 0
            for i in range(0,20):
                overall_residency_soc[cstates][queries]['all'][state] = overall_residency_soc[cstates][queries]['all'][state] + statistics.mean(avg_residency_soc[cstates][queries][state]['CPU' + str(i)])
                overall_residency_soc[cstates][queries]['0'][state] = overall_residency_soc[cstates][queries]['0'][state] + statistics.mean(avg_residency_soc[cstates][queries][state]['CPU' + str(i)])
                
            #socket 1
            for i in range(20,40):
                overall_residency_soc[cstates][queries]['all'][state] = overall_residency_soc[cstates][queries]['all'][state] + statistics.mean(avg_residency_soc[cstates][queries][state]['CPU' + str(i)])
                overall_residency_soc[cstates][queries]['1'][state] = overall_residency_soc[cstates][queries]['1'][state] + statistics.mean(avg_residency_soc[cstates][queries][state]['CPU' + str(i)])
        
            overall_residency_soc[cstates][queries]['all'][state] = overall_residency_soc[cstates][queries]['all'][state] / 40
            overall_residency_soc[cstates][queries]['0'][state] = overall_residency_soc[cstates][queries]['0'][state] / 20
            overall_residency_soc[cstates][queries]['1'][state] = overall_residency_soc[cstates][queries]['1'][state] / 20

if avg_residency[cstates][queries]:
    # print average for specific experiment

    for cstates in avg_residency:
        for queries in avg_residency[cstates]:
            file_path = parent_directory + '/profiler_residency_' + str(cstates) + '_' + str(queries) + '.csv'
            
            # Writing the dictionary to a CSV file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write headers - state
                
                states = ["C0", "POLL", "C1-SKX", "C1E-SKX", "C6-SKX"]
                
                # Write labels
                headers = ["-1", "C0", "POLL", "C1-SKX", "C1E-SKX", "C6-SKX"]
                writer.writerow(headers)
                
                # Write data
                for i in range(0,40):
                    row = []
                    row = ["CPU" + str(i)]
                    for state in states:
                        if state in avg_residency[cstates][queries]["CPU" + str(i)]: 
                            row.append(statistics.mean(avg_residency[cstates][queries]["CPU" + str(i)][state]))
                        else:
                            continue
                    writer.writerow(row)   

if avg_transitions[cstates][queries]:
    for cstates in avg_residency:
        for queries in avg_residency[cstates]:

            file_path = parent_directory + '/profiler_transitions_' + str(cstates) + '_' + str(queries) + '.csv'
            
            # Writing the dictionary to a CSV file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write headers - state
                
                states = ["POLL", "C1-SKX", "C1E-SKX", "C6-SKX"]
                
                # Write labels
                headers = ["-1", "POLL", "C1-SKX", "C1E-SKX", "C6-SKX"]
                writer.writerow(headers)
                
                # Write data
                for i in range(0,40):
                    row = []
                    row = ["CPU" + str(i)]
                    for state in states:
                        if state in avg_transitions[cstates][queries]["CPU" + str(i)]:
                            row.append(statistics.mean(avg_transitions[cstates][queries]["CPU" + str(i)][state]))
                        else:
                            continue
                    writer.writerow(row)  

if "package-0" in avg_rapl:
    for cstates in avg_rapl:
        for queries in avg_rapl[cstates]:
            file_path = parent_directory + '/profiler_rapl_' + str(cstates) + '_' + str(queries) + '.csv'

            # Writing the dictionary to a CSV file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write headers - state
                
                states = ["package-0", "package-1"]
                
                # Write labels
                headers = ["package-0", "package-1"]
                writer.writerow(headers)
                
                # Write data
                for i in range(0,len(avg_rapl[cstates][queries][states[0]])):
                    row = []
                    for domain in states:
                        row.append(avg_rapl[cstates][queries][domain][i])
                    writer.writerow(row)  

if avg_interrupts:
    for cstates in avg_interrupts:
        for queries in avg_interrupts[cstates]:

            file_path = parent_directory + '/profiler_interrupts_' + str(cstates) + '_' + str(queries) + '.csv'
            
            # Writing the dictionary to a CSV file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write headers - state
                
                headers = [-1]
                # Write labels
                for state in avg_interrupts[cstates][queries]:
                    headers.append(state)
                writer.writerow(headers)
                
                # Write data
                for i in range(0,40):
                    row = []
                    row = ["CPU" + str(i)]
                    for state in headers:
                        if state == -1:
                            continue
                        id = "CPU" + str(i)
                        if id in avg_interrupts[cstates][queries][state]:
                            row.append(statistics.mean(avg_interrupts[cstates][queries][state]["CPU" + str(i)]))
                        else: 
                            row.append("0")
                    writer.writerow(row) 

if avg_perf_rapl:
    for cstates in avg_perf_rapl:
        for queries in avg_perf_rapl[cstates]:

            file_path = parent_directory + '/profiler_perf_rapl' + str(cstates) + '_' + str(queries) + '.csv'
            
            # Writing the dictionary to a CSV file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write headers - state
                
                headers = [-1, "package power"]
                # Write labels
                writer.writerow(headers)
                
                # Write data
                for i in range(0,len(avg_perf_rapl[cstates][queries])):
                    row = []
                    row = ["RUN" + str(i)]
                    for power_meas in avg_perf_rapl[cstates][queries][i]:
                            row.append(power_meas)
                    writer.writerow(row)   

if overall_mpstat['c-states_enabled']['10000']:
    for cstates in overall_mpstat:
        for queries in overall_mpstat[cstates]:

            file_path = parent_directory + '/profiler_mpstat_' + str(cstates) + '_' + str(queries) + '.csv'
            
            # Writing the dictionary to a CSV file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write headers - state
                
                headers = [-1]
                # Write labels
                for state in overall_mpstat[cstates][queries]['CPU0']:
                    headers.append(state)
                writer.writerow(headers)
                
                # Write data
                for i in range(0,40):
                    row = []
                    row = ["CPU" + str(i)]
                    for state in headers:
                        if state == -1:
                            continue
                        id = "CPU" + str(i)
                        if id in overall_mpstat[cstates][queries]:
                            row.append(overall_mpstat[cstates][queries]["CPU" + str(i)][state])
                    writer.writerow(row) 

#print response time and query statistics for each qps
if avg_response_time:
    for cstates in avg_response_time:
        for queries in avg_response_time[cstates]:

            file_path = parent_directory + '/profiler_time_' + str(cstates) + '_' + str(queries) + '.csv'
            
            # Writing the dictionary to a CSV file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write headers - state
                
                headers = [-1, "queries", "avg", "99th"]
                # Write labels
                writer.writerow(headers)
                
                # Write data
                for i in range(0,len(avg_response_time[cstates][queries]['avg'])):
                    row = []
                    row = ["RUN" + str(i)]
                    row.append(avg_queries[cstates][queries]['qps'][i])
                    row.append(avg_response_time[cstates][queries]['avg'][i])
                    row.append(avg_response_time[cstates][queries]['99th'][i])
                    writer.writerow(row) 

# print residency soc for each qps and cpu
if avg_residency_soc:
    for cstates in avg_residency_soc:
        for queries in avg_residency_soc[cstates]:

            file_path = parent_directory + '/socwatch_residency' + str(cstates) + '_' + str(queries) + '.csv'
            
            # Writing the dictionary to a CSV file
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write headers - state
                
                headers = [-1, "CC0", "CC1", "CC6"]
                # Write labels
                writer.writerow(headers)
                
                # Write data
                for i in range(0,40):
                    row = []
                    row = ["CPU" + str(i)]
                    for state in headers:
                        if state == -1:
                            continue
                        id = "CPU" + str(i)
                        if id in avg_residency_soc[cstates][queries][state]:
                            row.append(statistics.mean(avg_residency_soc[cstates][queries][state]["CPU" + str(i)]))
                    writer.writerow(row) 


# print overall statistics in file   
if overall_residency:
    file_path = parent_directory + '/merged_profiler_residency.csv'

    # Writing the dictionary to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write headers - state
        
        states = ["C0", "POLL", "C1-SKX", "C1E-SKX", "C6-SKX"]
        
        # Write labels
        headers = ["-1","-1","-1", "C0", "POLL", "C1-SKX", "C1E-SKX", "C6-SKX"]
        writer.writerow(headers)
        

        # Write data
        for kernel_conf in overall_residency:
            for queries in overall_residency[kernel_conf]:
                row = []
                for domain in overall_residency[kernel_conf][queries]:
                    if domain == "all":
                        row = [kernel_conf,queries,domain]
                    else:
                        row = ["-1","-1",domain]
                    for state in states:
                        if state in overall_residency[kernel_conf][queries][domain]:
                            row.append(overall_residency[kernel_conf][queries][domain][state])
                        else:
                            continue
                    writer.writerow(row)     
            
if overall_transitions:

    file_path = parent_directory + '/merged_profiler_transitions.csv'

    # Writing the dictionary to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write headers - state
        
        states = ["POLL", "C1-SKX", "C1E-SKX", "C6-SKX"]
        
        # Write labels
        headers = ["-1","-1","-1", "POLL", "C1-SKX", "C1E-SKX", "C6-SKX"]
        writer.writerow(headers)
        

        # Write data
        for kernel_conf in overall_transitions:
            for queries in overall_transitions[kernel_conf]:
                row = []
                for domain in overall_transitions[kernel_conf][queries]:
                    if domain == "all":
                        row = [kernel_conf,queries,domain]
                    else:
                        row = ["-1","-1",domain]
                    for state in states:
                        if state in overall_transitions[kernel_conf][queries][domain]:
                            row.append(overall_transitions[kernel_conf][queries][domain][state])
                        else:
                            continue
                    writer.writerow(row)

if "package-0" in overall_rapl:
    file_path = parent_directory + '/merged_profiler_rapl.csv'

    # Writing the dictionary to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write headers - state
        
        states = ["package-0", "package-1"]
        
        # Write labels
        headers = ["-1","-1","-1", "package-0", "package-1"]
        writer.writerow(headers)
        

        # Write data
        for kernel_conf in overall_rapl:
            for queries in overall_rapl[kernel_conf]:
                row = []
                row = ["-1",kernel_conf,queries]
                for domain in states: 
                    row.append(overall_rapl[kernel_conf][queries][domain])
                writer.writerow(row)

# print overall statistics in file   
if overall_interrupts:
    for cstates in overall_interrupts:
        for queries in overall_interrupts[cstates]:
            print()
    headers = [-1,-1]
    for state in overall_interrupts[cstates][queries]:
        headers.append(state)
    
    
    file_path = parent_directory + '/merged_profiler_interrupt.csv'

    # Writing the dictionary to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers) 
        row = []
        # Write data
        for kernel_conf in overall_interrupts:
            row = []
            row.append(kernel_conf)
            for queries in overall_interrupts[kernel_conf]:
                row.append(queries)
                for state in headers:
                    if state in overall_interrupts[kernel_conf][queries]:
                        row.append(overall_interrupts[kernel_conf][queries][state])
                    else:
                        row.append("0")
                writer.writerow(row)
                row=[]
                row.append(-1)     

# print overall statistics in file   
if overall_rapl:
    file_path = parent_directory + '/merged_profiler_perf_rapl.csv'

    # Writing the dictionary to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
              
        # Write labels
        headers = ["package"]
        writer.writerow(headers)
        

        # Write data
        for kernel_conf in overall_perf_rapl:
            for queries in overall_perf_rapl[kernel_conf]:
                row = []
                row = ["-1",kernel_conf,queries]
                row.append(overall_perf_rapl[kernel_conf][queries])
                writer.writerow(row)

# print overall statistics in file   
if overall_mpstat['c-states_enabled']['10000']:
    for cstates in overall_mpstat:
        for queries in overall_mpstat[cstates]:
            print()
    headers = [-1,-1]
    for state in overall_mpstat[cstates][queries]['CPUall']:
        headers.append(state)
    
    
    file_path = parent_directory + '/merged_profiler_mpstat.csv'

    # Writing the dictionary to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers) 
        row = []
        # Write data
        for kernel_conf in overall_mpstat:
            row = []
            row.append(kernel_conf)
            for queries in overall_mpstat[kernel_conf]:
                row.append(queries)
                for state in headers:
                    if state in overall_mpstat[kernel_conf][queries]['CPUall']:
                        row.append(overall_mpstat[kernel_conf][queries]['CPUall'][state])
                writer.writerow(row)
                row=[]
                row.append(-1) 


#print overll statistics time and queries
if overall_response_time:
    file_path = parent_directory + '/merged_profiler_time.csv'

    # Writing the dictionary to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
              
        # Write labels
        headers = ["-1", "-1", "-1", "qps", "avg", "avg-stdev", "99th", "99th-stdev"]
        writer.writerow(headers)
        

        # Write data
        for kernel_conf in overall_response_time:
            for queries in overall_response_time[kernel_conf]:
                row = []
                row = ["-1",kernel_conf,queries]
                row.append(overall_queries[kernel_conf][queries]['qps'])
                row.append(overall_response_time[kernel_conf][queries]['avg'])
                row.append(overall_response_time[kernel_conf][queries]['avg-stdev'])
                row.append(overall_response_time[kernel_conf][queries]['99th'])
                row.append(overall_response_time[kernel_conf][queries]['99th-stdev'])
                writer.writerow(row)

#print overall statistics for socwatch residency

# print overall statistics in file     
if overall_residency_soc:
    file_path = parent_directory + '/merged_socwatch_residency.csv'

    # Writing the dictionary to a CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write headers - state
        
        states = ["CC0", "CC1", "CC6"]
        
        # Write labels
        headers = ["-1","-1","-1", "CC0", "CC1", "CC6"]
        writer.writerow(headers)
        

        # Write data
        for kernel_conf in overall_residency_soc:
            for queries in overall_residency_soc[kernel_conf]:
                row = []
                for domain in overall_residency_soc[kernel_conf][queries]:
                    if domain == "all":
                        row = [kernel_conf,queries,domain]
                    else:
                        row = ["-1","-1",domain]
                    for state in states:
                        if state in overall_residency_soc[kernel_conf][queries][domain]:
                            row.append(overall_residency_soc[kernel_conf][queries][domain][state])
                        else:
                            continue
                    writer.writerow(row)