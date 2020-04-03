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
    
print('Creating config.ini...')
config = configparser.ConfigParser()
config['pyrogram'] = {}    
config['pyrogram']['api_id'] = (argv[1] if 1 < len(argv) else input('Input your api_id: ')) or raise_ex(ValueError('Invalid api_id'))
config['pyrogram']['api_hash'] = (argv[2] if 2 < len(argv) else input('Input your api_hash: ')) or raise_ex(ValueError('Invalid api_hash'))
config['pyrogram']['bot_token'] = (argv[3] if 3 < len(argv) else input('Input the bot token: ')) or raise_ex(ValueError('Invalid bot token'))

with open('config.ini','w') as fp:
    config.write(fp)

async def init():
    print('Logging in and creating .session file...')
    client = Client('bot', plugins={'enabled':False})
    await client.start()
    print("\nYour PYROGRAM_SESSION (SENSITIVE DATA, DO NOT SHARE):")
    cprint(client.export_session_string()+"\n", 'green')
    
    print("\nYour PYROGRAM_CONFIG (SENSITIVE DATA, DO NOT SHARE):")
    cprint(base64.b64encode(json.dumps({k:v for section in config.sections() for k,v in config.items(section)}, separators=(',', ':')).encode()).decode()+"\n", 'blue')
    
    await client.stop()

loop = asyncio.get_event_loop()
if not os.path.exists('bot.session'):
    loop.run_until_complete(init())
print("Done.")