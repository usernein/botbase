from config import langs
from database import User
from pyrogram import Client, filters

# Getting the language to use
@Client.on_message(group=-2)
async def deflang(client, message):
    language = 'en'
    from_user = message.from_user
    if not from_user:
        message._lang = langs.get_language(language)
        return
    language = langs.normalize_code(from_user.language_code or "en")
    if message.chat.type == 'private':
        user, is_new = await User.get_or_create({'language': language}, id=from_user.id)
        language = user.language
    message._lang = langs.get_language(language)
    
# Define what updates to reject
@Client.on_message(~filters.private | filters.edited)
async def reject(client, message):
    message.stop_propagation()