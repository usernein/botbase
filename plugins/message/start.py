from pyrogram import Client, Filters
from pyromod.helpers import ikb

@Client.on_message(Filters.command('start'))
async def onstart(client, message):
    lang = message.lang
    
    text = lang.start_text(
        from_user=message.from_user
    )
    keyboard = ikb([
        [(lang.help, 'help'), (lang.about, 'about')]
    ])
    
    await message.reply(text, reply_markup=keyboard)