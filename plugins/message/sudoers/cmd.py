import asyncio
import html
import re

from config import langs, sudoers
from database import Users
from pyrogram import Client, Filters
from termcolor import cprint
from pyromod.helpers import ikb

@Client.on_message(Filters.command("cmd") & Filters.user(sudoers))
async def cmd(client, message):
    lang = message.lang
    code = re.split(r"[\n ]+", message.text, 1)[1]
    proc = await asyncio.create_subprocess_shell(code,
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.STDOUT)
    ex = await proc.communicate()
    res = ex[0].decode().rstrip() or lang.executed_cmd
    await message.reply(f'<code>{html.escape(res)}</code>')