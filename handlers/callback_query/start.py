from pyrogram import Client, filters
from pyromod.helpers import ikb

@Client.on_callback_query(filters.regex('^start'))
async def onstart(client, query):
    lang = query._lang
    from_user = query.from_user
    
    text = lang.start_text(
        from_user=from_user
    )
    keyboard = ikb([
        [(lang.help, 'help'), (lang.about, 'about')]
    ])
    
    await query.edit_message_text(text, reply_markup=keyboard)
    await query.answer()