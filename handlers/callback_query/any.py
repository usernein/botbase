from config import langs
from database import User
from pyrogram import Client

# Getting the language to use
@Client.on_callback_query(group=-2)
async def deflang(client, query):
    from_user = query.from_user
    language = langs.normalize_code(from_user.language_code or "en")
    user = await User.get_or_none(id=from_user.id)
    query._lang = langs.get_language(user.language if user else language)