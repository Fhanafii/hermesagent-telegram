def get_gemini_function_declarations():
    declarations = []

    for name, schema in TOOL_SCHEMAS.items():
        declarations.append(
            {
                "name": name,
                "description": schema["description"],
                "parameters": schema["parameters"],
            }
        )

    return declarations

TOOL_SCHEMAS = {
    "get_server_status": {
        "description": (
            "Mendapatkan status server saat ini, "
            "termasuk CPU, RAM, disk, dan uptime."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },

    "get_memory": {
        "description": (
            "Mendapatkan penggunaan RAM dan swap "
            "server saat ini."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },

    "get_disk": {
        "description": (
            "Mendapatkan penggunaan disk pada filesystem root."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },

    "get_docker_containers": {
        "description": (
            "Mendapatkan daftar Docker container "
            "beserta status dan image-nya."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },

    "get_container_logs": {
        "description": (
            "Mengambil log terbaru dari Docker container "
            "yang diizinkan."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "container": {
                    "type": "string",
                    "description": "Nama Docker container.",
                },
                "lines": {
                    "type": "integer",
                    "description": (
                        "Jumlah baris log yang ingin diambil."
                    ),
                },
            },
            "required": ["container"],
        },
    },

    "start_container": {
        "description": (
            "Menjalankan Docker container yang diizinkan."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "container": {
                    "type": "string",
                    "description": "Nama Docker container.",
                },
            },
            "required": ["container"],
        },
    },

    "stop_container": {
        "description": (
            "Menghentikan Docker container yang diizinkan."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "container": {
                    "type": "string",
                    "description": "Nama Docker container.",
                },
            },
            "required": ["container"],
        },
    },

    "restart_container": {
        "description": (
            "Merestart Docker container yang diizinkan."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "container": {
                    "type": "string",
                    "description": "Nama Docker container.",
                },
            },
            "required": ["container"],
        },
    },

    "get_error_log": {
        "description": (
            "Menampilkan isi file error.log dari project ESP32CAM/server/error.log "
            "mengambil baris terakhir (seperti tail)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "lines": {
                    "type": "integer",
                    "description": (
                        "Jumlah baris terakhir yang ingin ditampilkan (default 50)."
                    ),
                },
            },
        },
    },
}