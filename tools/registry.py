from tools.system import (
    get_status,
    get_memory,
    get_disk,
)

from tools.docker import (
    get_containers,
    get_container_logs,
    stop_container,
    start_container,
    restart_container,
)

from tools.schema import TOOL_SCHEMAS

from security.policy import get_tool_policy


TOOLS = {
    "get_server_status": get_status,
    "get_memory": get_memory,
    "get_disk": get_disk,
    "get_docker_containers": get_containers,
    "get_container_logs": get_container_logs,

    "start_container": start_container,
    "stop_container": stop_container,
    "restart_container": restart_container,
}


def get_tool(name: str):
    return TOOLS.get(name)


def get_schema(name: str):
    return TOOL_SCHEMAS.get(name)


def get_policy(name: str):
    return get_tool_policy(name)


def execute_tool(
    name: str,
    arguments: dict | None = None,
):
    tool = get_tool(name)

    if tool is None:
        return {
            "success": False,
            "error": f"Tool '{name}' tidak ditemukan.",
        }

    arguments = arguments or {}

    try:
        return tool(**arguments)

    except TypeError as error:
        return {
            "success": False,
            "error": f"Invalid arguments: {error}",
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }