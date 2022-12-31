import asyncio
import logging
import os

from config import logs_chat, client
from database import connect_database
from tortoise import run_async
from waiters import waiters
from pyrogram import idle
from pyrogram.errors import RPCError
from rich import print

async def alert_startup():
    plugins = [
        (
            handler.user_callback
            if hasattr(handler, "user_callback")
            else handler.callback
        )
        for group in client.dispatcher.groups.values()
        for handler in group
    ]

    plugins_count = len(plugins)

    started_alert = f"""
🚀 Bot launched. <code>{plugins_count}</code> plugins loaded.
- <b>app_version</b>: <code>{client.app_version}</code>
- <b>device_model</b>: <code>{client.device_model}</code>
- <b>system_version</b>: <code>{client.system_version}</code>
"""
    await client.send_message(logs_chat, started_alert)


class TelegramHandler(logging.Handler):
    def emit(self, record):
        text = self.format(record)
        asyncio.ensure_future(client.send_message(logs_chat, text))


if os.getenv("DEBUG"):
    logger = logging.getLogger("pyrogram.client.ext.dispatcher")
    logger.addHandler(TelegramHandler(logging.DEBUG))


async def main():
    await client.start()
    waiters.bind_client(client)
    await connect_database()
    try:
        await alert_startup()
    except RPCError:
        print("[yellow]An RPCError occurred while trying to alert_startup()[/]")
    print("[green]Running...[/]")
    await idle()


run_async(main())
