from mcp.server import MCPServer

from tools.system import (
    get_status,
    get_memory as system_get_memory,
    get_disk as system_get_disk,
)


server = MCPServer(
    name="Hermes Sysadmin",
    version="0.1.0",
    instructions=(
        "Read-only server monitoring tools for the Hermes sysadmin agent."
    ),
)


@server.tool(
    name="get_server_status",
    description=(
        "Get the current server status including CPU, RAM, disk usage, "
        "and system uptime."
    ),
)
def get_server_status():
    return get_status()


@server.tool(
    name="get_memory",
    description=(
        "Get current RAM and swap memory usage of the server."
    ),
)
def get_memory():
    return system_get_memory()


@server.tool(
    name="get_disk",
    description=(
        "Get current disk usage including total, used, free space, "
        "and usage percentage."
    ),
)
def get_disk():
    return system_get_disk()


if __name__ == "__main__":
    server.run_stdio_async()