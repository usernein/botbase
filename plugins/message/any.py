from config import langs
from database import User
from pyrogram import Client, Filters

# Getting the language to use
@Client.on_message(group=-2)
async def deflang(client, message):
    from_user = message.from_user
    language = langs.normalize_code(from_user.language_code or "en")
    user, is_new = await User.get_or_create({'language': language}, id=from_user.id)
    message.lang = langs.get_language(user.language)
    
# Define what updates to reject
@Client.on_message(~Filters.private | Filters.edited)
async def reject(client, message):
    message.stop_propagation()