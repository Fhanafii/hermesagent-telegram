from tools.registry import (
    get_tool,
    get_policy,
)

class SecurityGate:

    def check(
        self,
        tool_name: str,
        arguments: dict | None = None,
    ) -> dict:

        arguments = arguments or {}

        # Tool harus terdaftar
        if get_tool(tool_name) is None:
            return {
                "allowed": False,
                "requires_confirmation": False,
                "reason": (
                    f"Tool '{tool_name}' tidak ditemukan."
                ),
            }

        # Policy harus tersedia
        policy = get_policy(tool_name)

        if policy is None:
            return {
                "allowed": False,
                "requires_confirmation": False,
                "reason": (
                    f"Tool '{tool_name}' belum memiliki "
                    "security policy."
                ),
            }

        # HIGH / confirmation
        if policy["requires_confirmation"]:
            return {
                "allowed": False,
                "requires_confirmation": True,
                "risk": policy["risk"].value,
                "tool": tool_name,
                "arguments": arguments,
                "reason": "Confirmation required.",
            }

        # LOW
        return {
            "allowed": True,
            "requires_confirmation": False,
            "risk": policy["risk"].value,
            "tool": tool_name,
            "arguments": arguments,
        }