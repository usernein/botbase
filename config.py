import asyncio
import json
import os
import yaml

from base64 import b64decode, b64encode
from langs import Langs

from pyromod import listen, filters
from pyrogram import Client
from utils import tryint

if os.path.exists('env.json'):
    with open('env.json', 'r') as fp:
        config_json = json.load(fp)
    os.environ.update(**config_json)

for required_env in ['LOGS_CHAT', 'SUDOERS_LIST', 'DATABASE_URL']:
    if required_env not in os.environ:
        raise AttributeError(f'Missing required env variable: {required_env}')
    if not os.getenv(required_env):
        raise ValueError(f'Invalid value for required env variable {required_env}')

# Extra **kwargs for creating pyrogram.Client
# TODO: Beautify this, please
config = json.loads(
    b64decode(
        # e30= is {} encoded
        os.getenv('PYROGRAM_CONFIG', 'e30=').encode() or b'{}'
    ).decode()
)
app = Client(os.getenv('PYROGRAM_SESSION') or 'bot', plugins={"root":"plugins"}, **config)
app.set_parse_mode('html')

with open('./strings/en.yml') as enfp:
    langs = Langs(
        escape_html=True,
        en=yaml.safe_load(enfp),
    )
    
logs_chat = tryint(os.getenv('LOGS_CHAT'))
sudoers = list(map(tryint, os.getenv('SUDOERS_LIST').split(' ')))
