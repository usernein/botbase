import asyncio
import html
import io
import re
import traceback

from config import langs, sudoers
from contextlib import redirect_stdout
from database import User
from pyrogram import Client, Filters
from termcolor import cprint
from pyromod.helpers import ikb

@Client.on_message(Filters.command("exec") & Filters.user(sudoers))
async def execs(client, message):
    lang = message.lang
    strio = io.StringIO()
    code = re.split(r"[\n ]+", message.text, 1)[1]
    exec('async def __ex(client, message): ' + ' '.join('\n ' + l for l in code.split('\n')))
    with redirect_stdout(strio):
        try:
            await locals()["__ex"](client, message)
        except:
            return await message.reply(f'<b>{html.escape(traceback.format_exc())}</b>')
    
    out = lang.executed_cmd
    if strio.getvalue():
        out = f"<code>{html.escape(strio.getvalue())}</code>"
        
    await message.reply(out)