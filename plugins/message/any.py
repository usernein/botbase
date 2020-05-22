from config import langs
from database import User
from pyrogram import Client, Filters

# Getting the language to use
@Client.on_message(group=-2)
async def deflang(client, message):
    message.lang = langs.getLanguage(message.from_user.language_code)
    # Add the user if it's not added yet
    await User.get_or_create({'language': message.lang.language}, id=message.from_user.id)
    
# Define what updates to reject
@Client.on_message(~Filters.private | Filters.edited)
async def reject(client, message):
    message.stop_propagation()