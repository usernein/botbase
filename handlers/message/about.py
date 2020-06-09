from pyrogram import Client, Filters
from pyromod.helpers import ikb

@Client.on_message(Filters.command('about'))
async def onabout(client, message):
    lang = message.lang
    text = lang.about_text
    
    await message.reply(text)