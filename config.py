import asyncio
import base64
import glob
import json
import re
import os
import pyrogram
import yaml

from dotenv import load_dotenv
from langs import Langs

from pyromod import listen, filters
from pyrogram import Client
from utils import tryint, query_edit, message_remove_keyboard, message_reply

# Load variables on .env to os.environ
load_dotenv('.env')

def b64encode(value:str):
    return base64.b64encode(value.encode()).decode()
def b64decode(value:str):
    return base64.b64decode(value.encode()).decode()

required_env_vars = ['LOGS_CHAT', 'SUDOERS_LIST', 'DATABASE_URL']
for required in required_env_vars:
    if required not in os.environ:
        raise AttributeError(f'Missing required env variable: {required}')
    if not os.getenv(required):
        raise ValueError(f'Invalid value for required env variable {required}')

# Extra **kwargs for creating pyrogram.Client
pyrogram_config = os.getenv('PYROGRAM_CONFIG') or b64encode('{}')
pyrogram_config = b64decode(pyrogram_config)
pyrogram_config = json.loads(pyrogram_config)

# All monkeypatch must be done before the Client instance is created
pyrogram.types.CallbackQuery.edit = query_edit
pyrogram.types.Message.remove_keyboard = message_remove_keyboard
pyrogram.types.Message.reply = message_reply

# I don't use os.getenv('KEY', fallback) because the fallback wil only be used if the key doesn't exist. I want to use the fallback also when the key exists but it's invalid
client = Client(os.getenv('PYROGRAM_SESSION') or 'client', plugins={"root":"handlers"}, **pyrogram_config)
client.set_parse_mode('html')

def open_yml(filename):
    with open(filename) as fp:
        data = yaml.safe_load(fp)
    return data

strings = {}
for string_file in glob.glob('strings/**/*.yml', recursive=True):
    language_code = re.search('/(.+?)\.yml$', string_file)[1]
    strings_dict = open_yml(string_file)
    if len(language_code) > 30 or 'NAME' not in strings_dict:
        continue
    if language_code in strings:
        print('Loading duplicated', string_file)
    strings[language_code] = strings_dict

langs = Langs(**strings, escape_html=True)

logs_chat = tryint(os.getenv('LOGS_CHAT'))
sudoers = list(map(tryint, os.getenv('SUDOERS_LIST').split(' ')))
