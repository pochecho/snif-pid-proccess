import time
from psutil import Process 


class LoggerProcess:
    def __init__(self,pid, name):
        self.name = name
        self.pid = pid
        self.process = Process(pid)
        self.folder = self.generate_name_folder()
        
    def generate_name_folder(self):
        return f"logs/{self.pid}-{self.name.lower()}.log"
    def read(self):
        cpu = self.process.cpu_percent()
        mem_info = self.process.memory_info()
        net = self.process.io_counters()
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        return t, cpu, mem_info.rss / (1024*1024), net.write_bytes / (1024*1024)