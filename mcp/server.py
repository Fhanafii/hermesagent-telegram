from mcp.server.fastmcp import FastMCP

from tools.system import (
    get_status,
    get_memory as system_get_memory,
    get_disk as system_get_disk,
)


mcp = FastMCP("Hermes Sysadmin")


@mcp.tool()
def get_server_status():
    """Get the current CPU, RAM, disk usage, and server uptime."""
    return get_status()


@mcp.tool()
def get_memory():
    """Get current RAM and swap memory usage."""
    return system_get_memory()


@mcp.tool()
def get_disk():
    """Get current disk usage of the server."""
    return system_get_disk()


if __name__ == "__main__":
    mcp.run()