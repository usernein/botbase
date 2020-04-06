import asyncio
import base64
import configparser
import json
import os
from sys import argv

from pyrogram import Client
from termcolor import cprint

def raise_ex(e):
    raise e

def b64encode(value:str):
    return base64.b64encode(value.encode()).decode()
def b64decode(value:str):
    return base64.b64decode(value.encode()).decode()
    
print('Creating config.ini...')
config = configparser.ConfigParser()
if os.path.exists('config.ini'):
    config.read('config.ini')
    print("Loaded existing config.ini. If you don't specify a value, the existing one will be used.")
config.setdefault('pyrogram', {})
config['pyrogram']['api_id'] = input('Input your api_id: ') or config['pyrogram'].get('api_id') or raise_ex(ValueError('Invalid api_id'))
config['pyrogram']['api_hash'] = input('Input your api_hash: ') or config['pyrogram'].get('api_hash') or raise_ex(ValueError('Invalid api_hash'))
config['pyrogram']['bot_token'] = input('Input the bot token: ') or config['pyrogram'].get('bot_token') or raise_ex(ValueError('Invalid bot token'))

with open('config.ini','w') as fp:
    config.write(fp)

async def init():
    print('Logging in and creating new .session file...')
    if os.path.exists('bot.session'):
        os.remove('bot.session')
    client = Client('bot', plugins={'enabled':False})
    await client.start()
    
    session_config = {k:v for section in config.sections() for k,v in config.items(section)}
    session_config = json.dumps(session_config)
    session_config = b64encode(session_config)
    
    session_string = client.export_session_string()
    
    me = await client.get_me()
    mention = f"@{me.username}" if me.username else me.first_name
    cprint(f"Logged in as {mention}", 'green')
    
    print("\nYour PYROGRAM_CONFIG (SENSITIVE DATA, DO NOT SHARE):")
    cprint(session_config, 'blue')
    
    print("\nYour PYROGRAM_SESSION (SENSITIVE DATA, DO NOT SHARE):")
    cprint(session_string+"\n", 'green')
    
    await client.stop()

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
print("Done.")