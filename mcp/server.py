from mcp.server import MCPServer
import asyncio

from agent.executor import ToolExecutor


server = MCPServer(
    name="Hermes Sysadmin",
    version="0.1.0",
    instructions=(
        "Sysadmin tools for the Hermes agent. "
        "Read-only tools can be executed directly. "
        "Mutating tools require security confirmation."
    ),
)

executor = ToolExecutor()

@server.tool(
    name="get_server_status",
    description=(
        "Get the current server status including CPU, RAM, "
        "disk usage, and system uptime."
    ),
)
def get_server_status():
    return executor.execute(
        "get_server_status",
        {},
    )


@server.tool(
    name="get_memory",
    description=(
        "Get current RAM and swap memory usage of the server."
    ),
)
def get_memory():
    return executor.execute(
        "get_memory",
        {},
    )


@server.tool(
    name="get_disk",
    description=(
        "Get current disk usage including total, used, "
        "free space, and usage percentage."
    ),
)
def get_disk():
    return executor.execute(
        "get_disk",
        {},
    )

if __name__ == "__main__":
    asyncio.run(server.run_stdio_async())