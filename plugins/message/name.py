from database import User
from pyrogram import Client, Filters
from waiters import waiters

@Client.on_message(Filters.command('name'))
async def onname(client, message):
    user = await User.get(id=message.from_user.id)
    await user.wait_for('name')
    await message.reply('This is an example of waiter. Send me your name.')

# Sample of waiter usage
@waiters.add_handler('name')
async def on_name(client, message, user):
    if not message.text:
        return await message.reply('Please send your name in a text message.')
    await message.reply(f'Ok, your name is {message.text}. I am not waiting for it anymore.')
    await user.wait_end()