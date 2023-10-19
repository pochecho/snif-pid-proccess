import multiprocessing
import time
from psutil import Process 


class LoggerProcess:
    def __init__(self,pid, name,log_folder, metrics):
        self.metrics = metrics
        self.name = name
        self.pid = pid
        self.log_folder = log_folder
        self.process = Process(pid)
        self.folder = self.generate_name_folder()
        self.metric_handlers ={
            "cpu": self.read_cpu,
            "memory": self.read_memory,
            "paginated-memory": self.read_paginated_memory,
            "net-output": self.read_net_output,
            "net-input": self.read_net_input,
        }
        self.size_parser = {
            'B': lambda x: x,
            'KB': lambda x: x/1024,
            'MB': lambda x: x/(1024*1024),
            'GB': lambda x: x/(1024*1024*1024),
        }

        
    def generate_name_folder(self):
        return f"{self.log_folder}/{self.pid}-{self.name.lower()}.log"
    def read(self):
        response = []
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        response.append(t)
        for m in self.metrics:
            if(m['status'] == 'enabled'):
                d = self.metric_handlers[m['name']](m) 
                response.append(d)
        return response
    
    def read_cpu(self, config):
        cpu = self.process.cpu_percent()
        if(config['absolute']):
            cpu = cpu * 10
        elif(config['normalize']):
            cores = multiprocessing.cpu_count()
            cpu = cpu / cores
        return cpu
    
    def read_memory(self, config):
        mem_info = self.process.memory_info()
        value = mem_info.rss
        return self.size_parser[config['unit']](value)
    
    def read_net_output(self, config):
        io = self.process.io_counters()
        value = io.write_bytes
        return self.size_parser[config['unit']](value)
    
    def read_net_input(self, config):
        io = self.process.io_counters()
        value = io.read_bytes
        return self.size_parser[config['unit']](value)
    
    def read_paginated_memory(self, config):
        mem_info = self.process.memory_info()
        value = mem_info.vms
        return self.size_parser[config['unit']](value)
        
        