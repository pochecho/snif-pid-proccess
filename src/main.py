import argparse
import time
import os
import signal
import sys
import json
from   constants import DEFAULT_CONFIG
from helpers import merge_configurations
from features.sniffer.index import SnifferHandler

if __name__ == "__main__":
    with open('config.json', 'r') as t:
        custom_config = json.load(t) 
    config = merge_configurations(DEFAULT_CONFIG,custom_config)
    
    parser = argparse.ArgumentParser(
        description="""
            Permite monitorear, reducir logs y graficar los mismos.
            Usa el archivo de configuración para establecer el modo de trabajo.
        """
    )

    parser.add_argument(
        '--mode',
        '-m', 
        nargs='?',
        type=str, 
        help='Modo de operación. Por defecto es "sniff". Valores posibles: "sniff" | "reducer" | "graph" ', 
        default='sniff'
    )


    args = parser.parse_args()
    
    mode_handlers = {
        'sniff': SnifferHandler
    }
    
    handler_class = mode_handlers[args.mode]
    handler = handler_class()
    
    def signal_handler(sig, frame):
        i  = 0
        handler.exit()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    
    handler.index(config)
    
    