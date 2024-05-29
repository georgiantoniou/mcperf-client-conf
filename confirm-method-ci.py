#############################################################################################
# This script implements the CONFIRM method from the paper "Taming Performance Variability"
# published in USENIX OSDI 2018. The method calculates the number of runs required to gain
# statistical confidence in the case where we have a variable that follows a non parametric 
# distribution in our case the parameter is the average response time of a system. Based on 
# the method, for a set of collected measurments X with n values we select a subset s <=n for
# which we estimate the confidence interval for the median. Then we shuffle x and select a 
# new subset of size s. After we repeat this process c times we calculate the means of the 
# lower and upper CI bounds. The c time picked in the papers is 200. Furthermore the subset
# size s starts from 10 runs and goes upto the number that will lead to confidence intervals 
# with less than 1% error and 95% confidence. If not then the specific variable cannot converge.
# 
# The input passed to the scripts is in the form of experiment_name,run1,run2,run3,....
# The output is the sample size s, the medians of all s subsets and the CI. 

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


def perform_CONFIRM(raw_data):

    for key,value in raw_data.items():
        print(key)
        for s in range(10,len(value)):
            min_temp = []
            max_temp = []
            median_all = []
            for c in range(0,200):
                temp = random.sample(value, s)
                min_meas,max_meas = confidence_interval_mean(temp,s)
                median_all.append(statistics.median(temp))
                min_temp.append(min_meas)
                max_temp.append(max_meas)
            median_str = str(s)
            for meas in median_all:
                median_str = median_str + "," + str(meas)
            median_str = median_str + "," + str(statistics.mean(min_temp)) + "," + str(statistics.mean(max_temp))       
            print(median_str)

def read_data(raw_file):

    raw_data = {}
    with open(raw_file, 'r') as f:
        for l in f:
            line = l.split(",")
            raw_data[str(line[0]) + "-" + str(line[1])] = []
            for meas in line[2:]:
                raw_data[str(line[0]) + "-" + str(line[1])].append(float(meas.strip()))
    return raw_data

def main(argv):
    raw_file = argv[1]
    raw_data = read_data(raw_file)
    perform_CONFIRM(raw_data)
        
if __name__ == '__main__':
    main(sys.argv)