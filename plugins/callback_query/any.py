from config import langs
from database import User
from pyrogram import Client

# Getting the language to use
@Client.on_callback_query(group=-2)
async def deflang(client, query):
    query.lang = langs.get_language(query.from_user.language_code)
    # Add the user if it's not added yet
    #await User.get_or_create({'language': query.lang.code}, id=query.from_user.id)