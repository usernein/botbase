from pyrogram import Client, filters
from pyromod.helpers import ikb

@Client.on_message(filters.command('about'))
async def onabout(client, message):
    lang = message._lang
    text = lang.about_text
    
    await message.reply(text)