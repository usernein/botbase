import asyncio

from config import langs
from database import User
from pyrogram import Client, Filters

# Getting the language to use
@Client.on_message(group=-2)
async def deflang(client, message):
    message.lang = langs.getLanguage(message.from_user.language_code)
    # Adding the user if it's not added yet
    if not len(await User.objects.filter(id=message.from_user.id).all()):
        await User.objects.create(id=message.from_user.id, language=message.lang.language)
    
# Define what updates to reject
## Reject messages that doesn't come from private chats. i.e. groups
@Client.on_message(~Filters.private)
async def ongroup(client, message):
    message.stop_propagation()

## Reject edited messages
@Client.on_message(Filters.edited)
async def onedited(client, message):
    message.stop_propagation()