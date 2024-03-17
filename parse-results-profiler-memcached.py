import os
import pandas as pd
import json
import statistics
import csv 
import sys
import math
import re

#Need to Check confidence interval theory

qps_list = [10000, 50000, 100000, 200000, 300000, 400000, 500000]
z=1.96 # from taming performance variability paper
n=10
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
                        row = []
                        row.append(exp_name)
                        row.append(conf)
                        row.append(qps)
                        row.append(metric)
                        row.append(overall_statistics[exp_name][id][conf][qps]['C0-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['C1-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['C1E-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['C6-res']["avg"])
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
                        row = []
                        row.append(exp_name)
                        row.append(conf)
                        row.append(qps)
                        row.append(metric)
                        row.append(overall_statistics[exp_name][id][conf][qps]['C0-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['C1-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['C1E-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['C6-tr']["avg"])
                        writer.writerow(row)

def print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, metric, filename):

    header = ["exp_name","configuration","qps", "metric", "avg", "median", "stdev", "cv", "ci-min", "ci-max"]
   
    for exp_name in overall_raw_measurements:
        for conf_list in overall_raw_measurements[exp_name]:
            for id,conf in enumerate(list(conf_list.keys())):
                for qps in qps_list:
                    size = len(overall_raw_measurements[exp_name][id][conf][qps][metric])
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
                        row = []
                        row.append(exp_name)
                        row.append(conf)
                        row.append(qps)
                        row.append(metric)
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["median"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["stdev"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["cv"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["ci"]["min"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["ci"]["max"])
                        for meas in overall_raw_measurements[exp_name][id][conf][qps][metric]:
                            row.append(meas)
                        
                        writer.writerow(row)

def confidence_interval_mean (metric_measurements):
    # temp_list  = metric_measurements
    # temp_list.sort()
    sum_m_n = 0
    sum_s_n = 0

    #calculate m_n first

    for x in metric_measurements:
        sum_m_n = sum_m_n + x

    m_n = 1/n * (sum_m_n)

    for x in metric_measurements:
        sum_s_n = sum_s_n + ((x-m_n) * (x-m_n))
    
    sum_s_n = 1/n * (sum_s_n)
    s_n = math.sqrt(sum_s_n)

    min_val = m_n - z * (s_n/math.sqrt(n))
    max_val = m_n + z * (s_n/math.sqrt(n))

    return min_val, max_val

def coefficient_of_variation(metric_measurements):
    return statistics.stdev(metric_measurements) / statistics.median(metric_measurements)

def standard_deviation(metric_measurements):
    return statistics.stdev(metric_measurements)

def median(metric_measurements):
    return statistics.median(metric_measurements)

def average(metric_measurements):
    return statistics.mean(metric_measurements)

def calculate_stats_single_instance(instance_stats, instance_raw_measurements):

    for qps in instance_raw_measurements[list(instance_raw_measurements.keys())[0]]:
        instance_stats[qps] = {}
        for metric in instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps]:
            
            if metric != "residency": 
                instance_stats[qps][metric] = {}
                #calculate statistics    
                instance_stats[qps][metric]['avg'] = average(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                instance_stats[qps][metric]['median'] = median(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                instance_stats[qps][metric]['stdev'] = standard_deviation(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                if instance_stats[qps][metric]['median'] > 0:
                    instance_stats[qps][metric]['cv'] = coefficient_of_variation(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                else:
                    instance_stats[qps][metric]['cv'] = 0
                instance_stats[qps][metric]['ci'] = {}
                instance_stats[qps][metric]['ci']['min'], instance_stats[qps][metric]['ci']['max'] = confidence_interval_mean(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
            

def calculate_stats_multiple_instances(exp_name,overall_raw_measurements):

    instances_stats = {}
    
    for ind,instance in enumerate(overall_raw_measurements[exp_name]):
        
        instances_stats[list(instance.keys())[0]] = {}
        calculate_stats_single_instance(instances_stats[list(instance.keys())[0]], overall_raw_measurements[exp_name][ind])
    
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
        for i, res in enumerate(usage_el):
            instances_raw_measurements[inst_name][qps][metrics[i]].append(res)
    return 

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
    
    client_stats_file = os.path.join(stats_dir, 'mcperf')
    stats['throughput'].append(parse_client_throughput(client_stats_file))
    
    client_time_stats = {}
    client_time_stats = parse_client_time(client_stats_file)
    stats['avg'].append(client_time_stats['read']['avg'])
    stats['99th'].append(client_time_stats['read']['p99'])
    
    power_dir = os.path.join(stats_dir, 'memcached')
    stats['package-0'].append(parse_power_rapl(power_dir, "package-0"))
    stats['package-1'].append(parse_power_rapl(power_dir, "package-1"))
    stats['dram-0'].append(parse_power_rapl(power_dir, "dram-0"))
    stats['dram-1'].append(parse_power_rapl(power_dir, "dram-1"))

    residency_dir = os.path.join(stats_dir, 'memcached')
    stats['residency'].append(parse_cstate_stats(residency_dir))

    server_stats_dir = stats_dir
    all_time, user_time, sys_time = parse_server_time(server_stats_dir, qps)
    stats['server-avg-all'].append(all_time)
    stats['server-avg-user'].append(user_time)
    stats['server-avg-sys'].append(sys_time)

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

    return overall_raw_measurements


def main(argv):
    stats_root_dir = argv[1]
    stats = parse_multiple_exp_stats(stats_root_dir)
        
if __name__ == '__main__':
    main(sys.argv)
