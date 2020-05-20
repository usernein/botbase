import waiters

from database import User
from pyrogram import Client, Filters

@Client.on_message(group=-1)
async def waiter_resolve(client, message):
    lang = message.lang
    exists = await User.objects.get(id=message.from_user.id)
    if exists and exists.waiting_for in waiters.funcs:
        if message.text == '/cancel':
            await message.reply(lang.command_canceled)
            await exists.wait_end()
            message.stop_propagation()
        elif message.text == '/start':
            await exists.wait_end()
            
        await waiters.funcs[exists.waiting_for]['func'](client, message, exists)
        message.stop_propagation()
        