import asyncio
import html
import re
import traceback

from config import langs, sudoers
from database import Users
from pyrogram import Client, Filters
from termcolor import cprint
from meval import meval

@Client.on_message(Filters.command("eval") & Filters.user(sudoers))
async def evals(client, message):
    code = re.split(r"[\n ]+", message.text, 1)[1]
    try:
        res = await meval(code, locals())
    except:
        ev = traceback.format_exc()
        await message.reply(ev)
        return
    else:
        try:
            await message.reply(f"<code>{html.escape(str(res))}</code>")
        except Exception as e:
            await message.reply(e)