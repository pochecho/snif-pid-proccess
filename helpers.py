import psutil
def get_process_by_name(name):
    stats = psutil.cpu_stats()
    iterator = psutil.process_iter(attrs=['pid', 'name'])
    response  = []
    for process in iterator:
        
        info = process.info
        if(name in info['name'].lower()):
            response.append(info)
    return response

def generate_name_folder(process):
    return f"{process['pid']}-{process['name'].lower()}"