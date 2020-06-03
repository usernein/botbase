import asyncio
import base64
import glob
import json
import re
import os
import yaml

from dotenv import load_dotenv
from langs import Langs

from pyromod import listen, filters
from pyrogram import Client
from utils import tryint

# Load variables on .env to os.environ
load_dotenv()

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

# I don't use os.getenv('KEY', fallback) because the fallback wil only be used if the key doesn't exist. I want to use the fallback also when the key exists but it's invalid
client = Client(os.getenv('PYROGRAM_SESSION') or 'client', plugins={"root":"plugins"}, **pyrogram_config)
client.set_parse_mode('html')

def open_yml(filename):
    with open(filename) as fp:
        data = yaml.safe_load(fp)
    return data

strings = {}
for string_file in glob.glob('strings/*.yml'):
    language_code = re.match('strings/(.+)\.yml$', string_file)[1]
    strings[language_code] = open_yml(string_file)

langs = Langs(**strings, escape_html=True)

logs_chat = tryint(os.getenv('LOGS_CHAT'))
sudoers = list(map(tryint, os.getenv('SUDOERS_LIST').split(' ')))