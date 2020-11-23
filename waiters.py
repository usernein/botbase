import pyrogram

from database import User

class Waiters():
    handlers = []
    cancel_filter = pyrogram.filters.command('cancel')
    
    def bind_client(self, client: pyrogram.Client):
        self.client = client
        self.client.add_handler(pyrogram.handlers.MessageHandler(self.message_handler), -1)
    
    async def message_handler(self, client: pyrogram.Client, message: pyrogram.types.Message):
        lang = message.lang
        user = await User.get(id=message.from_user.id)
        
        for waiter_obj in self.handlers:
            if user.waiting_for != waiter_obj['waiting_for'] or not (await waiter_obj['filters'](client, message) if callable(waiter_obj['filters']) else True):
                continue
        
            if await self.cancel_filter(client, message) and user.waiting_cancelable:
                await message.reply(lang.command_canceled(command=user.waiting_for))
                await user.wait_end()
                message.stop_propagation()
            
            await waiter_obj["callback"](client, message, user)
            message.stop_propagation()

    def add_handler(self, waiting_for: str, filters=None):
        def decorator(func):
            self.handlers.append({
                "waiting_for": waiting_for,
                "callback": func,
                "filters": filters
            })
            return func
        return decorator

waiters = Waiters()
