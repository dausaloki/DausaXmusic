"""Owner health diagnostics and private user reports."""
from __future__ import annotations

import html
import time
from collections import defaultdict

import psutil
from pyrogram import filters
from pyrogram.types import Message

import config
from DAUSAXMUSIC import app
from DAUSAXMUSIC.core.mongo import mongodb
from DAUSAXMUSIC.misc import _boot_

_report_cooldowns: dict[int, float] = defaultdict(float)


def _uptime() -> str:
    seconds = max(0, int(time.time() - _boot_))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"


@app.on_message(filters.command("health") & filters.user(config.OWNER_ID))
async def owner_health(_, message: Message):
    try:
        await mongodb.command("ping")
        db_status = "Connected"
    except Exception as exc:
        db_status = f"Unavailable ({type(exc).__name__})"
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    await message.reply_text(
        "<b>🩺 DausaXmusic Runtime Health</b>\n\n"
        f"• Uptime: <code>{_uptime()}</code>\n"
        f"• CPU: <code>{psutil.cpu_percent(interval=0.2)}%</code>\n"
        f"• RAM: <code>{memory.percent}%</code>\n"
        f"• Disk: <code>{disk.percent}%</code>\n"
        f"• MongoDB: <code>{html.escape(db_status)}</code>\n"
        f"• Python PID: <code>{__import__('os').getpid()}</code>"
    )


@app.on_message(filters.command("report") & filters.private)
async def user_report(_, message: Message):
    if not message.from_user:
        return
    text = message.text.split(None, 1)[1].strip() if len(message.command) > 1 else ""
    if not text:
        return await message.reply_text("Usage: <code>/report describe the issue</code>")
    now = time.monotonic()
    if now - _report_cooldowns[message.from_user.id] < 60:
        return await message.reply_text("Please wait one minute before sending another report.")
    _report_cooldowns[message.from_user.id] = now
    sender = message.from_user
    username = f"@{sender.username}" if sender.username else "(no username)"
    report = (
        "<b>📨 New DausaXmusic Report</b>\n"
        f"User: {html.escape(sender.first_name)}\n"
        f"Username: {html.escape(username)}\n"
        f"User ID: <code>{sender.id}</code>\n\n"
        f"{html.escape(text[:3000])}"
    )
    try:
        await app.send_message(config.LOGGER_ID, report)
    except Exception:
        _report_cooldowns.pop(sender.id, None)
        return await message.reply_text("Report could not be delivered. Please contact the bot owner directly.")
    await message.reply_text("✅ Your report has been sent to the bot owner. Thank you.")
