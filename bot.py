import asyncio
import html
import inspect
import os
import sys
import utils

from functools import partial
from termcolor import cprint

import config
from config import logs_chat

loop = asyncio.get_event_loop()

async def run_client(client):
    try:
        await client.start()
    except AttributeError as e:
        if 'key' in str(e).lower():
            return cprint(str(e).split('. ')[0]+f". Run '{os.path.basename(sys.executable)} login.py' first.", 'red')
        raise e
        
    await asyncio.sleep(0.1)
    await alert_init(client)
    await client.idle()

async def alert_init(client):
    plugins = [(handler.user_callback if hasattr(handler, 'user_callback') else handler.callback) for group in client.dispatcher.groups.values() for handler in group]
    
    plugins_count = len(plugins)
    plugins_names = []
    for plugin_callback in plugins:
        members = {key:value for key,value in inspect.getmembers(plugin_callback)}
        full_name = f"{members['__globals__']['__name__']}.{members['__name__']}"
        plugins_names.append(full_name)
    plugins_text = utils.tree(utils.parse_tree(plugins_names))
    started_text = config.langs.start_log(plugins_count=plugins_count, plugins_names=plugins_names, plugins_text=plugins_text, client=client)
    
    await client.send_message(logs_chat, started_text)
        
loop.run_until_complete(run_client(config.app))
