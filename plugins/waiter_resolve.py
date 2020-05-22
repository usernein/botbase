import waiters

from database import User
from pyrogram import Client

@Client.on_message(group=-1)
async def waiter_resolve(client, message):
    lang = message.lang
    user = await User.get(id=message.from_user.id)
    if user.waiting_for in waiters.funcs:
        if message.text == '/cancel':
            await message.reply(lang.command_canceled(waiting_for=user.waiting_for))
            await user.wait_end()
            message.stop_propagation()
        elif message.text == '/start':
            await user.wait_end()
            
        await waiters.funcs[user.waiting_for]['func'](client, message, user)
        message.stop_propagation()