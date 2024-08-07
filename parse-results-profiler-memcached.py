import os
import pandas as pd
import json
import statistics
import csv 
import sys
import math
import re
from itertools import combinations

#Need to Check confidence interval theory

# qps_list = [10000, 50000, 100000, 200000, 300000, 400000, 500000]
qps_list = [5000, 10000, 15000, 20000]
z=1.96 # from taming performance variability paper
# n=50

def print_speedup_metrics(stats_dir, speedup_statistics, filename ):
    header = ["exp_name-configuration","qps", "metric", "ci-min", "ci-max"]
    metric_tab = ['avg-speedup', '99th-speedup']
    for exp_name in speedup_statistics:
        for qps in qps_list:
            for metric in speedup_statistics[exp_name][0][qps]:
                size = len(speedup_statistics[exp_name][0][qps][metric])
                break
            break
        break
    
    for i in range(0,size):
        header.append("M" + str(i+1))
   
    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        
        for exp_name in speedup_statistics: 
            for metric in metric_tab:
                for qps in qps_list:
                    
                    row = []
                    row.append(exp_name)
                    row.append(qps)
                    row.append(metric)
                    row.append(speedup_statistics[exp_name][0][qps][str(metric) + '-ci-min'])
                    row.append(speedup_statistics[exp_name][0][qps][str(metric) + '-ci-max'])
                   
                    for meas in speedup_statistics[exp_name][0][qps][metric]:
                        row.append(meas)
                    
                    writer.writerow(row)

def print_all_metrics(stats_dir, overall_raw_measurements, overall_statistics, filename):

    header = ["exp_name","configuration","qps", "metric", "avg", "median", "stdev", "cv", "ci-min", "ci-max"]
   
    for exp_name in overall_raw_measurements:
        for conf_list in overall_raw_measurements[exp_name]:
            for id,conf in enumerate(list(conf_list.keys())):
                for qps in qps_list:
                    for metric in overall_raw_measurements[exp_name][id][conf][qps]:
                        size = len(overall_raw_measurements[exp_name][id][conf][qps][metric])
                        break
                    break
                break
            break
        break
    
    for i in range(0,size):
        header.append("M" + str(i+1))
   
    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for metric in overall_statistics[exp_name][0][conf][qps_list[0]]:
                        for qps in qps_list:
                            if qps in overall_statistics[exp_name][0][conf]:
                                row = []
                                row.append(exp_name)
                                row.append(conf)
                                row.append(qps)
                                row.append(metric)
                                row.append(overall_statistics[exp_name][0][conf][qps][metric]["avg"])
                                row.append(overall_statistics[exp_name][0][conf][qps][metric]["median"])
                                row.append(overall_statistics[exp_name][0][conf][qps][metric]["stdev"])
                                row.append(overall_statistics[exp_name][0][conf][qps][metric]["cv"])
                                row.append(overall_statistics[exp_name][0][conf][qps][metric]["ci"]["min"])
                                row.append(overall_statistics[exp_name][0][conf][qps][metric]["ci"]["max"])
                                for meas in overall_raw_measurements[exp_name][0][conf][qps][metric]:
                                    row.append(meas)
                                
                                writer.writerow(row)

def print_residency_merged(stats_dir, overall_raw_measurements, overall_statistics, metric, filename):
    header = ["exp_name","configuration","qps", "metric", "C0", "C1", "C1E", "C6"]
      
    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for qps in qps_list:
                        if qps in overall_statistics[exp_name][0][conf]:    
                            if "C0-res" not in overall_statistics[exp_name][0][conf][qps]:
                                return
                            row = []
                            row.append(exp_name)
                            row.append(conf)
                            row.append(qps)
                            row.append(metric)
                            row.append(overall_statistics[exp_name][0][conf][qps]['C0-res']["avg"])
                            row.append(overall_statistics[exp_name][0][conf][qps]['C1-res']["avg"])
                            row.append(overall_statistics[exp_name][0][conf][qps]['C1E-res']["avg"])
                            row.append(overall_statistics[exp_name][0][conf][qps]['C6-res']["avg"])
                            writer.writerow(row)

def print_transition_merged(stats_dir, overall_raw_measurements, overall_statistics, metric, filename):
    
    header = ["exp_name","configuration","qps", "metric", "C0", "C1", "C1E", "C6"]

    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for qps in qps_list:
                        if qps in overall_statistics[exp_name][0][conf]:
                            if "C0-tr" not in overall_statistics[exp_name][0][conf][qps]:
                                return
                            row = []
                            row.append(exp_name)
                            row.append(conf)
                            row.append(qps)
                            row.append(metric)
                            row.append(overall_statistics[exp_name][0][conf][qps]['C0-tr']["avg"])
                            row.append(overall_statistics[exp_name][0][conf][qps]['C1-tr']["avg"])
                            row.append(overall_statistics[exp_name][0][conf][qps]['C1E-tr']["avg"])
                            row.append(overall_statistics[exp_name][0][conf][qps]['C6-tr']["avg"])
                            writer.writerow(row)

def print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, metric, filename):

    header = ["exp_name","configuration","qps", "metric", "avg", "median", "stdev", "cv", "ci-min", "ci-max"]
   
    for exp_name in overall_raw_measurements:
        for conf_list in overall_raw_measurements[exp_name]:
            for id,conf in enumerate(list(conf_list.keys())):
                for qps in qps_list:
                    if not "C0-res" in overall_raw_measurements[exp_name][0][conf][qps]:
                        return
                    size = len(overall_raw_measurements[exp_name][0][conf][qps][metric])
                    break
                break
            break
        break
    
    for i in range(0,size):
        header.append("M" + str(i+1))
   
    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for qps in qps_list:
                        if qps in overall_statistics[exp_name][0][conf]:
                            row = []
                            row.append(exp_name)
                            row.append(conf)
                            row.append(qps)
                            row.append(metric)
                            row.append(overall_statistics[exp_name][0][conf][qps][metric]["avg"])
                            row.append(overall_statistics[exp_name][0][conf][qps][metric]["median"])
                            row.append(overall_statistics[exp_name][0][conf][qps][metric]["stdev"])
                            row.append(overall_statistics[exp_name][0][conf][qps][metric]["cv"])
                            row.append(overall_statistics[exp_name][0][conf][qps][metric]["ci"]["min"])
                            row.append(overall_statistics[exp_name][0][conf][qps][metric]["ci"]["max"])
                            for meas in overall_raw_measurements[exp_name][0][conf][qps][metric]:
                                row.append(meas)
                            
                            writer.writerow(row)

def confidence_interval_mean (metric_measurements):
    temp_list  = metric_measurements.copy()
    temp_list.sort()
    n = len(temp_list)
    
    min_i = math.floor((n-z*math.sqrt(n)) / 2)
    max_i = math.ceil(1 + (n+z*math.sqrt(n)) / 2) 
    return temp_list[min_i-1], temp_list[max_i-1]

def coefficient_of_variation(metric_measurements):
    return statistics.stdev(metric_measurements) / statistics.mean(metric_measurements)

def standard_deviation(metric_measurements):
    return statistics.stdev(metric_measurements)

def median(metric_measurements):
    return statistics.median(metric_measurements)

def average(metric_measurements):
    return statistics.mean(metric_measurements)

def average_ignore_zeros(metric_measurements):
    return statistics.mean([i for i in metric_measurements if i!=0] or [0])

def calculate_speedup_stats_single_instance(instance_stats, first_item, second_item):

    metrics = ['avg','99th']
    for qps in first_item:
        instance_stats[qps] = {}
        for metric in metrics:
           
            # measure items in 1 and 2
            len1 = len(first_item[qps][metric])
            len2 = len(second_item[qps][metric])
            if len1 >= len2:
                num_elements = len2
            else:
                num_elements = len1

            # measure x speedups 1 - x1/x2 for both avg and 99th tail latency
            instance_stats[qps][str(metric) + "-speedup"] = []
            for i in range(0,num_elements):
                instance_stats[qps][str(metric) + "-speedup"].append(first_item[qps][metric][i] / second_item[qps][metric][i])
               
            # measure CI for avg
            instance_stats[qps][str(metric) + "-speedup" + "-ci-min"], instance_stats[qps][str(metric) + "-speedup" + "-ci-max"] = confidence_interval_mean(instance_stats[qps][str(metric) + "-speedup"])
            
def calculate_stats_single_instance(instance_stats, instance_raw_measurements, conf):

    for qps in instance_raw_measurements[conf]:
        instance_stats[qps] = {}
        for metric in instance_raw_measurements[conf][qps]:
            
            if metric != "residency": 
                if instance_raw_measurements[conf][qps][metric]:
                    instance_stats[qps][metric] = {}
                    #calculate statistics   
                    if "package-0" in metric or "package-1" in metric or "dram-0" in metric or "dram-1" in metric:
                        instance_stats[qps][metric]['avg'] = average_ignore_zeros(instance_raw_measurements[conf][qps][metric])
                    else:
                        instance_stats[qps][metric]['avg'] = average(instance_raw_measurements[conf][qps][metric])
                    instance_stats[qps][metric]['median'] = median(instance_raw_measurements[conf][qps][metric])
                    if len(instance_raw_measurements[conf][qps][metric]) >=2: 
                        instance_stats[qps][metric]['stdev'] = standard_deviation(instance_raw_measurements[conf][qps][metric])
                    else:
                        instance_stats[qps][metric]['stdev'] = 0 
                    if instance_stats[qps][metric]['median'] > 0 and instance_stats[qps][metric]['stdev'] != 0:
                        instance_stats[qps][metric]['cv'] = coefficient_of_variation(instance_raw_measurements[conf][qps][metric])
                    else:
                        instance_stats[qps][metric]['cv'] = 0
                    instance_stats[qps][metric]['ci'] = {}
                    if len(instance_raw_measurements[conf][qps][metric]) < 10:
                        instance_stats[qps][metric]['ci']['min'] = 0
                        instance_stats[qps][metric]['ci']['max'] = 0
                    else:
                        instance_stats[qps][metric]['ci']['min'], instance_stats[qps][metric]['ci']['max'] = confidence_interval_mean(instance_raw_measurements[conf][qps][metric])
                else:
                    instance_stats[qps][metric] = {}
                    instance_stats[qps][metric]['avg'] = 0
                    instance_stats[qps][metric]['median'] = 0
                    instance_stats[qps][metric]['stdev'] = 0
                    instance_stats[qps][metric]['cv'] = 0
                    instance_stats[qps][metric]['ci'] = {}
                    instance_stats[qps][metric]['ci']['min'] = 0
                    instance_stats[qps][metric]['ci']['max'] = 0

def calculate_speedup_stats_multiple_instances(name, first_item, second_item):
    instance_stats = {}
    calculate_speedup_stats_single_instance(instance_stats, first_item, second_item)
    return instance_stats

def calculate_stats_multiple_instances(exp_name,overall_raw_measurements):

    instances_stats = {}
    for ind,instance in enumerate(overall_raw_measurements[exp_name]):
        for conf in overall_raw_measurements[exp_name][ind]:
            instances_stats[conf] = {}
            calculate_stats_single_instance(instances_stats[conf], overall_raw_measurements[exp_name][ind], conf)
    
    return instances_stats

def derive_datatype(datastr):
    try:
        return type(ast.literal_eval(datastr))
    except:
        return type("")

def read_timeseries(filepath):
    header = None
    timeseries = None
    with open(filepath, 'r') as f:
        header = f.readline().strip()
        timeseries = []
        data = f.readline().strip().split(',')
        datatype = derive_datatype(data[1])
        f.seek(0)
        for l in f.readlines()[1:]:
            data = l.strip().split(',')
            timestamp = int(data[0])
            value = datatype(data[1])
            timeseries.append((timestamp, value))
    return (header, timeseries)            

def add_metric_to_dict(stats_dict, metric_name, metric_value):
    head = metric_name.split('.')[0]
    tail = metric_name.split('.')[1:]
    if tail:
        stats_dict = stats_dict.setdefault(head, {})
        add_metric_to_dict(stats_dict, '.'.join(tail), metric_value)
    else:
        stats_dict[head] = metric_value

def cpu_state_usage(data, cpu_id):
    cpu_str = "CPU{}".format(cpu_id)
    state_names = ['POLL', 'C1', 'C1E', 'C6']
    state_time_perc = []
    total_state_time = 0
    time_us = 0
    state_usage_vec = []
    for state_name in state_names:
        if state_name in data[cpu_str]:
            (ts_start, val_start) = data[cpu_str][state_name]['usage'][0]
            (ts_end, val_end) = data[cpu_str][state_name]['usage'][-1]
            state_usage = int(val_end) - int(val_start)
            state_usage_vec.append(state_usage)
    return state_usage_vec

def avg_state_usage(stats, cpu_id_list):
    total_state_usage = [0]*4
    cpu_count = 0
    for cpud_id in cpu_id_list:
        cpu_count += 1
        total_state_usage = [a + b for a, b in zip(total_state_usage, cpu_state_usage(stats, cpud_id))]
    avg_state_usage = [a/b for a, b in zip(total_state_usage, [cpu_count]*len(total_state_usage))]
    return avg_state_usage

def cpu_state_time_perc(data, cpu_id):
    cpu_str = "CPU{}".format(cpu_id)
    state_names = ['POLL', 'C1', 'C1E', 'C6']
    state_time_perc = []
    total_state_time = 0
    time_us = 0
    # determine time window of measurements
    for state_name in state_names:
        if state_name in data[cpu_str]:
            (ts_start, val_start) = data[cpu_str][state_name]['time'][0]
            (ts_end, val_end) = data[cpu_str][state_name]['time'][-1]
            time_us = max(time_us, (ts_end - ts_start) * 1000000.0)
            total_state_time += int(val_end) - int(val_start)    
    time_us = max(time_us, total_state_time)
    # FIXME: time duration is currently hardcoded at 120s (120000000us)
    extra_c6_time_us = time_us - 120000000
    # calculate percentage
    for state_name in state_names:
        if state_name == 'C6':
            extra = extra_c6_time_us
        else:
            extra = 0
        if state_name in data[cpu_str]:
            (ts_start, val_start) = data[cpu_str][state_name]['time'][0]
            (ts_end, val_end) = data[cpu_str][state_name]['time'][-1]
            state_time_perc.append(((int(val_end)-int(val_start)-extra)/time_us)*100)
    # calculate C0 as the remaining time 
    state_time_perc[0] = 100 - sum(state_time_perc[1:4])
    state_names[0] = 'C0' 
    return state_time_perc

def avg_state_time_perc(stats, cpu_id_list):
    for stat in stats:
        total_state_time_perc = [0]*4
        cpu_count = 0
        for cpud_id in cpu_id_list:
            cpu_count += 1
            total_state_time_perc = [a + b for a, b in zip(total_state_time_perc, cpu_state_time_perc(stats, cpud_id))]
        avg_state_time_perc = [a/b for a, b in zip(total_state_time_perc, [cpu_count]*len(total_state_time_perc))]
    return avg_state_time_perc

def calculate_cstate_stats(instances_raw_measurements, inst_name, qps):
    # Check if residency exiists
    if not instances_raw_measurements[inst_name][qps]['residency'][0]:
        return
    # determine used C-states
    state_names = ['C0']
    check_state_names = ['C1', 'C1E', 'C6']
    for state_name in check_state_names:
        if state_name in instances_raw_measurements[inst_name][qps]['residency'][0]['CPU0']:
            state_names.append(state_name)
    
    time_perc_list = []
    for stat in instances_raw_measurements[inst_name][qps]['residency']:
        time_perc_list.append(avg_state_time_perc(stat, range(0, 10)))
   
    instances_raw_measurements[inst_name][qps]['C0-res'] = []
    instances_raw_measurements[inst_name][qps]['C1-res'] = []
    instances_raw_measurements[inst_name][qps]['C1E-res'] = []
    instances_raw_measurements[inst_name][qps]['C6-res'] = []
    metrics=['C0-res','C1-res','C1E-res','C6-res']
    
    for time_perc in time_perc_list:
        while len(time_perc) < len(metrics):
            time_perc.append(0)
        for i, res in enumerate(time_perc):
            instances_raw_measurements[inst_name][qps][metrics[i]].append(res)   
    
    ## RESIDENCY DONE CALCULATE TRANSITIONS
     # determine used C-states
    state_names = ['POLL']
    check_state_names = ['C1', 'C1E', 'C6']
    for state_name in check_state_names:
        if state_name in instances_raw_measurements[inst_name][qps]['residency'][0]['CPU0']:
            state_names.append(state_name)
    
    usage_list = []
    for stat in instances_raw_measurements[inst_name][qps]['residency']:
        usage_list.append(avg_state_usage(stat, range(0, 10)))
    
    instances_raw_measurements[inst_name][qps]['C0-tr'] = []
    instances_raw_measurements[inst_name][qps]['C1-tr'] = []
    instances_raw_measurements[inst_name][qps]['C1E-tr'] = []
    instances_raw_measurements[inst_name][qps]['C6-tr'] = []
    metrics=['C0-tr','C1-tr','C1E-tr','C6-tr']
    
    for usage_el in usage_list:
        while len(usage_el) < len(metrics):
            usage_el.append(0)
        for i, res in enumerate(usage_el):
            instances_raw_measurements[inst_name][qps][metrics[i]].append(res)
    return 

def parse_client_turbostat(client_turbostat_file):
    
    data_dict = {}

    # Open the turbostat output file for reading
    with open(client_turbostat_file, 'r') as file:

        # Read all lines from the file
        lines = file.readlines()

    # Extract header and data rows
    header = lines[0].split()
    data_rows = [line.split() for line in lines[1:]]
    
    # Iterate over data rows
    for row in data_rows:
        
        if "Package" in row or not row:
            continue

        # Extract core and data values
        if row[2] == "-":
            core = -1
        else:
            core = int(row[2])
        
        data_values = {header[i]: float(row[i]) for i in range(3, len(row))}

        # Check if the core already exists in the dictionary
        #print(str(j) + " " + str(core))
        if core in data_dict:
            # Append new values to the existing dictionary
            existing_values = data_dict[core]
            for key, value in data_values.items():
                existing_values[key].append(value)
        else:
            # Create a new entry with the current values
            data_dict[core] = {key: [value] for key, value in data_values.items()}

    # Calculate averages for each metric and core
    averages_dict = {}
    for core, values in data_dict.items():
        averages_dict[core] = {key: statistics.mean(value) for key, value in values.items()}
    
    return averages_dict
    
def parse_server_time(server_stats_dir, qps):

    warmup_file = os.path.join(server_stats_dir, 'memcachedstatswarmup')
    run_file = os.path.join(server_stats_dir, 'memcachedstatsrun')
    warmup_user = 0
    warmup_sys = 0
    run_user = 0
    run_sys = 0

    with open(warmup_file, 'r') as file:
        for line in file:
            if "rusage_user" in line:
                warmup_user = line.split(" ")[2]
            if "rusage_system" in line:
                warmup_sys = line.split(" ")[2]
    
    with open(run_file, 'r') as file:
        for line in file:
            if "rusage_user" in line:
                run_user = line.split(" ")[2]
            if "rusage_system" in line:
                run_sys = line.split(" ")[2]

    all_server_time = ((float(run_sys) - float(warmup_sys)) + (float(run_user) - float(warmup_user))) * 1000000 / 120 / int(qps)
    user_server_time = (float(run_user) - float(warmup_user)) * 1000000 / 120 / int(qps)
    sys_server_time = (float(run_sys) - float(warmup_sys)) * 1000000 / 120 / int(qps)

    return all_server_time, user_server_time, sys_server_time

def parse_cstate_stats(stats_dir):
    stats = {}
    prog = re.compile('(.*)\.(.*)\.(.*)')
    for f in os.listdir(stats_dir):
        m = prog.match(f)
        if m:
            stats_file = os.path.join(stats_dir, f)
            cpu_id = m.group(1)
            state_name = m.group(2)
            metric_name = m.group(3)
            (metric_name, timeseries) = read_timeseries(stats_file)
            add_metric_to_dict(stats, metric_name, timeseries)
    return stats

def parse_power_rapl(power_dir, filename):

    prev_stats, cur_stats = 0, 0
    with open(power_dir + "/" + filename, 'r') as file:
        
        header = next(file) 
        prev_stats = next(file)
        cur_stats = next(file)
        

    final_power =  (int(cur_stats.split(',')[1]) - int(prev_stats.split(',')[1])) / (int(cur_stats.split(',')[0]) - int(prev_stats.split(',')[0])) / 1000000
    
    if final_power < 0:
        return 0
    
    return final_power


def parse_client_time(client_stats_file):
    stats = {}  
      
    with open(client_stats_file, 'r') as f:
        for l in f:
            if l.startswith('#type'):
                stat_names = l.split()[1:]
                read_stats = next(f).split()[1:]
                update_stats = next(f).split()[1:]
                read_stats_dict = {}
                update_stats_dict = {}
                for i, stat_name in enumerate(stat_names):
                    read_stats_dict[stat_name] = float(read_stats[i])
                    update_stats_dict[stat_name] = float(update_stats[i])
                stats['read'] = read_stats_dict
                stats['update'] = update_stats_dict
                
    return stats


def parse_client_throughput(client_stats_file):
    
    with open(client_stats_file, 'r') as f:
        for l in f:
            if l.startswith('Total QPS'):
                return (float(l.split()[3]))


def parse_single_instance_stats(stats,stats_dir, qps):
    
    run = int(stats_dir.split("-")[-1])
    
    if "throughput" not in stats:
        stats['throughput'] = []
        stats['avg'] = []
        stats['99th'] = []
        stats['package-0'] = []
        stats['package-1'] = []
        stats['dram-0'] = []
        stats['dram-1'] = []
        stats['residency'] = []
        stats['server-avg-all'] = []
        stats['server-avg-user'] = []
        stats['server-avg-sys'] = []
    
    if "client-pkg-0" not in stats:
        stats['client-pkg-0'] = []
        stats['client-pkg-1'] = []
        stats['client-C1-res-hw-all'] = []
        stats['client-C6-res-hw-all'] = []
        stats['client-C0-res-hw-all'] = []
        stats['client-C1-res-sw-all'] = []
        stats['client-C1E-res-sw-all'] = []
        stats['client-C6-res-sw-all'] = []
        stats['client-C0-res-sw-all'] = []
        stats['client-C1-res-hw-s0'] = []
        stats['client-C6-res-hw-s0'] = []
        stats['client-C0-res-hw-s0'] = []
        stats['client-C1-res-sw-s0'] = []
        stats['client-C1E-res-sw-s0'] = []
        stats['client-C6-res-sw-s0'] = []
        stats['client-C0-res-sw-s0'] = []
        stats['client-C1-res-hw-s1'] = []
        stats['client-C6-res-hw-s1'] = []
        stats['client-C0-res-hw-s1'] = []
        stats['client-C1-res-sw-s1'] = []
        stats['client-C1E-res-sw-s1'] = []
        stats['client-C6-res-sw-s1'] = []
        stats['client-C0-res-sw-s1'] = []
        stats['client-C1-tr-all'] = []
        stats['client-C1E-tr-all'] = []
        stats['client-C6-tr-all'] = []
        stats['client-C1-tr-s0'] = []
        stats['client-C1E-tr-s0'] = []
        stats['client-C6-tr-s0'] = []
        stats['client-C1-tr-s1'] = []
        stats['client-C1E-tr-s1'] = []
        stats['client-C6-tr-s1'] = []

    # Check if client turbostat in files parse turbostat as well with the rest
    client_turbostat_file = os.path.join(stats_dir, 'turbostat_client')
    if os.path.exists(client_turbostat_file):
        temp = parse_client_turbostat(client_turbostat_file)
        if "PkgWatt" in temp[0]:
            stats['client-pkg-0'].insert(run,temp[0]['PkgWatt'])
        else:
            stats['client-pkg-0'].insert(run,0)

        if "PkgWatt" in temp[10]:
            stats['client-pkg-1'].insert(run,temp[10]['PkgWatt'])
        else:
            stats['client-pkg-1'].insert(run,0)

        if r"CPU%c1" in temp[-1]:
            stats['client-C1-res-hw-all'].insert(run,temp[-1][r'CPU%c1'])
        else:
            stats['client-C1-res-hw-all'].insert(run,0)

        if r"CPU%c6" in temp[-1]:
            stats['client-C6-res-hw-all'].insert(run,temp[-1][r'CPU%c6'])
        else:
            stats['client-C6-res-hw-all'].insert(run,0)
        
        stats['client-C0-res-hw-all'].insert(run,100-stats['client-C6-res-hw-all'][-1] - stats['client-C1-res-hw-all'][-1])

        if "C1%" in temp[-1]:
            stats['client-C1-res-sw-all'].insert(run,temp[-1]['C1%'])
        else:
            stats['client-C1-res-sw-all'].insert(run,0)
        
        if "C1E%" in temp[-1]:
            stats['client-C1E-res-sw-all'].insert(run,temp[-1]['C1E%'])
        else:
            stats['client-C1E-res-sw-all'].insert(run,0)

        if "C6%" in temp[-1]:
            stats['client-C6-res-sw-all'].insert(run,temp[-1]['C6%'])
        else:
            stats['client-C6-res-sw-all'].insert(run,0)
        
        stats['client-C0-res-sw-all'].insert(run,100-stats['client-C6-res-sw-all'][-1] - stats['client-C1-res-sw-all'][-1] - stats['client-C1E-res-sw-all'][-1])

        # Socket 0 Residency
        if r"CPU%c1" in temp[0]:
            stats['client-C1-res-hw-s0'].insert(run,temp[0][r'CPU%c1'])
        else:
            stats['client-C1-res-hw-s0'].insert(run,0)

        if r"CPU%c6" in temp[0]:
            stats['client-C6-res-hw-s0'].insert(run,temp[0][r'CPU%c6'])
        else:
            stats['client-C6-res-hw-s0'].insert(run,0)
        
        stats['client-C0-res-hw-s0'].insert(run,100-stats['client-C6-res-hw-s0'][-1] - stats['client-C1-res-hw-s0'][-1])

        if "C1%" in temp[0]:
            stats['client-C1-res-sw-s0'].insert(run,temp[0]['C1%'])
        else:
            stats['client-C1-res-sw-s0'].insert(run,0)
        
        if "C1E%" in temp[0]:
            stats['client-C1E-res-sw-s0'].insert(run,temp[0]['C1E%'])
        else:
            stats['client-C1E-res-sw-s0'].insert(run,0)

        if "C6%" in temp[0]:
            stats['client-C6-res-sw-s0'].insert(run,temp[0]['C6%'])
        else:
            stats['client-C6-res-sw-s0'].insert(run,0)
        
        stats['client-C0-res-sw-s0'].insert(run,100-stats['client-C6-res-sw-s0'][-1] - stats['client-C1-res-sw-s0'][-1] - stats['client-C1E-res-sw-s0'][-1])

        # Socket 1 Residency
        if r"CPU%c1" in temp[10]:
            stats['client-C1-res-hw-s1'].insert(run,temp[10][r'CPU%c1'])
        else:
            stats['client-C1-res-hw-s1'].insert(run,0)

        if r"CPU%c6" in temp[10]:
            stats['client-C6-res-hw-s1'].insert(run,temp[10][r'CPU%c6'])
        else:
            stats['client-C6-res-hw-s1'].insert(run,0)
        
        stats['client-C0-res-hw-s1'].insert(run,100-stats['client-C6-res-hw-s1'][-1] - stats['client-C1-res-hw-s1'][-1])

        if "C1%" in temp[10]:
            stats['client-C1-res-sw-s1'].insert(run,temp[10]['C1%'])
        else:
            stats['client-C1-res-sw-s1'].insert(run,0)
        
        if "C1E%" in temp[10]:
            stats['client-C1E-res-sw-s1'].insert(run,temp[10]['C1E%'])
        else:
            stats['client-C1E-res-sw-s1'].insert(run,0)

        if "C6%" in temp[10]:
            stats['client-C6-res-sw-s1'].insert(run,temp[10]['C6%'])
        else:
            stats['client-C6-res-sw-s1'].insert(run,0)
        
        stats['client-C0-res-sw-s1'].insert(run,100-stats['client-C6-res-sw-s1'][-1] - stats['client-C1-res-sw-s1'][-1] - stats['client-C1E-res-sw-s1'][-1])

        # Transitions
        if "C1" in temp[-1]:
            stats['client-C1-tr-all'].insert(run,temp[-1]['C1'])
        else:
            stats['client-C1-tr-all'].insert(run,0)
        
        if "C1E" in temp[-1]:
            stats['client-C1E-tr-all'].insert(run,temp[-1]['C1E'])
        else:
            stats['client-C1E-tr-all'].insert(run,0)

        if "C6" in temp[-1]:
            stats['client-C6-tr-all'].insert(run,temp[-1]['C6'])
        else:
            stats['client-C6-tr-all'].insert(run,0)

        # Socket 0 Transitions
        if "C1" in temp[0]:
            stats['client-C1-tr-s0'].insert(run,temp[0]['C1'])
        else:
            stats['client-C1-tr-s0'].insert(run,0)
        
        if "C1E" in temp[0]:
            stats['client-C1E-tr-s0'].insert(run,temp[0]['C1E'])
        else:
            stats['client-C1E-tr-s0'].insert(run,0)

        if "C6" in temp[0]:
            stats['client-C6-tr-s0'].insert(run,temp[0]['C6'])
        else:
            stats['client-C6-tr-s0'].insert(run,0)
        
        # Socket 1 Residency
        if "C1" in temp[10]:
            stats['client-C1-tr-s1'].insert(run,temp[10]['C1'])
        else:
            stats['client-C1-tr-s1'].insert(run,0)
        
        if "C1E" in temp[10]:
            stats['client-C1E-tr-s1'].insert(run,temp[10]['C1E'])
        else:
            stats['client-C1E-tr-s1'].insert(run,0)

        if "C6" in temp[10]:
            stats['client-C6-tr-s1'].insert(run,temp[10]['C6'])
        else:
            stats['client-C6-tr-s1'].insert(run,0)
        

    client_stats_file = os.path.join(stats_dir, 'mcperf')
    qps_temp = parse_client_throughput(client_stats_file)
    stats['throughput'].insert(run, qps_temp)
    
    # if (float(qps) - float(qps_temp)) > 50000:
    #     stats['throughput'].pop(run)
    #     if stats['client-pkg-0']:
    #         stats['client-pkg-0'].pop(run)
    #         stats['client-pkg-1'].pop(run)
    #         stats['client-C1-res-hw-all'].pop(run)
    #         stats['client-C6-res-hw-all'].pop(run)
    #         stats['client-C0-res-hw-all'].pop(run)
    #         stats['client-C1-res-sw-all'].pop(run)
    #         stats['client-C1E-res-sw-all'].pop(run)
    #         stats['client-C6-res-sw-all'].pop(run)
    #         stats['client-C0-res-sw-all'].pop(run)
    #         stats['client-C1-res-hw-s0'].pop(run)
    #         stats['client-C6-res-hw-s0'].pop(run)
    #         stats['client-C0-res-hw-s0'].pop(run)
    #         stats['client-C1-res-sw-s0'].pop(run)
    #         stats['client-C1E-res-sw-s0'].pop(run)
    #         stats['client-C6-res-sw-s0'].pop(run)
    #         stats['client-C0-res-sw-s0'].pop(run)
    #         stats['client-C1-res-hw-s1'].pop(run)
    #         stats['client-C6-res-hw-s1'].pop(run)
    #         stats['client-C0-res-hw-s1'].pop(run)
    #         stats['client-C1-res-sw-s1'].pop(run)
    #         stats['client-C1E-res-sw-s1'].pop(run)
    #         stats['client-C6-res-sw-s1'].pop(run)
    #         stats['client-C0-res-sw-s1'].pop(run)
    #         stats['client-C1-tr-all'].pop(run)
    #         stats['client-C1E-tr-all'].pop(run)
    #         stats['client-C6-tr-all'].pop(run)
    #         stats['client-C1-tr-s0'].pop(run)
    #         stats['client-C1E-tr-s0'].pop(run)
    #         stats['client-C6-tr-s0'].pop(run)
    #         stats['client-C1-tr-s1'].pop(run)
    #         stats['client-C1E-tr-s1'].pop(run)
    #         stats['client-C6-tr-s1'].pop(run)
    #     return

    client_time_stats = {}
    client_time_stats = parse_client_time(client_stats_file)
    stats['avg'].insert(run,client_time_stats['read']['avg'])
    stats['99th'].insert(run,client_time_stats['read']['p99'])
    
    power_dir = os.path.join(stats_dir, 'memcached')
    stats['package-0'].insert(run,parse_power_rapl(power_dir, "package-0"))
    stats['package-1'].insert(run,parse_power_rapl(power_dir, "package-1"))
    stats['dram-0'].insert(run,parse_power_rapl(power_dir, "dram-0"))
    stats['dram-1'].insert(run,parse_power_rapl(power_dir, "dram-1"))

    residency_dir = os.path.join(stats_dir, 'memcached')
    stats['residency'].insert(run,parse_cstate_stats(residency_dir))

    server_stats_dir = stats_dir
    all_time, user_time, sys_time = parse_server_time(server_stats_dir, qps)
    stats['server-avg-all'].insert(run,all_time)
    stats['server-avg-user'].insert(run,user_time)
    stats['server-avg-sys'].insert(run,sys_time)
   

def parse_multiple_instances_stats(exp_dir, pattern='.*'):
    
    instances_raw_measurements = {}
    exp_name = exp_dir.split("/")[-1]
    
    dirs = list(os.listdir(exp_dir))
    dirs.sort()

    for conf in dirs:   
        
        instance_dir = os.path.join(exp_dir, conf)
        
        #check if experiment run is a directory and contains a directory with the name memcached and contains turbo in name
        if "turbo" not in conf or not os.path.isdir(instance_dir) or not os.path.isdir(os.path.join(instance_dir, "memcached")):
            continue
        
        instance_name = conf[:conf.rfind('-')]
        qps = int(instance_name.split("=")[-1])
        instance_name = instance_name[:instance_name.rfind('-')]
       
        if not os.path.isdir(exp_dir):
            continue

        if instance_name not in instances_raw_measurements:
            instances_raw_measurements[instance_name] = {}
        if qps not in instances_raw_measurements[instance_name]:
            instances_raw_measurements[instance_name][qps] = {}
       
        parse_single_instance_stats(instances_raw_measurements[instance_name][qps],instance_dir, qps)
        
    # calculate statistics for residency in order to find the average per CPU etc....
    for inst_name in instances_raw_measurements:
        for qps in instances_raw_measurements[inst_name]:
            calculate_cstate_stats(instances_raw_measurements, inst_name, qps)

    return instances_raw_measurements

def parse_multiple_exp_stats(stats_dir, pattern='.*'):

    # extract data
    overall_raw_measurements = {}
    for f in os.listdir(stats_dir):
        exp_dir = os.path.join(stats_dir, f)
        if not os.path.isdir(exp_dir):
            continue

        #get configuration for experiment and parse raw data 
        overall_raw_measurements.setdefault(f, []).append(parse_multiple_instances_stats(exp_dir))
    
    #parse statistics
    overall_statistics = {}
    for exp_name in overall_raw_measurements:
        overall_statistics.setdefault(exp_name, []).append(calculate_stats_multiple_instances(exp_name,overall_raw_measurements))

    # Calculate the speedup statistics between experiments for example
    # if we have two scenarios SMTon/off calculate percentage of improvement for all x runs and then calculate median
    # and confidence interval. 

    speedup_statistics = {}
    temp_raw = {}
    for key, value in overall_raw_measurements.items():
        for conf in value:
            for conf_key,conf_val in conf.items():
                temp_raw[str(key) + "-" + str(conf_key)] = conf_val
    
    # pairs = list(combinations(temp_raw.items(), 2))
    # if not (len(temp_raw) == 1):
    #     for pair in pairs:
    #     # Access the first and second items within each tuple
    #         first_item = pair[0]
    #         second_item = pair[1]
    #         speedup_statistics.setdefault(str(first_item[0]) + "-" + str(second_item[0]), []).append(calculate_speedup_stats_multiple_instances(str(first_item[0]) + "-" + str(second_item[0]), first_item[1], second_item[1]))    
    
    # print_speedup_metrics(stats_dir, speedup_statistics, "speedup_metrics.csv" )
    print(stats_dir)
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "throughput", "overall_throughput_time.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "avg", "overall_average_time.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "99th", "overall_99th_time.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "package-0", "overall_package_0.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "package-1", "overall_package_1.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "dram-0", "overall_dram_0.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "dram-1", "overall_dram_1.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "C0-res", "overall_c0_res.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "C1-res", "overall_c1_res.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "C1E-res", "overall_c1e_res.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "C6-res", "overall_c6_res.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "C0-tr", "overall_c0_tr.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "C1-tr", "overall_c1_tr.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "C1E-tr", "overall_c1e_tr.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "C6-tr", "overall_c6_tr.csv")
    print_residency_merged(stats_dir, overall_raw_measurements, overall_statistics, "residency", "overall_residency.csv")
    print_transition_merged(stats_dir, overall_raw_measurements, overall_statistics, "transition", "overall_transition.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "server-avg-all", "overall_server_all.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "server-avg-user", "overall_server_user.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "server-avg-sys", "overall_server_sys.csv")
    print_all_metrics(stats_dir, overall_raw_measurements, overall_statistics, "all-metrics.csv")

    return overall_raw_measurements


def main(argv):
    stats_root_dir = argv[1]
    stats = parse_multiple_exp_stats(stats_root_dir)
        
if __name__ == '__main__':
    main(sys.argv)
