from security.gate import SecurityGate


class ToolExecutor:

    def __init__(self):
        self.gate = SecurityGate()

    def execute(
        self,
        tool_name: str,
        arguments: dict | None = None,
    ) -> dict:

        arguments = arguments or {}

        check = self.gate.check(
            tool_name,
            arguments,
        )

        # -----------------------------------------------
        # Tool tidak diizinkan / tidak ditemukan
        # -----------------------------------------------

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
                "reason": check["reason"],
            }

        # -----------------------------------------------
        # LOW risk → execute
        # -----------------------------------------------

        result = self.gate.execute(
            tool_name,
            arguments,
        )

        if not result["success"]:
            return {
                "status": "error",
                "tool": tool_name,
                "result": result,
            }

        return {
            "status": "success",
            "tool": tool_name,
            "result": result["result"],
        }