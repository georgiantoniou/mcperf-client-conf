import os
import pandas as pd
import json
import statistics
import csv 
import sys


qps_list = [10000, 50000, 100000, 200000, 300000, 400000, 500000]
z=1.96 # from taming performance variability paper

def confidence_interval_mean (metric_measurements):
    temp_list  = metric_measurements
    temp_list.sort()
    


def coefficient_of_variation(metric_measurements):
    return statistics.stdev(metric_measurements) / statitsics.median(metric_measurements)

def standard_deviation(metric_measurements):
    return statistics.stdev(metric_measurements)

def median(metric_measurements):
    return statitsics.median(metric_measurements)

def average(metric_measurements):
    return statitsics.mean(metric_measurements) / len(metric_measurements)

def calculate_stats_single_instance(instances_stats, instance_raw_measurements):

    for qps in instance_raw_measurements:
        instances_stats[qps] = {}
        for metric in instance_raw_measurements[qps]:
            instances_stats[qps][metric] = {}
            #calculate statistics            
            instances_stats[qps][metric]['avg'] = average(instances_stats[qps][metric])
            instances_stats[qps][metric]['median'] = median(instances_stats[qps][metric])
            instances_stats[qps][metric]['stdev'] = standard_deviation(instances_stats[qps][metric])
            instances_stats[qps][metric]['cv'] = coefficient_of_variation(instances_stats[qps][metric])
            instances_stats[qps][metric]['ci'] = confidence_interval_mean(instances_stats[qps][metric])

def calculate_stats_multiple_instances(exp_name,overall_raw_measurements):

    instances_stats = {}
    
    for instance in overall_raw_measurements[exp_name]:
        
        instance_stats[instance] = {}
        calculate_stats_single_instance(instances_stats[instance_name], overall_raw_measurements[exp_name][instance])

    return instances_stats


def parse_mcperf_stats(mcperf_results_path):
    stats = None
    with open(mcperf_results_path, 'r') as f:
        stats = {}
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
            if l.startswith('Total QPS'):
                stats['total_qps'] = float(l.split()[3])
    return stats

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
    
    client_stats_file = os.path.join(stats_dir, 'mcperf')
    stats['throughput'].append(parse_client_throughput(client_stats_file))
    
    client_time_stats = {}
    client_time_stats = parse_client_time(client_stats_file)
    stats['avg'].append(client_time_stats['read']['avg'])
    stats['99th'].append(client_time_stats['read']['p99'])
   

def parse_multiple_instances_stats(exp_dir, pattern='.*'):
    
    instances_raw_measurements = {}
    exp_name = exp_dir.split("/")[-1]

    for conf in os.listdir(exp_dir):
        
        instance_dir = os.path.join(exp_dir, conf)
        #check if experiment run is a directory and contains a directory with the name memcached and contains turbo in name
        if "turbo" not in conf or not os.path.isdir(instance_dir) or not os.path.isdir(os.path.join(instance_dir, "memcached")):
            continue

        instance_name = conf[:conf.rfind('-')]
        qps = int(instance_name.split("=")[-1])
        instance_name = instance_name[:instance_name.rfind('-')]
        
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
        overall_statistics.setdefault(f, []).append(calculate_stats_multiple_instances(f,overall_raw_measurements))
        
    
    
    print_stats_
    return overall_raw_measurements


def main(argv):
    stats_root_dir = argv[1]
    stats = parse_multiple_exp_stats(stats_root_dir)
        
if __name__ == '__main__':
    main(sys.argv)