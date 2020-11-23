from pyrogram import Client, filters
from pyromod.helpers import ikb

@Client.on_message(filters.command('help'))
async def onhelp(client, message):
    lang = message.lang
    await message.reply(lang.help_text)