funcs = {}

def create_waiter(waiting_for, filters=None):
    def decorator(func):
        funcs[waiting_for] = {"func": func, filters: filters}
        return func
    return decorator

# Sample of waiter usage
@create_waiter('name')
async def on_name(client, message, user):
    if not message.text:
        return await message.reply('Please send your name in a text message.')
    await message.reply(f'Ok, your name is {message.text}. I am not waiting for it anymore.')
    await user.wait_end()