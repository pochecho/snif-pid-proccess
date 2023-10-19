DEFAULT_CONFIG = {
    "name": "tic-partner",
    "features": {
        "sniffer": {
            "logs-folder": "logs",
            "sniff-myself": True,
            "sniff-host": True,
            "process-to-sniff-file" : "my-process.json",
            "sniff-from-file": False,
            "process-to-sniff-regex": "^terminal64$",
            "metrics" : [
                {
                    "name" :"cpu",
                    "normalize": False,
                    "status" : "enabled"
                },
                {
                    "name" :"memory",
                    "unit": "MB",
                    "status" : "enabled"
                },
                {
                    "name" :"paginated-memory",
                    "unit": "MB",
                    "status" : "enabled"
                },
                {
                    "name" :"net-output",
                    "unit": "MB",
                    "status" : "enabled"
                },
                {
                    "name" :"net-input",
                    "unit": "MB",
                    "status" : "enabled"
                }
            ]

        }
    }
}