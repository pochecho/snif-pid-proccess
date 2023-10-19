import psutil
from typing import Any, Dict


def generate_name_folder(process):
    return f"{process['pid']}-{process['name'].lower()}"

def merge_configurations(default_config: Dict, custom_config: Dict):
    response = {}
    default_entries = default_config.items()
    for d_entry in default_entries:
        response[d_entry[0]] =custom_config.get(d_entry[0], d_entry[1])
    return response