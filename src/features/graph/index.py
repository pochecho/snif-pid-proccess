import math
import matplotlib.pyplot as plt
import os
import argparse
import numpy as np
from core.handler import Handler
from mpldatacursor import datacursor
from datetime import datetime


class GraphicHandler(Handler):
    
    def getData(self,config, columns):
        with open(config['path'], 'r') as t:
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
                        hour = d1.hour
                        minutes = d1.minute
                        seconds = d1.second
                        res.append(f'{hour}:{minutes}:{seconds}')
                    i+=1
                return res
                    
            
            content = list(filter(lambda y: len(y) == len(columns), map(lambda x: trim_data(x.split(',')),content)))
        return content
    def exit(self):
        return super().exit()
    def index(self, ful_config):
        config = ful_config['features']['graph']
        # plt.xlabel('Tiempo')
        # plt.ylabel('MB Memoria')
        columns = config['columns']
        path = config['path']
        # Mostrar leyenda

        def files_to_plot():
            response = []
            files = os.listdir(path)

            response = list(map(lambda name: {'path':f'{path}/{name}', 'tag': name.split('.')[0] }, files))
            return response

        files = files_to_plot()

        for file in files:
            data = self.getData(file, columns)
            x = []
            y = []
            # plt.title(file['tag'])
            valid_columns = list(filter(lambda x: x['visible'], columns))
            rows = math.ceil(len(valid_columns) / 2)
            cols = math.ceil(len(valid_columns) / rows)
            print('****',len(valid_columns) , rows, cols)
            fig, axes = plt.subplots(nrows=rows, ncols= cols)
            r = 0
            cx  = 0 
            for column in valid_columns: 
                c = columns.index(column)
                print(column['display'])
                print(c)
                print()
                x = []
                y = []
                for row in data:
                    x.append(row[0])
                    y.append(row[c])
                    # Anotar el valor mínimo

            
                min_y = min(y)
                max_y = max(y)
                average = np.mean(np.array(y))
                
                
                print('r,cx', r,cx)
                
                axes[r][cx].plot(x, y, label=column['display'])
                axes[r][cx].annotate(f'Mínimo: {min_y}', xy=(x[y.index(min_y)], min_y), xytext=(20, 10),
                            textcoords='offset points', arrowprops=dict(arrowstyle="->"))

                axes[r][cx].annotate(f'Máximo: {max_y}', xy=(x[y.index(max_y)], max_y), xytext=(20, 10),
                            textcoords='offset points', arrowprops=dict(arrowstyle="->"))
                
                axes[r][cx].annotate(f'Promedio: {average}', xy=(x[len(x) // 2], average), xytext=(20, 10),
                            textcoords='offset points', arrowprops=dict(arrowstyle="->"))
                
                axes[r][cx].tick_params(axis='x', labelrotation=90)
                axes[r][cx].legend()
                if(r < rows-1):
                    r+=1
                else:
                    r = 0
                    cx += 1
                    
                # plt.plot( x,  y, label=column['display'], marker='o', linestyle='-', color=column['color'])
                    
            plt.tight_layout()
            # plt.legend()
            # Mostrar la gráfica
            plt.show()
            
            # Crear una gráfica de líneas
        return super().index()
