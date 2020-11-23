from database import User
from pyrogram import Client, filters
from pyromod.helpers import ikb

def gen_options(lang):
    options = []
    for LANGUAGE_CODE,obj in lang.strings.items():
        button = [
            (obj['NAME'], f'set_lang {LANGUAGE_CODE}'),
            (f"✅ {obj['NAME']}", 'noop')
        ][obj['NAME'] == lang.NAME]
        
        options.append(button)
    lines = [
        options
    ]
    return ikb(lines)

@Client.on_message(filters.command('language'))
async def onlangs(client, message):
    lang = message.lang
    keyboard = gen_options(lang)
    await message.reply(lang.choose_language, reply_markup=keyboard)

@Client.on_callback_query(filters.regex('^set_lang (?P<code>.+)'))
async def onsetlang(client, query):
    lang = query.lang
    match = query.matches[0]
    lang = lang.get_language(match['code'])
    await User.get(id=query.from_user.id).update(language=lang.code)
    keyboard = gen_options(lang)
    await query.edit_message_text(lang.choose_language, reply_markup=keyboard)
    await query.answer(lang.language_chose)