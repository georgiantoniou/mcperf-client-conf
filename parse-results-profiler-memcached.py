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
            instance_stats[qps][metric] = {}
            #calculate statistics            
            instance_stats[qps][metric]['avg'] = average(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
            instance_stats[qps][metric]['median'] = median(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
            instance_stats[qps][metric]['stdev'] = standard_deviation(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
            instance_stats[qps][metric]['cv'] = coefficient_of_variation(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
            instance_stats[qps][metric]['ci'] = {}
            instance_stats[qps][metric]['ci']['min'], instance_stats[qps][metric]['ci']['max'] = confidence_interval_mean(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])

def calculate_stats_multiple_instances(exp_name,overall_raw_measurements):

    instances_stats = {}
    
    for ind,instance in enumerate(overall_raw_measurements[exp_name]):
        
        instances_stats[list(instance.keys())[0]] = {}
        calculate_stats_single_instance(instances_stats[list(instance.keys())[0]], overall_raw_measurements[exp_name][ind])
    
    return instances_stats

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


def parse_single_instance_stats(stats,stats_dir):
    
    if "throughput" not in stats:
        stats['throughput'] = []
        stats['avg'] = []
        stats['99th'] = []
        stats['package-0'] = []
        stats['package-1'] = []
        stats['dram-0'] = []
        stats['dram-1'] = []
    
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

        parse_single_instance_stats(instances_raw_measurements[instance_name][qps],instance_dir)
        
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


    return overall_raw_measurements


def main(argv):
    stats_root_dir = argv[1]
    stats = parse_multiple_exp_stats(stats_root_dir)
        
if __name__ == '__main__':
    main(sys.argv)
