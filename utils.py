import inspect
import pyrogram
from pyromod.utils import patch, patchable
import config

# Shortcuts
## CallbackQuery.edit
pyrogram.client.types.bots_and_keyboards.callback_query.CallbackQuery.edit = pyrogram.client.types.bots_and_keyboards.callback_query.CallbackQuery.edit_message_text

# Monkeypatching
## Pass a langs.Langs object as positional argument to all handlers that have from_user in its update
@patch(pyrogram.client.handlers.handler.Handler)
class Handler():
    @patchable
    def __init__(self, callback: callable, filters=None):
        async def inject_lang(client, update, *args):
            language_code = None
            if getattr(update, 'from_user'):
                language_code = update.from_user.language_code
            
            lang = config.langs.getLanguage(language_code)
            update.lang = lang
            
            spec = inspect.getfullargspec(callback)
            if len([x for x in spec.args if x != 'self']) > 2 or spec.varargs:
                args += (lang,)
            
            return await callback(client, update, *args)
        self.callback = inject_lang
        self.filters = filters

# prefix components:
space =  '  '
branch = '│ '
# pointers:
tee =    '├─'
last =   '└─'


def parse_tree(paths=[], parsed={}):
    for path in paths:
        levels = path.split('.')
        length = len(levels)
        
        last_level = parsed
        for key,level in enumerate(levels):
            negative_pos = key-length
            if negative_pos == -2:
                level = f'📄 {level}.py'
            elif negative_pos == -1:
                level = f'{level}'
            else:
                level = f'📂 {level}/'
                
                
            if type(last_level) != dict:
                last_level = {}
            last_level = last_level.setdefault(level, {})
        
    return parsed
            
            
def tree(contents, prefix: str='', result=[]):
    # contents each get pointers that are ├── with a final └── :
    pointers = dict(zip(contents.keys(),  [tee] * (len(contents) - 1) + [last]))

    for name,content in contents.items():
        pointer = pointers.get(name, space)
        result.append(prefix + pointer + name)
        if len(content) != 0: # extend the prefix and recurse:
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            tree(content, prefix=prefix+extension, result=result)+"\n"
    return '\n'.join(result)
