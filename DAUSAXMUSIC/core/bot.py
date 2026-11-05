from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


class JARVIS(Client):
    def __init__(self):
        super().__init__(
            name="DausaXmusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            workers=48,
            max_concurrent_transmissions=7,
        )
        LOGGER(__name__).info("Bot client initialized.")

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username, self.id = me.username, me.id
        self.name = f"{me.first_name} {me.last_name or ''}".strip()
        self.mention = me.mention

        try:
            await self.send_message(
                config.LOGGER_ID,
                (
                    f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                    f"ɪᴅ : <code>{self.id}</code>\n"
                    f"ɴᴀᴍᴇ : {self.name}\n"
                    f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("❌ Bot cannot access the log group/channel – add & promote it first!")
            raise RuntimeError("Bot cannot access LOGGER_ID; add and promote it first.") from None
        except Exception as exc:
            LOGGER(__name__).error(f"❌ Bot has failed to access the log group.\nReason: {type(exc).__name__}")
            raise RuntimeError("Bot could not send the startup message to LOGGER_ID.") from None

        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
        except Exception as exc:
            LOGGER(__name__).error(
                "❌ Could not check log-group admin status (%s).",
                type(exc).__name__,
            )
            raise RuntimeError("Could not verify bot admin status in LOGGER_ID.") from None
        if member.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error("❌ Promote the bot as admin in the log group/channel.")
            raise RuntimeError("Bot must be an administrator in LOGGER_ID.")

        LOGGER(__name__).info(f"✅ Music Bot started as {self.name} (@{self.username})")
