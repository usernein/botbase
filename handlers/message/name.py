from database import User
from pyrogram import Client, Filters
from waiters import waiters

@Client.on_message(Filters.command('name'))
async def onname(client, message):
    user = await User.get(id=message.from_user.id)
    await user.wait_for('name')
    await message.reply('This is an example of waiter. Send me your name.')

# Sample of waiter usage
@waiters.add_handler('name', ~Filters.text)
async def on_name_reject(client, message, user):
    await message.reply('Hey, i only read text.')

@waiters.add_handler('name')
async def on_name(client, message, user):
    await message.reply(f'Ok, your name is {message.text}. I am not waiting for it anymore.')
    await user.wait_end()