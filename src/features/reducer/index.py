import copy
import math
import matplotlib.pyplot as plt
import os
import argparse
import shutil
import numpy as np
from core.handler import Handler
from mpldatacursor import datacursor
from datetime import datetime


class ReducerHandler(Handler):
    
    def exit(self):
        return super().exit()
    
    def getData(self,path, columns):
        with open(path, 'r') as t:
            content = t.read().strip()
            content = content.split('\n')
            def trim_data(x):
                data =  list(map(lambda t: t.strip(), x))
                i = 0
                res = []
                for d in data:
                    column_data = columns[i]
                    if(column_data['computable']):
                        res.append(float(d))
                    else:
                        d1 = datetime.fromisoformat(d)
                        res.append(d1)
                    i+=1
                return res
                    
            
            content = list(filter(lambda y: len(y) == len(columns), map(lambda x: trim_data(x.split(',')),content)))
        return content
    def index(self, ful_config):
        config = ful_config['features']['reducer']
        columns = config['columns']
        from_folder = config['from']
        unit_reducer = {
            's': lambda x: x.second,
            'm': lambda x: x.minute,
            'h': lambda x: x.hour,
        }
        unit_converter = {
            's': 1,
            'm': 60,
            'h': 3600,
        }
        
        files = os.listdir(from_folder)
        
        for f in files:
            path = f'{from_folder}/{f}'
            data = self.getData(path,columns)
            
            if(len(data) > 0): 
                index = 0
                first = data[index]
                if(config['start-exactly']):
                    item,index  = self.get_next_empty(config, data, unit_reducer, index)
                    first = item
                limit = config['range-to-reduce'] * unit_converter[config['unit-to-reduce']]
                
                row = index
                sum = [0] * (len(columns) - 1)
                response = []
                
                while row < len(data):
                    
                    rowData = data[row][1:]
                    sum = [ a + b for a,b in zip(sum, rowData)]
                    if(row % limit == 0):
                        result = [x/limit for x in sum]
                        result.insert(0,data[row][0])
                        response.append(copy.deepcopy(result))
                        sum = [0] * (len(columns )-1)
                        
                        
                    row+=1
                log_folder = config["to"]
                if(os.path.exists(log_folder)):
                    shutil.rmtree(log_folder)
                os.mkdir(log_folder)
                to_path = f'{log_folder}/{f}'
                with open(to_path, 'a') as t:
                    for line in response:
                        t.write(', '.join(list(map(lambda x: str(x),line))))
                        t.write('\n')
                
                
                
            
        
        # plt.xlabel('Tiempo')
        # plt.ylabel('MB Memoria')
        # Mostrar leyenda

        return super().index()

    def get_next_empty(self, config, data, unit_reducer, index):
        date_extractor = unit_reducer[config['unit-to-reduce']]
        found = None
        item = None
        for y in data:
            part = date_extractor(y[0])
            found = part == 0
            if(found):
                item = part
                break
            index += 1
        index-=1
        return item,index
