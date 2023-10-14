from logger_process import LoggerProcess
from time import sleep
def sniffer(process: LoggerProcess, active: bool):
    folder = process.folder
    with open(folder, "a") as log:
        while active:
            data = process.read()
            log.write(', '.join(list(map(lambda x: str(x),data))))
            log.write('\n')
            log.flush()
            sleep(1)
        
        
    