import psutil
import os
from helpers import get_process_by_name
from threading import Thread
from sniffer import sniffer
from logger_process import LoggerProcess
from time import sleep
import signal
import sys
import json

import argparse

# Crea un objeto ArgumentParser
parser = argparse.ArgumentParser(argument_default= {'file': False, 'fileName': 'pid-to-sniff.json' })
# Agrega argumentos
parser.add_argument('--file','-f', nargs='?',type=str, help='Descripción del primer argumento', default=False)
parser.add_argument('--fileName','-fn',  nargs='?', type=str, help='Descripción del primer argumento', default='pid-to-sniff.json')

args = parser.parse_args()
print(args)
output_logs_folder = 'logs'

file = args.file
fileName = args.fileName

print(file)
print(os.getpid())

memory_limit = 0.9
cpu_limit = 0.9

mode = 'saving' # standard

if __name__ == "__main__":
    try:
        threads = []
        processes = []
        myPID = (os.getpid())
        if(file):
            with (open(fileName)) as f:
                processes =  json.load(f)
        else:
            processes = get_process_by_name('postman')
        processes.append({
            'name': 'AMAZING LOGGER',
            'pid': myPID,
        })
        if(not os.path.exists('logs')):
            os.mkdir('logs')

        threads_configs = list(map(lambda x: {'alive': True, 'data': x}, processes))
        
        
        def signal_handler(sig, frame):
            i  = 0
            for t in threads_configs:
                t['alive'] = False
                threads[i].join()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        
        for thread_config in threads_configs:
            p = LoggerProcess(thread_config['data']['pid'], thread_config['data']['name'])
            t = Thread(target=sniffer, args=(p, thread_config))
            t.start()
            threads.append(t)
        
        while True:
            memoria = psutil.virtual_memory()
            cpu_usage = psutil.cpu_percent(interval=1) 
            red = psutil.net_io_counters()
            print(f"Uso de Memoria: {memoria.percent}%")
            print(f"Uso de CPU: {cpu_usage}%")
            print(f"Uso de Red (bytes enviados): {red.bytes_sent} bytes")
            print(f"Uso de Red (bytes recibidos): {red.bytes_recv} bytes")
            print()
            sleep(1)
    except KeyboardInterrupt:
        print("Capturaste Ctrl+C. Realizando acciones antes de salir...")
        sys.exit(0)