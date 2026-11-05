import asyncio
import importlib

from pyrogram import idle
from pyrogram.types import BotCommand

import config
from DAUSAXMUSIC import LOGGER, app, userbot
from DAUSAXMUSIC.core.call import JARVIS
from DAUSAXMUSIC.misc import sudo
from DAUSAXMUSIC.plugins import ALL_MODULES
from DAUSAXMUSIC.utils.database import get_banned_users, get_gbanned
from DAUSAXMUSIC.utils.lyrics import close_lyrics_http_client
from config import BANNED_USERS

BOT_COMMANDS = [
    BotCommand("start", "Start the bot"),
    BotCommand("help", "Open help menu"),
    BotCommand("play", "Play audio in voice chat"),
    BotCommand("vplay", "Play video in voice chat"),
    BotCommand("song", "Download a song"),
    BotCommand("spotify", "Download a Spotify track as audio"),
    BotCommand("apple", "Download an Apple Music track as audio"),
    BotCommand("lyrics", "Search and fetch song lyrics"),
    BotCommand("queue", "Show current queue"),
    BotCommand("player", "Open player controls"),
    BotCommand("autoplay", "Toggle similar-song autoplay"),
    BotCommand("autodelete", "Auto-delete player and queue notices"),
    BotCommand("vcnotify", "Toggle VC join notifications"),
    BotCommand("voiceplay", "Control spoken song requests"),
    BotCommand("gpt", "Ask the AI assistant"),
    BotCommand("claude", "Ask Claude-style AI"),
    BotCommand("geminivision", "Analyze a replied image"),
    BotCommand("editimg", "Edit a replied image with AI"),
    BotCommand("getdraw", "Generate an AI image"),
    BotCommand("genvid", "Generate a short AI video"),
    BotCommand("upscale", "Enhance a replied image"),
    BotCommand("rmbg", "Remove image background"),
    BotCommand("weather", "Get weather info"),
    BotCommand("insta", "Download Instagram media"),
    BotCommand("youtube", "Download a YouTube link"),
    BotCommand("facebook", "Download Facebook media"),
    BotCommand("x", "Download X/Twitter media"),
    BotCommand("snap", "Download Snapchat media"),
    BotCommand("tiktok", "Download TikTok media"),
    BotCommand("movie", "Search movie info"),
    BotCommand("news", "Get latest topic news"),
    BotCommand("encrypt", "PM-only encrypt replied content"),
    BotCommand("decrypt", "PM-only one-time decrypt"),
    BotCommand("settings", "Open group settings"),
    BotCommand("ping", "Check bot status"),
    BotCommand("health", "Owner-only runtime health check"),
    BotCommand("playlist", "Manage your saved playlists"),
    BotCommand("favorites", "Show your saved favorite tracks"),
    BotCommand("favorite", "Save a track to your favorites"),
    BotCommand("unfavorite", "Remove a saved favorite"),
    BotCommand("report", "Send a private issue report to the owner"),
]


async def init():
    missing = config.validate_required_config()
    if missing:
        raise RuntimeError("Missing required environment variables: " + ", ".join(missing))

    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error(
            "Assistant session not filled, please fill a Pyrogram session."
        )
        raise RuntimeError("At least one assistant STRING_SESSION is required.")

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    await app.start()
    await app.set_bot_commands(BOT_COMMANDS)
    await userbot.start()
    await JARVIS.start()

    await JARVIS.decorators()
    for all_module in ALL_MODULES:
        importlib.import_module("DAUSAXMUSIC.plugins" + all_module)

    LOGGER("DAUSAXMUSIC.plugins").info("Modules loaded.")
    LOGGER("DAUSAXMUSIC").info(
        "DausaXmusic started successfully."
    )
    await idle()
    try:
        weather_plugin = importlib.import_module("DAUSAXMUSIC.plugins.Kishu.weather")
        await weather_plugin.close_weather_http_client()
    except Exception:
        pass
    try:
        song_plugin = importlib.import_module("DAUSAXMUSIC.plugins.tools.song")
        await song_plugin.close_song_http_client()
    except Exception:
        pass
    await close_lyrics_http_client()
    await app.stop()
    await userbot.stop()
    LOGGER("DAUSAXMUSIC").info("Stopping music bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
