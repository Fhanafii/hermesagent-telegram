import os


def get_error_log(lines: int = 50) -> dict:
    # Prioritaskan absolute path ke project ESP32CAM di /home/fhanafi/ESP32CAM/server/error.log
    possible_paths = [
        "/home/fhanafi/ESP32CAM/server/error.log",
        os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "..",
                "ESP32CAM",
                "server",
                "error.log",
            )
        ),
        "ESP32CAM/server/error.log",
    ]

    log_path = None
    for path in possible_paths:
        if os.path.exists(path):
            log_path = path
            break

    if not log_path:
        # Jika belum ada sama sekali, gunakan path utama /home/fhanafi/ESP32CAM/server/error.log
        log_path = "/home/fhanafi/ESP32CAM/server/error.log"
        if not os.path.exists(log_path):
            return {
                "success": False,
                "error": f"Log file not found at {log_path}",
            }

    try:
        lines = max(1, min(lines, 500))
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            all_lines = f.readlines()
            tail_lines = all_lines[-lines:] if all_lines else []
            content = "".join(tail_lines)

        return {
            "success": True,
            "path": log_path,
            "lines": lines,
            "total_lines": len(all_lines),
            "logs": content,
        }
    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }
