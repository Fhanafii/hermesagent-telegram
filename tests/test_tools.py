from tools.registry import (
    get_tool,
    get_schema,
    get_policy,
    execute_tool,
)


def test_registered_tools():
    expected_tools = [
        "get_server_status",
        "get_memory",
        "get_disk",
        "get_docker_containers",
        "get_container_logs",
        "get_error_log",
        "start_container",
        "stop_container",
        "restart_container",
    ]

    for tool_name in expected_tools:
        assert get_tool(tool_name) is not None


def test_tool_schemas():
    expected_tools = [
        "get_server_status",
        "get_memory",
        "get_disk",
        "get_docker_containers",
        "get_container_logs",
        "get_error_log",
        "start_container",
        "stop_container",
        "restart_container",
    ]

    for tool_name in expected_tools:
        assert get_schema(tool_name) is not None


def test_mutating_tools_require_confirmation():
    for tool_name in [
        "start_container",
        "stop_container",
        "restart_container",
    ]:
        policy = get_policy(tool_name)

        assert policy is not None
        assert policy["requires_confirmation"] is True


def test_unknown_tool():
    assert get_tool("delete_server") is None
    assert get_schema("delete_server") is None
    assert get_policy("delete_server") is None


def test_unknown_container_is_rejected():
    result = execute_tool(
        "get_container_logs",
        {
            "container": "unknown-container",
            "lines": 10,
        },
    )

    assert result["success"] is False
