from pyrogram import Client, Filters
from pyromod.helpers import ikb

@Client.on_callback_query(Filters.callback_data('start'))
async def onstart(client, query):
    lang = query.lang
    
    text = lang.start_text(
        from_user=query.from_user
    )
    keyboard = ikb([
        [(lang.help, 'help'), (lang.about, 'about')]
    ])
    
    await query.edit(text, reply_markup=keyboard)
    await query.answer()