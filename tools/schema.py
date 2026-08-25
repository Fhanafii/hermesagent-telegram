TOOL_SCHEMAS = {
    "get_server_status": {
        "description": (
            "Mendapatkan status server saat ini, "
            "termasuk CPU, RAM, disk, dan uptime."
        ),
        "parameters": {},
    },

    "get_memory": {
        "description": (
            "Mendapatkan penggunaan RAM dan swap "
            "server saat ini."
        ),
        "parameters": {},
    },

    "get_disk": {
        "description": (
            "Mendapatkan penggunaan disk pada filesystem root."
        ),
        "parameters": {},
    },

    "get_docker_containers": {
        "description": (
            "Mendapatkan daftar Docker container "
            "beserta status dan image-nya."
        ),
        "parameters": {},
    },

    "get_container_logs": {
        "description": (
            "Mengambil log terbaru dari Docker container "
            "yang diizinkan."
        ),
        "parameters": {
            "container": {
                "type": "string",
                "description": "Nama Docker container.",
            },
            "lines": {
                "type": "integer",
                "description": (
                    "Jumlah baris log yang ingin diambil. "
                    "Default 30, maksimum 100."
                ),
            },
        },
        "required": [
            "container",
        ],
    },

    "start_container": {
        "description": (
            "Menjalankan Docker container yang diizinkan."
        ),
        "parameters": {
            "container": {
                "type": "string",
                "description": "Nama Docker container.",
            },
        },
        "required": [
            "container",
        ],
    },

    "stop_container": {
        "description": (
            "Menghentikan Docker container yang diizinkan."
        ),
        "parameters": {
            "container": {
                "type": "string",
                "description": "Nama Docker container.",
            },
        },
        "required": [
            "container",
        ],
    },

    "restart_container": {
        "description": (
            "Merestart Docker container yang diizinkan."
        ),
        "parameters": {
            "container": {
                "type": "string",
                "description": "Nama Docker container.",
            },
        },
        "required": [
            "container",
        ],
    },
}