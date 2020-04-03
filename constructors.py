from pyromod.helpers import ikb

def keyboard_back_to(back_data, lang):
    keyboard = ikb([
        [(lang.back, back_data)]
    ])
    return keyboard
    
def start(update, lang):
    text = lang.start_text(
        first_name=update.from_user.first_name
    )
    keyboard = ikb([
        [(lang.help, 'help'), (lang.about, 'about')]
    ])
    return text, keyboard
    
def help(update, lang):
    text = lang.help_text
    keyboard = keyboard_back_to('start', lang)
    return text, keyboard
    
def about(update, lang):
    text = lang.about_text
    keyboard = keyboard_back_to('start', lang)
    return text, keyboard