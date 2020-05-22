import asyncio
import html
import traceback

from config import sudoers
from database import User
from pyrogram import Client, Filters
from meval import meval

@Client.on_message(Filters.regex("^/eval\s(?P<code>.+)") & Filters.user(sudoers))
async def evals(client, message):
    eval_code = message.matches[0]['code']
    
    # Shortcuts that will be available for the user code
    reply = message.reply_to_message
    user_id = (reply or message).from_user.id
    try:
        user = await User.get(id=user_id)
    except:
        user = None
    
    try:
        output = await meval(eval_code, globals(), **locals())
    except:
        traceback_string = traceback.format_exc()
        return await message.reply(f"Exception while running the code:\n{traceback_string}")
    else:
        try:
            await message.reply(f"<code>{html.escape(str(output))}</code>")
        except:
            traceback_string = traceback.format_exc()
            return await message.reply(f"Exception while sending output:\n{traceback_string}")