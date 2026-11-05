from pyrogram import filters
from pyrogram.types import Message

from DAUSAXMUSIC import app
from DAUSAXMUSIC.core.call import JARVIS
from DAUSAXMUSIC.utils.database import set_loop
from DAUSAXMUSIC.utils.decorators import AdminRightsCheck
from DAUSAXMUSIC.utils.inline import close_markup
from config import BANNED_USERS
from DAUSAXMUSIC.utils.rich_buttons import rich_call


@app.on_message(
    filters.command(["end"], prefixes=["/", "!"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    await JARVIS.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await rich_call(message.reply_text,
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
