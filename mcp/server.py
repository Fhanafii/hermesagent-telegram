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

# Docker
@server.tool(
    name="get_docker_containers",
    description=(
        "List Docker containers currently running on the server, "
        "including their names, status, and images."
    ),
)
def get_docker_containers():
    return executor.execute(
        "get_docker_containers",
        {},
    )


@server.tool(
    name="get_container_logs",
    description=(
        "Get recent logs from a Docker container. "
        "The container name must be provided."
    ),
)
def get_container_logs(container: str):
    return executor.execute(
        "get_container_logs",
        {
            "container": container,
        },
    )

#Docker Mutating Tools
@server.tool(
    name="start_container",
    description=(
        "Start a Docker container. "
        "This operation requires user confirmation."
    ),
)
def start_container(container: str):
    return executor.execute(
        "start_container",
        {
            "container": container,
        },
    )

@server.tool(
    name="stop_container",
    description=(
        "Stop a Docker container. "
        "This operation requires user confirmation."
    ),
)
def stop_container(container: str):
    return executor.execute(
        "stop_container",
        {
            "container": container,
        },
    )

@server.tool(
    name="restart_container",
    description=(
        "Restart a Docker container. "
        "This operation requires user confirmation."
    ),
)
def restart_container(container: str):
    return executor.execute(
        "restart_container",
        {
            "container": container,
        },
    )
if __name__ == "__main__":
    asyncio.run(server.run_stdio_async())