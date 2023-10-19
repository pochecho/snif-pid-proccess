

name: El nombre del script de monitoreo, que es "tic-partner". Esto sirve para identificar el script en la configuración.

sniffer: Esta sección configura el módulo "sniffer" del script, que se encarga de supervisar los procesos.

logs-folder: Ruta de la carpeta donde se guardarán los registros de monitoreo.
sniff-myself: Un indicador booleano que especifica si el script debe monitorearse a sí mismo (true) o no (false).
sniff-host: Un indicador booleano que especifica si se deben monitorear los procesos del sistema operativo (true) o no (false).
process-to-sniff-file: El nombre de un archivo JSON que contiene la información de los procesos específicos a monitorear.
sniff-from-file: Un indicador booleano que especifica si se deben cargar los procesos a monitorear desde un archivo (true) o no (false).
process-to-sniff-regex: Un patrón de expresión regular que se utiliza para seleccionar procesos específicos a monitorear.

# metrics
Esta es una lista de métricas que el script capturará y supervisará:

cpu: Métrica que monitorea el uso de la CPU. Permite opciones para normalizar y mostrar valores absolutos.
memory: Métrica que monitorea el uso de memoria en megabytes (MB).
paginated-memory: Métrica que monitorea el uso de memoria paginada en megabytes (MB).
net-output: Métrica que monitorea la salida de red en megabytes (MB).
net-input: Métrica que monitorea la entrada de red en megabytes (MB).


pyinstaller --onefile src/main.py
