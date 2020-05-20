import pyrogram

# Shortcuts
## CallbackQuery.edit
pyrogram.client.types.bots_and_keyboards.callback_query.CallbackQuery.edit = pyrogram.client.types.bots_and_keyboards.callback_query.CallbackQuery.edit_message_text

def tryint(value):
    try:
        return int(value)
    except:
        return value
        
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
