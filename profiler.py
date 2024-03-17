from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import argparse
import functools
import logging
import os
import sys
import socket
import time
import threading
import subprocess 
from subprocess import call
import re
import math

# TODO: ProfilerGroup has a tick thread that wakes up at the minimum sampling period and wakes up each profiler if it has to wake up
# TODO: Use sampling period and sampling length
# def power_state_diff(new_vector, old_vector):
#     diff = []
#     for (new, old) in zip(new_vector, old_vector):
#         diff.append([x[0] - x[1] for x in zip(new, old)])
#     return diff
 
class EventProfiling:
    def __init__(self, sampling_period = 0, sampling_length = 1):
        self.terminate_thread = threading.Condition()
        self.is_active = False
        self.sampling_period = sampling_period
        self.sampling_length = sampling_length

    def profile_thread(self):
        logging.info("Profiling thread started")
        self.terminate_thread.acquire()
        while self.is_active:
            timestamp = str(int(time.time()))
            self.terminate_thread.release()
            self.sample(timestamp)
            self.terminate_thread.acquire()
            if self.is_active:
                self.terminate_thread.wait(timeout=self.sampling_period - self.sampling_length)
        self.terminate_thread.release()
        timestamp = str(int(time.time()))
        self.zerosample(timestamp)
        logging.info("Profiling thread terminated")

    def start(self):
        
        self.clear()
        if self.sampling_period:
            
            self.is_active=True
            self.thread = threading.Thread(target=EventProfiling.profile_thread, args=(self,))
            self.thread.daemon = True
            self.thread.start()
        else:
            
            timestamp = str(int(time.time()))
            self.sample(timestamp)

    def stop(self):
        if self.sampling_period:
            self.terminate_thread.acquire()
            self.interrupt_sample()
            self.is_active=False
            self.terminate_thread.notify()
            self.terminate_thread.release()
        else:
            timestamp = str(int(time.time()))
            self.sample(timestamp)

class InterruptsProfiling(EventProfiling):
    interrupt_path = '/proc/interrupts'

    def __init__(self, sampling_period=0):
        super().__init__(sampling_period)
        self.timeseries = {}

    def sample(self, timestamp):
        interrupt_path = InterruptsProfiling.interrupt_path
        output = open(interrupt_path,"r").readlines()

        #for each interrupt type
        for l in output[1:]:
            key = "INTR.{}".format(l.split()[0].replace(":",""))
            value = ' '.join(l.split()[1:len(output[0].split())+1])
            
            # #for each core
            # for i in range(0,len(output[0].split())):
            #     if (i+1) >= len(l.split()):
            #         break
            #     key = "INTR.CPU{}.{}".format(str(i), l.split()[0].replace(":",""))
            #     value = l.split()[i+1]
            self.timeseries.setdefault(key, []).append((timestamp, value))
    
    def interrupt_sample(self):
        pass

    def zerosample(self, timestamp):
        pass

    def clear(self):
        self.timeseries = {}

    def report(self):
        return self.timeseries

class MpstatProfiling(EventProfiling):
    def __init__(self, sampling_period=1, sampling_length=1):
        super().__init__(sampling_period, sampling_length)
        self.timeseries = {}
        self.timeseries['MPSTAT'] = []
       

    def sample(self, timestamp):
        flag = False
        cmd = ['mpstat', '-P', 'ALL' , '-u', str(self.sampling_length), '1']
        result = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        lines = result.stdout.decode('utf-8').splitlines() + result.stderr.decode('utf-8').splitlines()
        for l in lines:
            if "Average:" in l and "CPU" in l and "usr" in l and "idle" in l:
                flag = True
                metrics = l.split()
                continue
            elif "Average:" in l and "NODE" in l or "Average:" in l and "intr/s" in l:
                break
            if flag and "Average" in l:
                cpu_id = l.split()[1]
                value = ' '.join(l.split()[2:])
                key = "MPSTAT.CPU{}".format(cpu_id) 
                self.timeseries.setdefault(key, []).append((timestamp, value))

                # #%usr
                #metric = metrics[2].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[2]
                #self.timeseries.setdefault(key, []).append((timestamp, value))
                
                # #%nice
                #metric = metrics[3].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[3]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

                # #%sys
                #metric = metrics[4].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[4]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

                # #%iowait
                #metric = metrics[5].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[5]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

                # #irq
                #metric = metrics[6].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[6]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

                # #soft 
                #metric = metrics[7].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[7]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

                # #steal 
                #metric = metrics[8].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[8]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

                # #guest 
                #metric = metrics[9].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[9]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

                # #gnice 
                #metric = metrics[10].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[10]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

                # #idle 
                #metric = metrics[11].replace("%", "") 
                #key = "MPSTAT.CPU{}.{}".format(cpu_id, metric)
                #value = l.split()[11]
                #self.timeseries.setdefault(key, []).append((timestamp, value))

        return  

    def interrupt_sample(self):
        pass

    def zerosample(self, timestamp):
        pass

    def clear(self):
        self.timeseries = {}
        self.timeseries['MPSTAT'] = []

    def report(self):
        return self.timeseries

class PerfEventProfiling(EventProfiling):
    def __init__(self, sampling_period=1, sampling_length=1):
        super().__init__(sampling_period, sampling_length)
        self.perf_path = self.find_perf_path()
        logging.info('Perf found at {}'.format(self.perf_path)) 
        # get microarchitectural events 
        self.events = PerfEventProfiling.get_microarchitectural_events()
        
        # self.events = self.get_perf_power_events()
        #self.events = ['LLC-load-misses']
        # pgrep memcached
        # self.pid = memcached
        self.timeseries = {}
        for e in self.events:
            self.timeseries[e] = []

        #get pid of memcached    
        cmd = ['pgrep', 'memcached']
        result = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = result.stdout.decode('utf-8').splitlines() + result.stderr.decode('utf-8').splitlines()
        self.pid=out[0]

    @staticmethod
    def get_microarchitectural_events():
        events = []
        events.append('LLC-load-misses')
        return events

    def find_perf_path(self):
        kernel_uname = os.popen('uname -a').read().strip()
        if '4.15.0-159-generic' in kernel_uname:
            return '/mydata/linux-4.15.18/perf'
        else:
            return '/usr/bin/perf'
            

    def get_perf_power_events(self):
        events = []
        result = subprocess.run([self.perf_path, 'list'], stdout=subprocess.PIPE)
        for l in result.stdout.decode('utf-8').splitlines():
            l = l.lstrip()
            m = re.match("(power/energy-.*/)\s*\[Kernel PMU event]", l)
            if m:
                events.append(m.group(1))
        return events

    def sample(self, timestamp):
        #LLC-load-misses

        events_str = ','.join(self.events)
        cmd = ['sudo', self.perf_path, 'stat', '-e', events_str, '-p', self.pid, 'sleep', str(self.sampling_length)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out = result.stdout.decode('utf-8').splitlines() + result.stderr.decode('utf-8').splitlines()
        for e in self.events:
            for l in out:
                l = l.lstrip()
                m = re.match("(.*)\s+.*\s+{}".format(e), l)
                if m:
                    value = m.group(1)
                    self.timeseries[e].append((timestamp, str(float(value.replace(',', '')))))
    
    # FIXME: Currently, we add a dummy zero sample when we finish sampling. 
    # This helps us to determine the sampling duration later when we analyze the stats
    # It would be nice to have a more clear solution
    def zerosample(self, timestamp):
        for e in self.events:
            self.timeseries[e].append((timestamp, str(0.0)))

    def interrupt_sample(self):
        os.system('sudo pkill -2 sleep')

    def clear(self):
        self.timeseries = {}
        for e in self.events:
            self.timeseries[e] = []

    def report(self):
        return self.timeseries


class StateProfiling(EventProfiling):
    cpuidle_path = '/sys/devices/system/cpu/cpu0/cpuidle/'

    def __init__(self, sampling_period=0):
        super().__init__(sampling_period)
        self.state_names = StateProfiling.power_state_names()
        self.timeseries = {}

    @staticmethod
    def power_state_names():
        cpuidle_path = StateProfiling.cpuidle_path
        if not os.path.exists(cpuidle_path):
            return []
        state_names = []
        states = os.listdir(cpuidle_path)
        states.sort()
        for state in states:
            state_name_path = os.path.join(cpuidle_path, state, 'name')
            with open(state_name_path) as f:
                state_names.append(f.read().strip())
        return state_names

    @staticmethod
    def power_state_metric(cpu_id, state_id, metric):
        cpuidle_path = StateProfiling.cpuidle_path
        if not os.path.exists(cpuidle_path):
            return None
        output = open("/sys/devices/system/cpu/cpu{}/cpuidle/state{}/{}".format(cpu_id, state_id, metric)).read()
        return output.strip()

    def sample_power_state_metric(self, metric, timestamp):
        for cpu_id in range(0, os.cpu_count()):
            for state_id in range(0, len(self.state_names)):
                state_name = self.state_names[state_id]
                key = "CPU{}.{}.{}".format(cpu_id, state_name, metric)
                value = StateProfiling.power_state_metric(cpu_id, state_id, metric)
                self.timeseries.setdefault(key, []).append((timestamp, value))

    def sample(self, timestamp):
        self.sample_power_state_metric('usage', timestamp)
        self.sample_power_state_metric('time', timestamp)

    def interrupt_sample(self):
        pass

    def zerosample(self, timestamp):
        pass

    def clear(self):
        self.timeseries = {}

    def report(self):
        return self.timeseries

class RaplCountersProfiling(EventProfiling):
    raplcounters_path = '/sys/class/powercap/intel-rapl/'   

    def __init__(self, sampling_period=0):
        super().__init__(sampling_period)
        self.domain_names = {}
        self.domain_names = RaplCountersProfiling.power_domain_names()
        self.timeseries = {}

    @staticmethod
    def power_domain_names():
        raplcounters_path = RaplCountersProfiling.raplcounters_path
        if not os.path.exists(raplcounters_path):
            return []
        domain_names = {}
        
        #Find all supported domains of the system
        for root, subdirs, files in os.walk(raplcounters_path):
            for subdir in subdirs:
                if "intel-rapl" in subdir:
                    if "dram" in open("{}/{}/{}".format(root, subdir,'name'), "r").read().strip() and "1" in subdir:
                        domain_names[open("{}/{}/{}".format(root, subdir,'name'), "r").read().strip() + "-1"]= os.path.join(root,subdir,'energy_uj')
                    elif "dram" in open("{}/{}/{}".format(root, subdir,'name'), "r").read().strip() and "0" in subdir: 
                        domain_names[open("{}/{}/{}".format(root, subdir,'name'), "r").read().strip() + "-0"]= os.path.join(root,subdir,'energy_uj')
                    else: 
                        domain_names[open("{}/{}/{}".format(root, subdir,'name'), "r").read().strip()]= os.path.join(root,subdir,'energy_uj')
        return domain_names

   
    def sample(self, timestamp):
         for domain in self.domain_names:
                value = open(self.domain_names[domain], "r").read().strip()
                self.timeseries.setdefault(domain, []).append((timestamp, value))
       

    def interrupt_sample(self):
        pass

    def zerosample(self, timestamp):
        pass

    def clear(self):
        self.timeseries = {}

    def report(self):
        return self.timeseries

class ProfilingService:
    def __init__(self, profilers):
        self.profilers = profilers
        
    def start(self):
        
        for p in self.profilers:
            print(p)
            p.start()
           
    def stop(self):
        for p in self.profilers:
            p.stop()       

    def report(self):
        timeseries = {}
        for p in self.profilers:
            t = p.report()
            timeseries = {**timeseries, **t}
        return timeseries

    def set(self, kv):
        print(kv)
        

def server(port,perf_iteration):
    state_profiling = StateProfiling(sampling_period=0)
    rapl_profiling = RaplCountersProfiling(sampling_period=0)
    perf_profiling = PerfEventProfiling(sampling_period=10, sampling_length=10)
    mpstat_profiling = MpstatProfiling(sampling_period=10, sampling_length=10)
    interrupt_profiling = InterruptsProfiling(sampling_period=0)
    profiling_service = ProfilingService([ state_profiling, rapl_profiling])
    #profiling_service = ProfilingService([perf_profiling])
    hostname = socket.gethostname().split('.')[0]
    server = SimpleXMLRPCServer((hostname, port), allow_none=True)
    server.register_instance(profiling_service)
    logging.info("Listening on port {}...".format(port))
    server.serve_forever()

class StartAction:
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser('start', help = "Start profiling")
        parser.set_defaults(func=StartAction.action)

    @staticmethod
    def action(args):
        with xmlrpc.client.ServerProxy("http://{}:{}/".format(args.hostname, args.port)) as proxy:
            proxy.start()

class StopAction:
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser('stop', help = "Stop profiling")
        parser.set_defaults(func=StopAction.action)

    @staticmethod
    def action(args):
        with xmlrpc.client.ServerProxy("http://{}:{}/".format(args.hostname, args.port)) as proxy:
            proxy.stop()

class ReportAction:
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser('report', help = "Report profiling")
        parser.set_defaults(func=ReportAction.action)
        parser.add_argument(
                    "-d", "--directory", dest='directory',
                    help="directory where to output results")

    @staticmethod
    def action(args):
        with xmlrpc.client.ServerProxy("http://{}:{}/".format(args.hostname, args.port)) as proxy:
            stats = proxy.report()
            if args.directory:
                ReportAction.write_output(stats, args.directory)
            else:
                print(stats)

    @staticmethod
    def write_output(stats, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)        
        for metric_name,timeseries in stats.items():
            metric_file_name = metric_name.replace('/', '-')
            metric_file_path = os.path.join(directory, metric_file_name)
            with open(metric_file_path, 'w') as mf:
                mf.write(metric_name + '\n')
                for val in timeseries:
                    mf.write(','.join(val) + '\n')

class SetAction:
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser('set', help = "Set sysfs")
        parser.set_defaults(func=SetAction.action)
        parser.add_argument('-c', dest='command')
        parser.add_argument('rest', nargs=argparse.REMAINDER)

    @staticmethod
    def action(args):
        with xmlrpc.client.ServerProxy("http://{}:{}/".format(args.hostname, args.port)) as proxy:
            proxy.set(args.rest)

def parse_args():
    """Configures and parses command-line arguments"""
    parser = argparse.ArgumentParser(
                    prog = 'profiler',
                    description='profiler',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "-n", "--hostname", dest='hostname',
        help="profiler server hostname")
    parser.add_argument(
        "-p", "--port", dest='port', type=int, default=8000,
        help="profiler server port")
    parser.add_argument(
        "-v", "--verbose", dest='verbose', action='store_true',
        help="verbose")

    parser.add_argument(
        "-i", "--iteration", dest='perf_iteration', type=int, default=1,
        help="perf iteration to choose the right performance counters")

    subparsers = parser.add_subparsers(dest='subparser_name', help='sub-command help')
    actions = [StartAction, StopAction, ReportAction, SetAction]
    for a in actions:
      a.add_parser(subparsers)

    args = parser.parse_args()
    logging.basicConfig(format='%(levelname)s:%(message)s')

    if args.verbose:
        logging.getLogger('').setLevel(logging.INFO)
    else:
        logging.getLogger('').setLevel(logging.ERROR)

    if args.hostname:
        if 'func' in args:
            args.func(args)
        else:
            raise Exception('Attempt to run in client mode but no command is given')
    else:
        server(args.port,args.perf_iteration)

def real_main():
    parse_args()

def main():
    real_main()
    return
    try:
        real_main()
    except Exception as e:
        logging.error("%s %s" % (e, sys.stderr))
        sys.exit(1)

if __name__ == '__main__':
    main()