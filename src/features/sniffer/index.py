import psutil
import os
from threading import Thread
from features.sniffer.sniffer import sniffer
from features.sniffer.logger_process import LoggerProcess
from core.handler import Handler
from time import sleep
from json import load
import re
import time

memory_limit = 0.9
cpu_limit = 0.9

class SnifferHandler(Handler):
    def __init__(self):
        self.threads = []
        

    def get_process_by_regex(self,name):
        p = re.compile(name)
        iterator = psutil.process_iter(attrs=['pid', 'name'])
        response  = []
        for process in iterator:
            info = process.info
            if(p.search(info['name'].lower()) != None):
                response.append(info)
        return response


    def index(self,full_config):
        config = full_config['features']['sniffer']
        processes = []
        myPID = (os.getpid())
        if(config['sniff-from-file']):
            with (open(config['process-to-sniff-file'])) as f:
                processes =  load(f)
        else:
            process_to_sniff_regex = config['process-to-sniff-regex']
            processes = self.get_process_by_regex(process_to_sniff_regex)
        if(config['sniff-myself']):
            processes.append({
                'name': full_config['name'],
                'pid': myPID,
            })
        log_folder = config['logs-folder']
        if(not os.path.exists(log_folder)):
            os.mkdir(log_folder)

        self.threads_configs = list(map(lambda x: {'alive': True, 'data': x}, processes))
        
        self.counters = len(self.threads_configs)
        
        for thread_config in self.threads_configs:
            p = LoggerProcess(
                pid= thread_config['data']['pid'],
                name= thread_config['data']['name'],
                log_folder=log_folder,
                metrics=config['metrics']
            )
            t = Thread(target=sniffer, args=(p, thread_config))
            t.start()
            self.threads.append(t)
        sniff_host = config['sniff-host']
        if(sniff_host):
            self.counters +=1
            with open(f'{log_folder}/host.log', "a") as log:
                while self.counters > 0:
                    t = time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    memory = psutil.virtual_memory()
                    cpu = psutil.cpu_percent() 
                    red = psutil.net_io_counters()
                    log.write(', '.join(list(map(lambda x: str(x),[t,cpu, memory.percent, red.bytes_sent, red.bytes_recv]))))
                    log.write('\n')
                    log.flush()
                    sleep(1)
        elif((self.counters) > 0):
            while True:
                sleep(1)
        print(f'Finished ')
        
    def exit(self):
        i  = 0
        for t in self.threads_configs:
            t['alive'] = False
            self.threads[i].join()
            self.counters-=1
            i+=1
        self.counters-=1
        return super().exit()
