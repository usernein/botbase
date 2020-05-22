from pyrogram import Client, Filters
from pyromod.helpers import ikb

@Client.on_callback_query(Filters.regex('^about'))
async def onabout(client, query):
    lang = query.lang
    text = lang.about_text
    keyboard = ikb([
        [(lang.back, 'start')]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard)
    await query.answer()