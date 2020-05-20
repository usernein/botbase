import asyncio
import json
import os
import threading
import databases
import orm
import sqlalchemy

from functools import partial
from orm import Model, JSON, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker


database = databases.Database(os.getenv('DATABASE_URL'))
metadata = sqlalchemy.MetaData()

class User(Model):
    __tablename__ = 'user'
    __database__ = database
    __metadata__ = metadata
    
    key = Integer(primary_key=True)
    id = Integer()
    start_date = DateTime(default=func.now())
    waiting_for = String(max_length=50, allow_null=True)
    waiting_param = String(max_length=200, allow_null=True)
    language = String(max_length=10, default='en')
    timezone = String(max_length=100, default='UTC')
    
    async def wait_for(self, waiting_for, waiting_param=None):
        return await self.update(waiting_for=waiting_for, waiting_param=waiting_param)
        
    async def wait_end(self):
        return await self.update(waiting_for=None, waiting_param=None)
    

engine = sqlalchemy.create_engine(str(database.url))
metadata.create_all(engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()

async def create_db():
    return await database.connect()

# Need to run asyncio.run_coroutine_threadsafe with a loop in another thread. Otherwise this block will get stuck forever.
# I create a new loop to be able to use run_forever() and then stop() without affecting our main loop
loop = asyncio.get_event_loop()
threading.Thread(target=partial(asyncio.run_coroutine_threadsafe, create_db(), loop), daemon=True).start()
