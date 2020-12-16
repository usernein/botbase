import asyncio
import html
import io
import re
import traceback

from config import sudoers
from contextlib import redirect_stdout
from database import User
from pyrogram import Client, filters

@Client.on_message(filters.regex("^/exec\s+(?P<code>.+)", re.S) & filters.user(sudoers))
async def execs(client, message):
    lang = message._lang
    strio = io.StringIO()
    code = message.matches[0]['code']
    
    # Shortcuts that will be available for the user code
    reply = message.reply_to_message
    user_id = (reply or message).from_user.id
    user = await User.get(id=user_id)
    
    code_function = "async def __ex(client, message, reply, user_id, user):"
    for line in code.split('\n'):
        code_function += f"\n    {line}"
    exec(code_function)
    
    with redirect_stdout(strio):
        try:
            await locals()["__ex"](client, message, reply, user_id, user)
        except:
            traceback_string = traceback.format_exc()
            return await message.reply(f'<b>{html.escape(traceback_string)}</b>')
    
    text = lang.executed_cmd
    output = strio.getvalue()
    if output:
        output = html.escape(output) # escape html special chars
        text = ''
        for line in output.splitlines():
            text += f"<code>{line}</code>\n"
        
    await message.reply(text)
