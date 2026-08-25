from enum import Enum


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


TOOL_POLICIES = {
    "get_server_status": {
        "risk": RiskLevel.LOW,
        "requires_confirmation": False,
    },

    "get_memory": {
        "risk": RiskLevel.LOW,
        "requires_confirmation": False,
    },

    "get_disk": {
        "risk": RiskLevel.LOW,
        "requires_confirmation": False,
    },

    "get_docker_containers": {
        "risk": RiskLevel.LOW,
        "requires_confirmation": False,
    },

    "get_container_logs": {
        "risk": RiskLevel.LOW,
        "requires_confirmation": False,
    },

    "get_error_log": {
        "risk": RiskLevel.LOW,
        "requires_confirmation": False,
    },

    "start_container": {
        "risk": RiskLevel.HIGH,
        "requires_confirmation": True,
    },

    "stop_container": {
        "risk": RiskLevel.HIGH,
        "requires_confirmation": True,
    },

    "restart_container": {
        "risk": RiskLevel.HIGH,
        "requires_confirmation": True,
    },
}

def get_tool_policy(tool_name: str) -> dict | None:
    return TOOL_POLICIES.get(tool_name)


def requires_confirmation(tool_name: str) -> bool:
    policy = get_tool_policy(tool_name)

    if not policy:
        return True

    return policy["requires_confirmation"]