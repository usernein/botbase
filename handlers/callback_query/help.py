from pyrogram import Client, Filters
from pyromod.helpers import ikb

@Client.on_callback_query(Filters.regex('^help'))
async def onhelp(client, query):
    lang = query.lang
    
    text = lang.help_text
    keyboard = ikb([
        [(lang.back, 'start')]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard)
    await query.answer()
    