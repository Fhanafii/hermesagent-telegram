import os
from agent.executor import ToolExecutor
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from security.auth import is_authorized
from security.confirmation import ConfirmationManager

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


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

tool_executor = ToolExecutor()
confirmation_manager = ConfirmationManager()

# ============================================================
# SECURITY
# ============================================================

async def unauthorized(update: Update):
    if update.message:
        await update.message.reply_text(
            "⛔ Kamu tidak memiliki akses ke Hermes."
        )


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
            f"❌ Gagal membaca status server:\n"
            f"`{result.get('error', 'Unknown error')}`",
            parse_mode="Markdown",
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
            f"❌ Gagal membaca memory:\n"
            f"`{result.get('error', 'Unknown error')}`",
            parse_mode="Markdown",
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
            f"❌ Gagal membaca disk:\n"
            f"`{result.get('error', 'Unknown error')}`",
            parse_mode="Markdown",
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


async def restart(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user

    if not user or not is_authorized(user.id):
        await unauthorized(update)
        return

    if not context.args:
        await update.message.reply_text(
            "Gunakan:\n"
            "`/restart <container>`",
            parse_mode="Markdown",
        )
        return

    container = context.args[0]

    result = tool_executor.execute(
        "restart_container",
        {
            "container": container,
        },
    )

    if result["status"] == "confirmation_required":
        await request_confirmation(
            update,
            result["tool"],
            result["arguments"],
            result.get("risk"),
        )
        return

    if result["status"] == "blocked":
        await update.message.reply_text(
            f"⛔ {result['reason']}"
        )
        return

    if result["status"] == "success":
        await update.message.reply_text(
            "✅ Container berhasil direstart."
        )
        return

    await update.message.reply_text(
        f"❌ Gagal restart container:\n"
        f"`{result}`",
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
# Request Confirmation
# ============================================================
async def request_confirmation(
    update: Update,
    tool_name: str,
    arguments: dict,
    risk: str | None = None,
):
    user = update.effective_user

    if not user:
        return

    token = confirmation_manager.create(
        user_id=user.id,
        tool_name=tool_name,
        arguments=arguments,
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Confirm",
                callback_data=f"confirm:{token}",
            ),
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data=f"cancel:{token}",
            ),
        ]
    ]

    container = arguments.get(
        "container",
        "-",
    )

    await update.message.reply_text(
        "⚠️ *Confirmation Required*\n\n"
        f"Tool: `{tool_name}`\n"
        f"Container: `{container}`\n"
        f"Risk: `{(risk or 'unknown').upper()}`\n\n"
        "Apakah kamu yakin ingin menjalankan "
        "operasi ini?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def confirmation_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    user = query.from_user

    if not is_authorized(user.id):
        await query.edit_message_text(
            "⛔ Kamu tidak memiliki akses."
        )
        return

    data = query.data or ""

    if ":" not in data:
        await query.edit_message_text(
            "❌ Confirmation tidak valid."
        )
        return

    action, token = data.split(":", 1)

    request = confirmation_manager.get(token)

    if request is None:
        await query.edit_message_text(
            "⌛ Confirmation sudah kadaluarsa."
        )
        return

    # Pastikan token memang milik user yang menekan tombol.
    if request["user_id"] != user.id:
        await query.edit_message_text(
            "⛔ Confirmation ini bukan milik kamu."
        )
        return

    if action == "cancel":
        confirmation_manager.cancel(token)

        await query.edit_message_text(
            "❌ Operasi dibatalkan."
        )
        return

    if action != "confirm":
        await query.edit_message_text(
            "❌ Action tidak valid."
        )
        return

    request = confirmation_manager.consume(token)

    if request is None:
        await query.edit_message_text(
            "⌛ Confirmation sudah kadaluarsa."
        )
        return

    result = tool_executor.execute(
        request["tool"],
        request["arguments"],
        confirmed=True,
    )

    if result["success"]:
        await query.edit_message_text(
            "✅ Operasi berhasil dijalankan."
        )
    else:
        error = (
            result.get("result", {}).get(
                "error",
                "Unknown error",
            )
        )

        await query.edit_message_text(
            f"❌ Operasi gagal.\n\n"
            f"`{error[:3000]}`",
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

    application.add_handler(
        CallbackQueryHandler(
            confirmation_callback,
            pattern=r"^(confirm|cancel):",
        )
    )

    application.add_handler(
        CommandHandler("restart", restart)
    )

    print("Hermes Telegram Bot started.")

    application.run_polling()


if __name__ == "__main__":
    main()
