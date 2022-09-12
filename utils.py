def tryint(value):
    try:
        return int(value)
    except Exception:
        return value


async def query_edit(
    self, text: str, reply_markup=None, answer_kwargs=None, *args, **kwargs
):
    if answer_kwargs is None:
        answer_kwargs = {}
    edit = await self.edit_message_text(
        text=text, reply_markup=reply_markup, *args, **kwargs
    )

    await self.answer(**answer_kwargs)
    return edit


def message_remove_keyboard(self, message_id=None, *args, **kwargs):
    return self._client.edit_message_reply_markup(
        self.chat.id, message_id or self.message_id, {}, *args, **kwargs
    )


def message_reply(self, text: str, reply_markup=None, *args, **kwargs):
    return self.reply_text(
        text, *args, reply_markup=reply_markup, *args, **kwargs
    )
