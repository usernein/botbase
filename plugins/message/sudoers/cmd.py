import asyncio
import html

from config import sudoers
from pyrogram import Client, Filters

@Client.on_message(Filters.regex("^/cmd\s(?P<code>.+)") & Filters.user(sudoers))
async def cmd(client, message):
    lang = message.lang
    code = message.matches[0]['code']
    process = await asyncio.create_subprocess_shell(
        code,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT)
    result = await process.communicate()
    output = result[0].decode().rstrip() or lang.executed_cmd
    await message.reply(f'<code>{html.escape(output)}</code>')