#############################################################################################
# This script calculates stdev, mean, median and CI for ta file with exp, samples structure

import sys
import random
import math
import statistics
z=1.96 # from taming performance variability paper

def confidence_interval_mean (metric_measurements,n):
    temp_list  = metric_measurements.copy()
    temp_list.sort()
     
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

def calculate_metrics(raw_data):
    print("exp,avg,median,stv,ci_min,ci_max,")
    for key,value in raw_data.items():
        min_meas,max_meas = confidence_interval_mean(value,len(value))
        median_meas =  median(value)
        avg_meas = average(value)
        stdv_meas = standard_deviation(value)
        final_str = str(key)
        final_str = final_str + "," + str(avg_meas)
        final_str = final_str + "," + str(median_meas)
        final_str = final_str + "," + str(stdv_meas)
        final_str = final_str + "," + str(min_meas)
        final_str = final_str + "," + str(max_meas)
            
        for meas in value:
            final_str = final_str + "," + str(meas)       
        print(final_str)

def read_data(raw_file):

    raw_data = {}
    with open(raw_file, 'r') as f:
        for l in f:
            line = l.split(",")
            raw_data[str(line[0])] = []
            for meas in line[1:]:
                raw_data[str(line[0])].append(float(meas.strip()))
    return raw_data

def main(argv):
    raw_file = argv[1]
    raw_data = read_data(raw_file)
    calculate_metrics(raw_data)
        
if __name__ == '__main__':
    main(sys.argv)