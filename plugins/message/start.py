import constructors
from pyrogram import Client, Filters

@Client.on_message(Filters.command('start'))
async def onstart(client, message, lang):
    text, keyboard = constructors.start(message, lang)
    
    await message.reply(text, reply_markup=keyboard)