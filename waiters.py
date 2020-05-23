import pyrogram

from database import User

class Waiters():
    handlers = {}
    
    def bind_client(self, client: pyrogram.Client):
        self.client = client
        self.client.add_handler(pyrogram.MessageHandler(self.message_handler), -1)
    
    async def message_handler(self, client: pyrogram.Client, message: pyrogram.Message):
        lang = message.lang
        user = await User.get(id=message.from_user.id)
        if user.waiting_for in self.handlers:
            if message.text == '/cancel':
                await message.reply(lang.command_canceled(waiting_for=user.waiting_for))
                await user.wait_end()
                message.stop_propagation()
            elif message.text == '/start':
                await user.wait_end()
                
            await self.handlers[user.waiting_for]['callback'](client, message, user)
            message.stop_propagation()

    def add_handler(self, waiting_for: str, filters=None):
        def decorator(func):
            self.handlers[waiting_for] = {"callback": func, filters: filters}
            return func
        return decorator

waiters = Waiters()