from pyrogram import Client, Filters
from pyromod.helpers import ikb

@Client.on_callback_query(Filters.callback_data('about'))
async def onabout(client, query):
    lang = query.lang
    text = lang.about_text
    keyboard = ikb([
        [(lang.back, 'start')]
    ])
    
    await query.edit(text, reply_markup=keyboard)
    await query.answer()