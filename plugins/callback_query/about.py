import constructors
from pyrogram import Client, Filters

@Client.on_callback_query(Filters.callback_data('about'))
async def onabout(client, query, lang):
    text, keyboard = constructors.about(query, lang)
    
    await query.edit(text, reply_markup=keyboard)
    await query.answer()