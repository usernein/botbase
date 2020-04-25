import asyncio

from config import langs
from database import Users
from pyrogram import Client, Filters
from pyromod.helpers import ikb

# Add user to database
@Client.on_message(group=-1)
async def register_user(client, message, lang):
    # Add the user only if it's not added yet
    if not len(await Users.objects.filter(id=message.from_user.id).all()):
        await Users.objects.create(id=message.from_user.id, language=lang.language)
        
# Define what updates to reject
## Reject messages that doesn't come from private chats. i.e. groups
@Client.on_message(~Filters.private)
async def ongroup(client, message, lang):
    await message.chat.leave()
    message.stop_propagation()

## Reject edited messages
@Client.on_message(Filters.edited)
async def onedited(client, message, lang):
    message.stop_propagation()