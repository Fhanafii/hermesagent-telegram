import time

import psutil


def format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(value)

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


def format_uptime(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    return f"{days}d {hours}h {minutes}m"


def get_status():
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        uptime = int(time.time() - psutil.boot_time())

        return {
            "success": True,
            "cpu_percent": cpu,
            "memory": {
                "total": memory.total,
                "used": memory.used,
                "available": memory.available,
                "percent": memory.percent,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            },
            "uptime_seconds": uptime,
        }
    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }



def get_memory():
    try:
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            "success": True,
            "ram": {
                "total": ram.total,
                "used": ram.used,
                "available": ram.available,
                "percent": ram.percent,
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "percent": swap.percent,
            },
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


def get_disk():
    try:
        usage = psutil.disk_usage("/")

        return {
            "success": True,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }