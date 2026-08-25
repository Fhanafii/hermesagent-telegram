import os
import subprocess
import time

import psutil
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

ALLOWED_USER_IDS = {
    int(user_id.strip())
    for user_id in os.getenv("ALLOWED_USER_IDS", "").split(",")
    if user_id.strip()
}


# ============================================================
# SECURITY
# ============================================================

def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USER_IDS


async def unauthorized(update: Update):
    if update.message:
        await update.message.reply_text(
            "⛔ Kamu tidak memiliki akses ke Hermes."
        )


# ============================================================
# SERVER HELPERS
# ============================================================

def format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(value)

    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"

        size /= 1024

    return f"{size:.1f} PB"


def format_uptime(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    return f"{days}d {hours}h {minutes}m"


def run_command(command: list[str], timeout: int = 10):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

        return result.returncode, result.stdout.strip(), result.stderr.strip()

    except subprocess.TimeoutExpired:
        return -1, "", "Command timeout"

    except Exception as error:
        return -1, "", str(error)


# ============================================================
# /status
# ============================================================

async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user

    if not user or not is_authorized(user.id):
        await unauthorized(update)
        return

    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    uptime = int(time.time() - psutil.boot_time())

    await update.message.reply_text(
        "🖥️ *Server Status*\n\n"
        f"CPU: `{cpu:.1f}%`\n"
        f"RAM: `{format_bytes(memory.used)} / "
        f"{format_bytes(memory.total)}` "
        f"({memory.percent:.1f}%)\n"
        f"Disk: `{format_bytes(disk.used)} / "
        f"{format_bytes(disk.total)}` "
        f"({disk.percent:.1f}%)\n"
        f"Uptime: `{format_uptime(uptime)}`",
        parse_mode="Markdown",
    )


# ============================================================
# /memory
# ============================================================

async def memory(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user

    if not user or not is_authorized(user.id):
        await unauthorized(update)
        return

    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    await update.message.reply_text(
        "🧠 *Memory*\n\n"
        f"RAM Total: `{format_bytes(ram.total)}`\n"
        f"RAM Used: `{format_bytes(ram.used)}`\n"
        f"RAM Available: `{format_bytes(ram.available)}`\n"
        f"RAM Usage: `{ram.percent:.1f}%`\n\n"
        f"Swap Total: `{format_bytes(swap.total)}`\n"
        f"Swap Used: `{format_bytes(swap.used)}`\n"
        f"Swap Usage: `{swap.percent:.1f}%`",
        parse_mode="Markdown",
    )


# ============================================================
# /disk
# ============================================================

async def disk(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user

    if not user or not is_authorized(user.id):
        await unauthorized(update)
        return

    usage = psutil.disk_usage("/")

    await update.message.reply_text(
        "💾 *Disk Usage*\n\n"
        f"Total: `{format_bytes(usage.total)}`\n"
        f"Used: `{format_bytes(usage.used)}`\n"
        f"Free: `{format_bytes(usage.free)}`\n"
        f"Usage: `{usage.percent:.1f}%`",
        parse_mode="Markdown",
    )


# ============================================================
# /docker
# ============================================================

async def docker(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user

    if not user or not is_authorized(user.id):
        await unauthorized(update)
        return

    return_code, stdout, stderr = run_command(
        [
            "docker",
            "ps",
            "--format",
            "{{.Names}}|{{.Status}}|{{.Image}}",
        ]
    )

    if return_code != 0:
        await update.message.reply_text(
            f"❌ Docker error:\n`{stderr[:3000]}`",
            parse_mode="Markdown",
        )
        return

    if not stdout:
        await update.message.reply_text(
            "🐳 Tidak ada container yang sedang berjalan."
        )
        return

    lines = ["🐳 *Docker Containers*\n"]

    for line in stdout.splitlines():
        parts = line.split("|", 2)

        if len(parts) != 3:
            continue

        name, status, image = parts

        lines.append(
            f"• *{name}*\n"
            f"  Status: `{status}`\n"
            f"  Image: `{image}`"
        )

    await update.message.reply_text(
        "\n\n".join(lines),
        parse_mode="Markdown",
    )


# ============================================================
# /logs
# ============================================================

ALLOWED_CONTAINERS = {
    "monitoring-nginx",
    "monitoring-db",
    "pitjarus-backend-dev",
    "pitjarus-postgres-dev",
    "pitjarus-nginx-dev",
}


async def logs(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user

    if not user or not is_authorized(user.id):
        await unauthorized(update)
        return

    if not context.args:
        await update.message.reply_text(
            "Gunakan:\n\n"
            "`/logs <container>`\n\n"
            "Contoh:\n"
            "`/logs backend`",
            parse_mode="Markdown",
        )
        return

    container = context.args[0]

    if container not in ALLOWED_CONTAINERS:
        await update.message.reply_text(
            "⛔ Container tersebut tidak diizinkan."
        )
        return

    return_code, stdout, stderr = run_command(
        [
            "docker",
            "logs",
            "--tail",
            "30",
            container,
        ],
        timeout=10,
    )

    if return_code != 0:
        await update.message.reply_text(
            f"Gagal mengambil log:\n`{stderr[:3000]}`",
            parse_mode="Markdown",
        )
        return

    if not stdout:
        stdout = "(Tidak ada log)"

    # Telegram message memiliki batas ukuran.
    stdout = stdout[-3500:]

    await update.message.reply_text(
        f"📋 *Logs: {container}*\n\n"
        f"```text\n{stdout}\n```",
        parse_mode="Markdown",
    )


# ============================================================
# MAIN
# ============================================================

def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN belum diset."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", status)
    )

    application.add_handler(
        CommandHandler("status", status)
    )

    application.add_handler(
        CommandHandler("docker", docker)
    )

    application.add_handler(
        CommandHandler("disk", disk)
    )

    application.add_handler(
        CommandHandler("memory", memory)
    )

    application.add_handler(
        CommandHandler("logs", logs)
    )

    print("Hermes Telegram Bot started.")

    application.run_polling()


if __name__ == "__main__":
    main()
