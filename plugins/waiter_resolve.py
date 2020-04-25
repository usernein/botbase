import orm
import waiters
 
from database import Users
from pyrogram import Client, Filters

@Client.on_message(group=-2)
async def waiter_resolve(client, message, lang):
    try:
        User = await Users.objects.get(id=message.from_user.id)
    except orm.exceptions.NoMatch:
        return
    
    if User and User.waiting_for and User.waiting_for in waiters.funcs:
        if message.text == '/cancel':
            await message.reply(lang.command_canceled)
            await User.wait_end()
            message.stop_propagation()
        elif message.text == '/start':
            await User.wait_end()
            
        await waiters.funcs[User.waiting_for]['func'](client, message, User)
        message.stop_propagation()
        