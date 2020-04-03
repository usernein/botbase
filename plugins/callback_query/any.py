import asyncio

from config import langs
from database import User
from pyrogram import Client, Filters
from termcolor import cprint
from pyromod.helpers import ikb

# Getting the language to use
@Client.on_callback_query(group=-1)
async def deflang(client, query):
    query.lang = langs.getLanguage(query.from_user.language_code)
    # Adding the user if it's not added yet
    if not len(await User.objects.filter(id=query.from_user.id).all()):
        await User.objects.create(id=query.from_user.id, language=query.lang.language)
    