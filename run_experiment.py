import math
import argparse
import copy
import functools
import logging
import subprocess
import sys
import time 
import os
import configparser
import socket
import common 
from paramiko import SSHClient
from scp import SCPClient



log = logging.getLogger(__name__)
turbostat_monitor = False

def exec_command(cmd):
    logging.info(cmd)
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for l in result.stdout.decode('utf-8').splitlines():
        logging.info(l)
    for l in result.stderr.decode('utf-8').splitlines():
        logging.info(l)
    return result.stdout.decode('utf-8').splitlines()

def run_ansible_playbook(inventory, extravars=None, playbook=None, tags=None):
    extravars = ' '.join(extravars) if extravars else ''
    if tags:
        tags = '--tags "{}"'.format(tags) 
    else:
        tags = ""
    cmd = 'ansible-playbook -v -i {} -e "{}" {} {}'.format(inventory, extravars, tags, playbook)
    print(cmd)
    os.system(cmd)

def set_uncore_freq(conf, freq_mhz):
    freq_hex=format(freq_mhz//100, 'x')
    msr_val = "0x{}{}".format(freq_hex, freq_hex) 
    
    extravars = [
       'MSR_VALUE={}'.format(msr_val)]
    run_ansible_playbook(
       inventory='hosts', 
       extravars=extravars, 
       playbook='ansible/configure.yml')

def set_core_freq(conf, freq_mhz):
    extravars = [
       'CORE_FREQ={}MHz'.format(freq_mhz)]
    run_ansible_playbook(
       inventory='hosts', 
       extravars=extravars, 
       playbook='ansible/configure_core_freq.yml')

def run_socwatch(conf,name):
    extravars = [
        'MONITOR_TIME={}'.format("40"),
        'OUTPUT_FILE={}'.format(name)]
    run_ansible_playbook(
        inventory='hosts',
        extravars=extravars,
        playbook='./ansible/profiler.yml',
        tags='run_socwatch')

def run_socwatch_io(conf,name):
    extravars = [
        'OUTPUT_FILE={}'.format(name)]
    run_ansible_playbook(
        inventory='hosts',
        extravars=extravars,
        playbook='./ansible/profiler.yml',
        tags='run_socwatch_io')

def run_socwatch_hotspots(conf,name):
    extravars = [
        'OUTPUT_FILE={}'.format(name)]
    run_ansible_playbook(
        inventory='hosts',
        extravars=extravars,
        playbook='./ansible/profiler.yml',
        tags='run_socwatch_hotspots')

def run_socwatch_ccstates(conf,name):
    extravars = [
        'MONITOR_TIME={}'.format("100"),
        'OUTPUT_FILE={}'.format(name)]
    run_ansible_playbook(
        inventory='hosts',
        extravars=extravars,
        playbook='./ansible/profiler.yml',
        tags='run_socwatch_ccstates')

def run_profiler(conf,id):
    extravars = [
        'ITERATION={}'.format(id)]
    run_ansible_playbook(
        inventory='hosts', 
        extravars=extravars,
        playbook='ansible/profiler.yml', 
        tags='run_profiler')

def kill_profiler(conf):
    run_ansible_playbook(
        inventory='hosts', 
        playbook='ansible/profiler.yml', 
        tags='kill_profiler')

def run_remote(conf):
    extravars = [
        'WORKER_THREADS={}'.format(conf.memcached_worker_threads), 
        'MEMORY_LIMIT_MB={}'.format(conf.memcached_memory_limit_mb), 
        'PIN_THREADS={}'.format(conf.memcached_pin_threads)]
    run_ansible_playbook(
        inventory='hosts', 
        extravars=extravars, 
        playbook='ansible/mcperf.yml', 
        tags='run_memcached,run_agents')

def run_remote_modified(conf):
    extravars = [
        'WORKER_THREADS={}'.format(conf.memcached_worker_threads), 
        'MEMORY_LIMIT_MB={}'.format(conf.memcached_memory_limit_mb), 
        'PIN_THREADS={}'.format(conf.memcached_pin_threads),
        'MEMCACHED_DELAY={}'.format(conf.memcached_delay)]
    run_ansible_playbook(
        inventory='hosts', 
        extravars=extravars, 
        playbook='ansible/mcperf.yml', 
        tags='run_memcached_modified,run_agents')

def kill_remote(conf):
    extravars = [
        'WORKER_THREADS={}'.format(conf.memcached_worker_threads), 
        'MEMORY_LIMIT_MB={}'.format(conf.memcached_memory_limit_mb), 
        'PIN_THREADS={}'.format(conf.memcached_pin_threads)]
    run_ansible_playbook(
        inventory='hosts', 
        extravars=extravars, 
        playbook='ansible/mcperf.yml', tags='kill_memcached,kill_agents')

def host_is_reachable(host):
  return True if os.system("ping -c 1 {}".format(host)) == 0 else False

def memcached_node():
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('hosts')
    node = list(config['memcached'].items())
    if len(node) > 1:
        raise Exception('Do not support multiple memcached nodes')
    return node[0][0]

def wait_for_remote_node(node):
    while not host_is_reachable(node):
        logging.info('Waiting for remote host {}...'.format(node))
        time.sleep(30)
        pass

def configure_memcached_node(conf):
    node = memcached_node()
    print('ssh -n {} "cd ~/mcperf-client-conf; sudo python3 configure.py -v --turbo={} --kernelconfig={} -v"'.format(node, conf['turbo'], conf['kernelconfig']))
    rc = os.system('ssh -n {} "cd ~/mcperf-client-conf; sudo python3 configure.py -v --turbo={} --kernelconfig={} -v"'.format(node, conf['turbo'], conf['kernelconfig']))
    exit_status = rc >> 8 
    if exit_status == 2:
        logging.info('Rebooting remote host {}...'.format(node))
        os.system('ssh -n {} "sudo shutdown -r now"'.format(node))
        logging.info('Waiting for remote host {}...'.format(node))
        time.sleep(30)
        while not host_is_reachable(node):
            logging.info('Waiting for remote host {}...'.format(node))
            time.sleep(30)
            pass
        os.system('ssh -n {} "cd ~/mcperf-client-conf; sudo python3 configure.py -v --turbo={} --kernelconfig={} -v"'.format(node, conf['turbo'], conf['kernelconfig']))
        if conf['ht'] == False:
        	os.system('ssh -n {} "echo "forceoff" | sudo tee /sys/devices/system/cpu/smt/control"'.format(node))
        os.system('ssh -n {} "sudo cpupower frequency-set -g performance"'.format(node))
        if conf['turbo'] == False:
        	os.system('ssh -n {} "~/mcperf-client-conf/turbo-boost.sh disable"'.format(node))


def agents_list():
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('hosts')
    return [key for key in config['agents']]

def agents_parameter():
    la = ["-a " + a for a in agents_list()]
    return ' '.join(la)

def run_single_experiment(root_results_dir, name_prefix, conf, idx):

    if conf.memcached_delay < 0:
        name = name_prefix + conf.shortname()
    else:
        name = name_prefix + "memcachedelay={}-".format(conf.memcached_delay) + conf.shortname()
    results_dir_name = "{}-{}".format(name, idx)
    results_dir_path = os.path.join(root_results_dir, results_dir_name)
    memcached_results_dir_path = os.path.join(results_dir_path, 'memcached')
   
    # For turbostat
    turbostat_results_dir_path = os.path.join(results_dir_path, 'memcachedserverturbostat')

    # cleanup any processes left by a previous run
    kill_profiler(conf)
    kill_remote(conf)

    # prepare profiler, memcached, and mcperf agents
    if conf.memcached_delay < 0:
        run_remote(conf)
    else:
        run_remote_modified(conf)

    run_profiler(conf,idx)
    
    #wait profiler objects to initialize
    time.sleep(10)

    exec_command("./memcache-perf/mcperf -s node1 --loadonly -r {} "
        "--iadist={} --keysize={} --valuesize={}"
        .format(conf.mcperf_records, conf.mcperf_iadist, conf.mcperf_keysize, conf.mcperf_valuesize))

    # do a warmup run
    stdout = exec_command(
        "./memcache-perf/mcperf -s node1 --noload -B -T 40 -Q 1000 -D 4 -C 4 "
        "{} -c 4 -q {} -t {} -r {} " 
        "--update={} --iadist={} --keysize={} --valuesize={}"
        .format(agents_parameter(), conf.mcperf_warmup_qps, conf.mcperf_warmup_time, conf.mcperf_records, conf.mcperf_set_get_ratio, conf.mcperf_iadist, conf.mcperf_keysize, conf.mcperf_valuesize))    
    
    #create necessary results directory as I have to save statistics before I call profiler report
    if not os.path.exists(root_results_dir):
        print(root_results_dir)
        os.mkdir(root_results_dir)
    if not os.path.exists(results_dir_path):
        print(results_dir_path)
        os.mkdir(results_dir_path)
    if not os.path.exists(memcached_results_dir_path):
        print(memcached_results_dir_path)
        os.mkdir(memcached_results_dir_path) 

    cmd=['/users/ganton12/mcperf-client-conf/scripts/memcached-proc-time.sh']
    result = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out = result.stdout.decode('utf-8').splitlines()
    memcachedstats_results_path_name = os.path.join(results_dir_path, 'memcachedstatswarmup')
    memcached_stats_file = open(memcachedstats_results_path_name, 'w');
    for i in out:
    	memcached_stats_file.write(str(i) + "\n")
    memcached_stats_file.close()

    ##Start Turbostat Measurements
    if turbostat_monitor:
        # kill turbostat from previous experiments
        os.system("sudo pkill turbostat")
        for n in agents_list():
            print(n)
            os.system('ssh -n {} "sudo pkill turbostat"'.format(n))

        time.sleep(5)
        os.system('sudo turbostat --interval 10 --quiet --out /users/ganton12/temp &')
        for n in agents_list():
            os.system('ssh -n {} "sudo turbostat --interval 10 --quiet --out /users/ganton12/temp" &'.format(n))
    
    # do the measured run
    exec_command("python3 ./profiler.py -n node1 start")
    
    #run_socwatch(conf,results_dir_name)
    #run_socwatch_ccstates(conf,results_dir_name)
    #run_socwatch_io(conf,results_dir_name)
    #run_socwatch_hotspots(conf,results_dir_name)
    stdout = exec_command(
        "./memcache-perf/mcperf -s node1 --noload -B -T 40 -Q 1000 -D 4 -C 4 "
        "{} -c 4 -q {} -t {} -r {} "
        "--update={} --iadist={} --keysize={} --valuesize={}"
        .format(agents_parameter(), conf.mcperf_qps, conf.mcperf_time, conf.mcperf_records, conf.mcperf_set_get_ratio, conf.mcperf_iadist, conf.mcperf_keysize, conf.mcperf_valuesize))
    exec_command("python3 ./profiler.py -n node1 stop")
	
    if turbostat_monitor:
        # stop turbostat measurements
        exec_command("sudo pkill turbostat")
        for n in agents_list():
            os.system('ssh -n {} "sudo pkill turbostat"'.format(n))
    
   #check if socwatch is still processing
   # active_socwatch=exec_command("/users/ganton12/mcperf-client-conf/scripts/check-socwatch-status.sh node1")
   # while (int(active_socwatch[0]) > 2):
   #    time.sleep(30)
   #    active_socwatch=exec_command("/users/ganton12/mcperf-client-conf/scripts/check-socwatch-status.sh node1")

    exec_command("python3 ./profiler.py -n node1 report -d {}".format(memcached_results_dir_path))

    mcperf_results_path_name = os.path.join(results_dir_path, 'mcperf')
    with open(mcperf_results_path_name, 'w') as fo:
        for l in stdout:
            fo.write(l+'\n')

    
    # write memcached statistics
    cmd=['/users/ganton12/mcperf-client-conf/scripts/memcached-proc-time.sh']
    result = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out = result.stdout.decode('utf-8').splitlines()
    memcachedstats_results_path_name = os.path.join(results_dir_path, 'memcachedstatsrun')
    memcached_stats_file = open(memcachedstats_results_path_name, 'w');
    for i in out:
    	memcached_stats_file.write(str(i) + "\n")
    memcached_stats_file.close()
    
    if turbostat_monitor:
        # Write turbostat statistics
        with open("/users/ganton12/temp", "r") as file:
            stdout = file.readlines()

        turbostat_client_results_path_name = os.path.join(results_dir_path, 'turbostat_client')
        with open(turbostat_client_results_path_name, 'w') as fo:
            for l in stdout:
                fo.write(l+'\n')

        # write turbostat statistics for agents
        for n in agents_list():
            turbostat_client_results_path_name = os.path.join(results_dir_path, 'turbostat_client_{}'.format(n))
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(str(n))
            # Create an SCP client
            scp = ssh.open_sftp()
            scp.get('/users/ganton12/temp',turbostat_client_results_path_name) # Copy my_file.txt to the server
            scp.close()
            ssh.close()
    #move socwatch statistics to extra space because space at working directory is extremely limited
    #os.system('ssh -n node1 "sudo mkdir /myextraspace/local/data/{}; sudo mv ~/{}* /myextraspace/local/data/{}"'.format(results_dir_name,results_dir_name,results_dir_name))
 
    # cleanup
    kill_remote(conf)
    kill_profiler(conf)

def run_multiple_experiments_with_varying_freq(root_results_dir, batch_name, system_conf, batch_conf, iter):
    configure_memcached_node(system_conf)
    name_prefix = "turbo={}-kernelconfig={}-".format(system_conf['turbo'], system_conf['kernelconfig'])
    request_qps = [10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000]
    root_results_dir = os.path.join(root_results_dir, batch_name)
    set_uncore_freq(system_conf, 1600)
    for freq in [1400, 1600, 1800, 2000, 2200, 2400]:
        set_core_freq(system_conf, freq)
        for qps in request_qps:
            instance_conf = copy.copy(batch_conf)
            instance_conf.set('mcperf_qps', qps)
            instance_conf.set('memcached_freq', freq)
            run_single_experiment(root_results_dir, name_prefix, instance_conf, iter)

def run_multiple_experiments(root_results_dir, batch_name, system_conf, batch_conf, iter):
    ## configure_memcached_node(system_conf)
    #exit()
    ## time.sleep(120)
    #exit()
    name_prefix = "turbo={}-kernelconfig={}-hyperthreading={}-".format(system_conf['turbo'], system_conf['kernelconfig'],system_conf['ht'])
    #request_qps = [10000, 50000, 100000, 200000, 300000, 400000, 500000, 1000000, 2000000]
    request_qps = [10000, 50000, 100000, 200000, 300000, 400000, 500000]
    memcached_delay = [0, 1, 100, 1000, 10000]
    #request_qps = [4000, 10000, 20000, 50000, 100000, 200000, 300000, 400000, 500000]
    #request_qps = [500000, 400000, 300000, 200000, 100000, 50000, 20000, 10000, 4000]
    root_results_dir = os.path.join(root_results_dir, batch_name)
    set_uncore_freq(system_conf, 2000)
    #for freq in [2100]:
    #    set_core_freq(system_conf, freq)
    
    if batch_conf.memcached_delay < 0:
        memcached_delay = [0]
    
    for delay in memcached_delay:  
        for qps in request_qps:
            instance_conf = copy.copy(batch_conf)
            instance_conf.set('mcperf_qps', qps)
            instance_conf.set('memcached_delay', delay)
            #same work experiment
            #time=int(int(instance_conf.mcperf_time)*min(request_qps)/qps)
            #instance_conf.set('mcperf_time',time)
            temp_iter=iter
            iters_cycle=math.ceil(batch_conf.perf_counters/4.0)+1
            for it in range(iters_cycle*(iter),iters_cycle*(iter+1)):
                run_single_experiment(root_results_dir, name_prefix, instance_conf, it)
                time.sleep(20)

def main(argv):
    system_confs = [
##        {'turbo': True,  'kernelconfig': 'vanilla'},
##        {'turbo': False,  'kernelconfig': 'vanilla'},
#         {'turbo': False, 'kernelconfig': 'baseline', 'ht': False},
#          {'turbo': False, 'kernelconfig': 'disable_c6'},
#         {'turbo': True, 'kernelconfig': 'baseline'},
#         {'turbo': False, 'kernelconfig': 'disable_cstates'},
#         {'turbo': False, 'kernelconfig': 'disable_c6', 'ht': False},
#         {'turbo': True, 'kernelconfig': 'disable_c6'},
#          {'turbo': True, 'kernelconfig': 'disable_c1e_c6', 'ht': True},
#          {'turbo': False, 'kernelconfig': 'baseline', 'ht': False},
#          {'turbo': False, 'kernelconfig': 'disable_c6', 'ht': False},
          {'turbo': False, 'kernelconfig': 'disable_c1e_c6', 'ht': False},
#          {'turbo': False, 'kernelconfig': 'disable_cstates', 'ht': False},
#          {'turbo': False, 'kernelconfig': 'baseline', 'ht': False},
#          {'turbo': False, 'kernelconfig': 'disable_c1e_c6', 'ht': False, 'pstate': False},
#          {'turbo': False, 'kernelconfig': 'disable_c1e_c6', 'ht': True},
#         {'turbo': True, 'kernelconfig': 'disable_c1e_c6'},
##         {'turbo': False, 'kernelconfig': 'quick_c1'},
##         {'turbo': True, 'kernelconfig': 'quick_c1'},
##         {'turbo': False, 'kernelconfig': 'quick_c1_disable_c6'},
##         {'turbo': True, 'kernelconfig': 'quick_c1_disable_c6'},
##         {'turbo': False, 'kernelconfig': 'quick_c1_c1e'},
##         {'turbo': True, 'kernelconfig': 'quick_c1_c1e'},
##         {'turbo': True, 'kernelconfig': 'disable_cstates'},
    ]
    batch_conf = common.Configuration({
        'memcached_worker_threads': 10,
        'memcached_memory_limit_mb': 16384,
        'memcached_pin_threads': 'true',
        'mcperf_time': 120,
        'mcperf_warmup_qps': 1000000,
        'mcperf_warmup_time': 1,
        'mcperf_records': 1,
        'mcperf_iadist': 'fb_ia',
        'mcperf_keysize': 'fb_key',
        'mcperf_valuesize': 'fb_value',
        'perf_counters': 0, #21
        'mcperf_set_get_ratio': 0,
        # added for the modified version of memcached set to -1 if memcached normal is used
        'memcached_delay': 0
    })
    
   
    logging.getLogger('').setLevel(logging.INFO)
    if len(argv) < 1:
        raise Exception("Experiment name is missing")
    batch_name = argv[0]
    for iter in range(0, 5):
        for system_conf in system_confs:
            run_multiple_experiments('/users/ganton12/data', batch_name, system_conf, batch_conf, iter)

if __name__ == '__main__':
    main(sys.argv[1:])
