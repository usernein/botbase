from database import User
from pyrogram import Client, Filters

@Client.on_message(Filters.command('name'))
async def onname(client, message):
    user = await User.get(id=message.from_user.id)
    await user.wait_for('name')
    await message.reply('This is a example of waiter. Send me your name.')