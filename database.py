import asyncio
import os

from tortoise import fields
from tortoise import Tortoise
from tortoise.models import Model

class User(Model):
    key = fields.IntField(pk=True)
    id = fields.IntField()
    start_date = fields.DatetimeField(auto_now_add=True)
    waiting_for = fields.CharField(max_length=255, null=True)
    waiting_param = fields.CharField(max_length=255, null=True)
    waiting_cancelable = fields.CharField(max_length=255, null=True)
    language = fields.CharField(max_length=255, default='en')
    timezone = fields.CharField(max_length=255, default='UTC')
    
    async def wait_for(self, waiting_for, waiting_param=None, cancelable=True):
        return await self.get(key=self.key).update(waiting_for=waiting_for, waiting_param=waiting_param, waiting_cancelable=cancelable)
    
    async def wait_end(self):
        return await self.get(key=self.key).update(waiting_for=None, waiting_param=None, waiting_cancelable=None)
    
async def connect_database():
    await Tortoise.init({
        'connections': {
            'bot_db': os.getenv('DATABASE_URL')
        },
        'apps': {
            'bot': {'models': [__name__], 'default_connection': 'bot_db'}
        }
    })
    # Generate the schema
    await Tortoise.generate_schemas()