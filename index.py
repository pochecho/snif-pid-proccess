import psutil
import os
from helpers import get_process_by_name
from threading import Thread
from sniffer import sniffer
from logger_process import LoggerProcess
from time import sleep

print(os.getpid())

memory_limit = 0.9
cpu_limit = 0.9

mode = 'saving' # standard


if __name__ == "__main__":
    processes = get_process_by_name('riot')
    
    myPID = (os.getpid())
    processes.append({
        'name': 'AMAZING LOGGER',
        'pid': myPID,
    })

    threads_configs = list(map(lambda x: {'alive': True, 'data': x}, processes))
    threads = []
    for thread_config in threads_configs:
        p = LoggerProcess(thread_config['data']['pid'], thread_config['data']['name'])
        t = Thread(target=sniffer, args=(p, thread_config['alive']))
        t.start()
        threads.append(t)
    
    while True:
        memoria = psutil.virtual_memory()
        disco = psutil.disk_usage('/')
        cpu_usage = psutil.cpu_percent(interval=1)  # intervalo de 1 segundo
        red = psutil.net_io_counters()

        print(f"Uso de Memoria: {memoria.percent}%")
        print(f"Uso de Disco: {disco.percent}%")
        print(f"Uso de CPU: {cpu_usage}%")
        print(f"Uso de Red (bytes enviados): {red.bytes_sent} bytes")
        print(f"Uso de Red (bytes recibidos): {red.bytes_recv} bytes")
        print()
        print()
        sleep(1)