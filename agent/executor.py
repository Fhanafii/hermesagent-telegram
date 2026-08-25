from security.gate import SecurityGate
from tools.registry import execute_tool


class ToolExecutor:

    def __init__(self):
        self.gate = SecurityGate()

    def execute(
        self,
        tool_name: str,
        arguments: dict | None = None,
        confirmed: bool = False,
    ) -> dict:

        arguments = arguments or {}

        check = self.gate.check(
            tool_name,
            arguments,
            confirmed=confirmed,
        )

        if not check["allowed"]:

            if check["requires_confirmation"]:
                return {
                    "status": "confirmation_required",
                    "tool": tool_name,
                    "arguments": arguments,
                    "risk": check.get("risk"),
                    "reason": check["reason"],
                }

            return {
                "status": "blocked",
                "tool": tool_name,
                "arguments": arguments,
                "reason": check["reason"],
            }

        result = execute_tool(
            tool_name,
            arguments,
        )

        if not result.get("success", False):
            return {
                "status": "error",
                "tool": tool_name,
                "result": result,
            }

        return {
            "status": "success",
            "tool": tool_name,
            "result": result,
        }