import matplotlib.pyplot as plt
import os
import argparse

# Crea un objeto ArgumentParser
parser = argparse.ArgumentParser(argument_default= {'graphic': False })
# Agrega argumentos
parser.add_argument('--graphic','-g', nargs='?',type=str, help='Descripción del primer argumento', default=False)

args = parser.parse_args()
print(args)



# Datos de ejemplo
x = [1, 2, 3, 4, 5]
y = [10, 25, 18, 30, 15]


# Agregar etiquetas y título
plt.xlabel('Tiempo')
plt.ylabel('MB Memoria')
columns = [
    {
        'display': 'Date',
        'computable': False,
        'color': 'b'
    },
    {
        'display': 'CPU',
        'computable': True,
        'color': '#897564'
    },
    {
        'display': 'Memory',
        'computable': True,
        'color': '#1e90ff'
    },
    {
        'display': 'Net',
        'computable': True,
        'color': '#354'
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

print(files)

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
            print(row)
            graphs[c]['x'].append(row[0])
            graphs[c]['y'].append(row[c])
            # Anotar el valor mínimo
        x = graphs[c]['x']
        y = graphs[c]['y']
        if(column['computable']):
            min_y = min(y)
            max_y = max(y)
            plt.annotate(f'Mínimo: {min_y}', xy=(x[y.index(min_y)], min_y), xytext=(20, 10),
                        textcoords='offset points', arrowprops=dict(arrowstyle="->"))

            # Anotar el valor máximo
            plt.annotate(f'Máximo: {max_y}', xy=(x[y.index(max_y)], max_y), xytext=(20, 10),
                        textcoords='offset points', arrowprops=dict(arrowstyle="->"))
            plt.plot( x,  y, label=column['display'], marker='o', linestyle='-', color=column['color'])
        c+=1
    
    # Crear una gráfica de líneas

    break
plt.legend()

# Mostrar la gráfica
plt.show()
