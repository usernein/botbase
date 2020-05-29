import pyrogram

from database import User

class Waiters():
    handlers = []
    cancel_filter = pyrogram.Filters.command('cancel')
    
    def bind_client(self, client: pyrogram.Client):
        self.client = client
        self.client.add_handler(pyrogram.MessageHandler(self.message_handler), -1)
    
    async def message_handler(self, client: pyrogram.Client, message: pyrogram.Message):
        lang = message.lang
        user = await User.get(id=message.from_user.id)
        
        for waiter_obj in self.handlers:
            if user.waiting_for != waiter_obj['waiting_for'] or not (waiter_obj['filters'](message) if callable(waiter_obj['filters']) else True):
                continue
        
            if self.cancel_filter(message) and user.waiting_cancelable:
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