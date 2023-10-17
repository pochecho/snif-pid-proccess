import matplotlib.pyplot as plt
import os
import argparse
import numpy as np

# Crea un objeto ArgumentParser
parser = argparse.ArgumentParser(argument_default= {'graphic': False })
# Agrega argumentos
parser.add_argument('--graphic','-g', nargs='?',type=str, help='Descripción del primer argumento', default=False)

args = parser.parse_args()

plt.xlabel('Tiempo')
plt.ylabel('MB Memoria')
columns = [
    {
        'display': 'Date',
        'computable': False,
        'color': 'b',
        'visible': False
    },
    {
        'display': 'CPU',
        'computable': True,
        'color': '#897564',
        'visible': True
    },
    {
        'display': 'Memory',
        'computable': True,
        'color': '#1e90ff',
        'visible': True
    },
    {
        'display': 'Net',
        'computable': False,
        'color': '#354',
        'visible': False
    }

]
# Mostrar leyenda

def files_to_plot():
    response = []
    files = os.listdir('logs')

    response = list(map(lambda name: {'path':f'logs/{name}', 'tag': name.split('.')[0] }, files))
    return response

files = files_to_plot()

def getData(config, columns):
    with open(config['path'], 'r') as t:
        content = t.read()
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
                    res.append((d))
                i+=1
            return res
                
        
        content = list(filter(lambda y: len(y) == len(columns), map(lambda x: trim_data(x.split(',')),content)))
    print(content)
    return content

for file in files:
    data = getData(file, columns)
    x = []
    y = []
    c = 0
    graphs = []
    
    plt.title(file['tag'])
    for column in columns: 
        graphs.append({
            'x': [],
            'y': []
        })
        for row in data:
            graphs[c]['x'].append(row[0])
            graphs[c]['y'].append(row[c])
            # Anotar el valor mínimo
        x = graphs[c]['x']
        y = graphs[c]['y']
        if(column['visible']):
            min_y = min(y)
            max_y = max(y)
            average = np.mean(np.array(y))
            plt.annotate(f'Mínimo: {min_y}', xy=(x[y.index(min_y)], min_y), xytext=(20, 10),
                        textcoords='offset points', arrowprops=dict(arrowstyle="->"))

            # Anotar el valor máximo
            plt.annotate(f'Máximo: {max_y}', xy=(x[y.index(max_y)], max_y), xytext=(20, 10),
                        textcoords='offset points', arrowprops=dict(arrowstyle="->"))
            plt.annotate(f'Promedio: {average}', xy=(x[len(x) // 2], average), xytext=(20, 10),
                        textcoords='offset points', arrowprops=dict(arrowstyle="->"))
            plt.plot( x,  y, label=column['display'], marker='o', linestyle='-', color=column['color'])
            
        c+=1
    plt.legend()

    # Mostrar la gráfica
    plt.show()
    
    # Crear una gráfica de líneas
