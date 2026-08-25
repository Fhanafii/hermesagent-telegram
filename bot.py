import os

from security.auth import is_authorized
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from tools.system import (
    get_status,
    get_memory,
    get_disk,
    format_bytes,
    format_uptime,
)

from tools.docker import (
    get_containers,
    get_container_logs,
)


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ============================================================
# SECURITY
# ============================================================

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

    result = get_status()

    if not result["success"]:
        await update.message.reply_text(
            "❌ Gagal membaca status server."
        )
        return

    memory = result["memory"]
    disk = result["disk"]

    await update.message.reply_text(
        "🖥️ *Server Status*\n\n"
        f"CPU: `{result['cpu_percent']:.1f}%`\n"
        f"RAM: `{format_bytes(memory['used'])} / "
        f"{format_bytes(memory['total'])}` "
        f"({memory['percent']:.1f}%)\n"
        f"Disk: `{format_bytes(disk['used'])} / "
        f"{format_bytes(disk['total'])}` "
        f"({disk['percent']:.1f}%)\n"
        f"Uptime: `{format_uptime(result['uptime_seconds'])}`",
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

    result = get_memory()

    if not result["success"]:
        await update.message.reply_text(
            "❌ Gagal membaca memory."
        )
        return

    ram = result["ram"]
    swap = result["swap"]

    await update.message.reply_text(
        "🧠 *Memory*\n\n"
        f"RAM Total: `{format_bytes(ram['total'])}`\n"
        f"RAM Used: `{format_bytes(ram['used'])}`\n"
        f"RAM Available: `{format_bytes(ram['available'])}`\n"
        f"RAM Usage: `{ram['percent']:.1f}%`\n\n"
        f"Swap Total: `{format_bytes(swap['total'])}`\n"
        f"Swap Used: `{format_bytes(swap['used'])}`\n"
        f"Swap Usage: `{swap['percent']:.1f}%`",
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

    result = get_disk()

    if not result["success"]:
        await update.message.reply_text(
            "❌ Gagal membaca disk."
        )
        return

    await update.message.reply_text(
        "💾 *Disk Usage*\n\n"
        f"Total: `{format_bytes(result['total'])}`\n"
        f"Used: `{format_bytes(result['used'])}`\n"
        f"Free: `{format_bytes(result['free'])}`\n"
        f"Usage: `{result['percent']:.1f}%`",
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

    result = get_containers()

    if not result["success"]:
        await update.message.reply_text(
            f"❌ Docker error:\n"
            f"`{result['stderr'][:3000]}`",
            parse_mode="Markdown",
        )
        return

    containers = result["containers"]

    if not containers:
        await update.message.reply_text(
            "🐳 Tidak ada container."
        )
        return

    lines = ["🐳 *Docker Containers*\n"]

    for container in containers:
        lines.append(
            f"• *{container['name']}*\n"
            f"  Status: `{container['status']}`\n"
            f"  Image: `{container['image']}`"
        )

    await update.message.reply_text(
        "\n\n".join(lines),
        parse_mode="Markdown",
    )


# ============================================================
# /logs
# ============================================================

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
            "`/logs pitjarus-backend-dev`",
            parse_mode="Markdown",
        )
        return

    container = context.args[0]

    result = get_container_logs(
        container=container,
        lines=30,
    )

    if not result["success"]:
        await update.message.reply_text(
            f"❌ {result['error']}"
        )
        return

    logs_text = result["logs"] or "(Tidak ada log)"

    await update.message.reply_text(
        f"📋 *Logs: {container}*\n\n"
        f"```text\n{logs_text[-3500:]}\n```",
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
