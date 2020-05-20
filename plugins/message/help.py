from pyrogram import Client, Filters
from pyromod.helpers import ikb

@Client.on_message(Filters.command('help'))
async def onhelp(client, message):
    lang = message.lang
    await message.reply(lang.help_text)