import subprocess


ALLOWED_CONTAINERS = {
    "monitoring-nginx",
    "monitoring-db",
    "pitjarus-backend-dev",
    "pitjarus-postgres-dev",
    "pitjarus-nginx-dev",
}


def run_command(
    command: list[str],
    timeout: int = 10,
) -> dict:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": "Command timeout.",
        }

    except Exception as error:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": str(error),
        }


def is_allowed_container(container: str) -> bool:
    return container in ALLOWED_CONTAINERS


def get_containers() -> dict:
    result = run_command(
        [
            "docker",
            "ps",
            "-a",
            "--format",
            "{{.Names}}|{{.Status}}|{{.Image}}",
        ]
    )

    if not result["success"]:
        return result

    containers = []

    if result["stdout"]:
        for line in result["stdout"].splitlines():
            parts = line.split("|", 2)

            if len(parts) != 3:
                continue

            name, status, image = parts

            containers.append(
                {
                    "name": name,
                    "status": status,
                    "image": image,
                }
            )

    return {
        "success": True,
        "containers": containers,
    }


def start_container(container: str) -> dict:
    if not is_allowed_container(container):
        return {
            "success": False,
            "error": f"Container '{container}' tidak diizinkan.",
        }

    result = run_command(
        [
            "docker",
            "start",
            container,
        ]
    )

    if not result["success"]:
        return {
            "success": False,
            "error": result["stderr"],
        }

    return {
        "success": True,
        "action": "start",
        "container": container,
        "message": f"Container '{container}' berhasil dijalankan.",
    }


def stop_container(container: str) -> dict:
    if not is_allowed_container(container):
        return {
            "success": False,
            "error": f"Container '{container}' tidak diizinkan.",
        }

    result = run_command(
        [
            "docker",
            "stop",
            container,
        ]
    )

    if not result["success"]:
        return {
            "success": False,
            "error": result["stderr"],
        }

    return {
        "success": True,
        "action": "stop",
        "container": container,
        "message": f"Container '{container}' berhasil dihentikan.",
    }


def restart_container(container: str) -> dict:
    if not is_allowed_container(container):
        return {
            "success": False,
            "error": f"Container '{container}' tidak diizinkan.",
        }

    result = run_command(
        [
            "docker",
            "restart",
            container,
        ]
    )

    if not result["success"]:
        return {
            "success": False,
            "error": result["stderr"],
        }

    return {
        "success": True,
        "action": "restart",
        "container": container,
        "message": f"Container '{container}' berhasil direstart.",
    }


def get_container_logs(
    container: str,
    lines: int = 30,
) -> dict:
    if not is_allowed_container(container):
        return {
            "success": False,
            "error": f"Container '{container}' tidak diizinkan.",
        }

    lines = max(1, min(lines, 100))

    result = run_command(
        [
            "docker",
            "logs",
            "--tail",
            str(lines),
            container,
        ],
        timeout=10,
    )

    if not result["success"]:
        return {
            "success": False,
            "error": result["stderr"],
        }

    return {
        "success": True,
        "container": container,
        "lines": lines,
        "logs": result["stdout"][-12000:],
    }