import asyncio
import html
import io
import traceback

from config import sudoers
from contextlib import redirect_stdout
from database import User
from pyrogram import Client, Filters

@Client.on_message(Filters.regex("^/exec\s(?P<code>.+)") & Filters.user(sudoers))
async def execs(client, message):
    lang = message.lang
    strio = io.StringIO()
    code = message.matches[0]['code']
    
    # Shortcuts that will be available for the user code
    reply = message.reply_to_message
    user_id = (reply or message).from_user.id
    user = await User.objects.get(id=user_id)
    
    code_function = "async def __ex(client, message):"
    for line in code.split('\n'):
        code_function += f"\n    {line}"
    exec(code_function)
    
    with redirect_stdout(strio):
        try:
            await locals()["__ex"](client, message)
        except:
            traceback_string = traceback.format_exc()
            return await message.reply(f'<b>{html.escape(traceback_string)}</b>')
    
    output = lang.executed_cmd
    if strio.getvalue():
        output = f"<code>{html.escape(strio.getvalue())}</code>"
        
    await message.reply(output)