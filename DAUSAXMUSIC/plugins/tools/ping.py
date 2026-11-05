from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from config import *
from DAUSAXMUSIC import app
from DAUSAXMUSIC.core.call import JARVIS
from DAUSAXMUSIC.utils import bot_sys_stats
from DAUSAXMUSIC.utils.decorators.language import language
from DAUSAXMUSIC.utils.inline import supp_markup
from config import BANNED_USERS, PING_VID_URL
from DAUSAXMUSIC.utils.rich_buttons import rich_call


@app.on_message(filters.command("ping", prefixes=["/"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_video(
        video=PING_VID_URL,
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await JARVIS.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await rich_call(response.edit_text,
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
