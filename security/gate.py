from tools.registry import (
    get_tool,
    get_policy,
    execute_tool,
)


class SecurityGate:
    def check(
        self,
        tool_name: str,
        arguments: dict | None = None,
    ) -> dict:
        arguments = arguments or {}

        # -------------------------------------------------
        # 1. Pastikan tool terdaftar
        # -------------------------------------------------

        tool = get_tool(tool_name)

        if tool is None:
            return {
                "allowed": False,
                "requires_confirmation": False,
                "reason": f"Tool '{tool_name}' tidak ditemukan.",
            }

        # -------------------------------------------------
        # 2. Pastikan policy tersedia
        # -------------------------------------------------

        policy = get_policy(tool_name)

        if policy is None:
            # Fail closed
            return {
                "allowed": False,
                "requires_confirmation": False,
                "reason": (
                    f"Tool '{tool_name}' belum memiliki "
                    "security policy."
                ),
            }

        # -------------------------------------------------
        # 3. Cek apakah confirmation diperlukan
        # -------------------------------------------------

        if policy["requires_confirmation"]:
            return {
                "allowed": False,
                "requires_confirmation": True,
                "risk": policy["risk"].value,
                "tool": tool_name,
                "arguments": arguments,
                "reason": "Confirmation required.",
            }

        # -------------------------------------------------
        # 4. LOW risk → boleh dijalankan
        # -------------------------------------------------

        return {
            "allowed": True,
            "requires_confirmation": False,
            "risk": policy["risk"].value,
            "tool": tool_name,
            "arguments": arguments,
        }

    def execute(
        self,
        tool_name: str,
        arguments: dict | None = None,
    ) -> dict:
        check = self.check(
            tool_name,
            arguments,
        )

        if not check["allowed"]:
            return {
                "success": False,
                "blocked": True,
                **check,
            }

        result = execute_tool(
            tool_name,
            arguments,
        )

        return {
            "success": result.get("success", False),
            "blocked": False,
            "tool": tool_name,
            "result": result,
        }