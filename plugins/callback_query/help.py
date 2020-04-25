import constructors
from pyrogram import Client, Filters

@Client.on_callback_query(Filters.callback_data('help'))
async def onhelp(client, query, lang):
    text, keyboard = constructors.help(query, lang)
    
    await query.edit(text, reply_markup=keyboard)
    await query.answer()
    