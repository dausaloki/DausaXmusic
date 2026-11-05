"""Persistent private favorites and playlists.

These commands store user-submitted titles/URLs. Playback still uses the normal
/play command so all existing permissions, provider checks and queue rules apply.
"""
from __future__ import annotations

import re
from pyrogram import filters
from pyrogram.types import Message

from DAUSAXMUSIC import app
from DAUSAXMUSIC.core.mongo import mongodb
from config import BANNED_USERS

favorites_db = mongodb.user_favorites
playlists_db = mongodb.user_playlists
MAX_FAVORITES = 100
MAX_PLAYLISTS = 30
MAX_TRACKS_PER_PLAYLIST = 50


def _clean_name(value: str) -> str:
    value = re.sub(r"\s+", " ", (value or "").strip())
    return value[:48]


def _format_items(items: list[str], limit: int = 30) -> str:
    if not items:
        return "<i>Nothing saved yet.</i>"
    rows = [f"<b>{i}.</b> {item[:180]}" for i, item in enumerate(items[:limit], 1)]
    if len(items) > limit:
        rows.append(f"<i>…and {len(items) - limit} more.</i>")
    return "\n".join(rows)


@app.on_message(filters.command("favorite") & filters.private & ~BANNED_USERS)
async def save_favorite(_, message: Message):
    if not message.from_user:
        return
    query = message.text.split(None, 1)[1].strip() if len(message.command) > 1 else ""
    if not query:
        return await message.reply_text("Usage: <code>/favorite song name or URL</code>")
    user_id = message.from_user.id
    current = await favorites_db.find_one({"user_id": user_id}) or {"items": []}
    items = current.get("items", [])
    if query in items:
        return await message.reply_text("💗 This track is already in your favorites.")
    if len(items) >= MAX_FAVORITES:
        return await message.reply_text(f"Your favorites are full ({MAX_FAVORITES}). Remove one first with /unfavorite.")
    await favorites_db.update_one(
        {"user_id": user_id},
        {"$addToSet": {"items": query}, "$setOnInsert": {"user_id": user_id}},
        upsert=True,
    )
    await message.reply_text("💗 Saved to your private favorites. Use /favorites to view it.")


@app.on_message(filters.command("favorites") & filters.private & ~BANNED_USERS)
async def show_favorites(_, message: Message):
    if not message.from_user:
        return
    doc = await favorites_db.find_one({"user_id": message.from_user.id}) or {}
    items = doc.get("items", [])
    await message.reply_text(
        "<b>💗 Your Favorites</b>\n\n" + _format_items(items) +
        "\n\n<i>Play any entry with /play followed by its title or URL.</i>"
    )


@app.on_message(filters.command("unfavorite") & filters.private & ~BANNED_USERS)
async def remove_favorite(_, message: Message):
    if not message.from_user:
        return
    if len(message.command) < 2 or not message.command[1].isdigit():
        return await message.reply_text("Usage: <code>/unfavorite number</code> (see /favorites)")
    user_id = message.from_user.id
    doc = await favorites_db.find_one({"user_id": user_id}) or {}
    items = doc.get("items", [])
    index = int(message.command[1]) - 1
    if index < 0 or index >= len(items):
        return await message.reply_text("That favorite number does not exist.")
    removed = items.pop(index)
    await favorites_db.update_one({"user_id": user_id}, {"$set": {"items": items}})
    await message.reply_text(f"Removed: <code>{removed[:180]}</code>")


@app.on_message(filters.command("playlist") & filters.private & ~BANNED_USERS)
async def manage_playlists(_, message: Message):
    if not message.from_user:
        return
    user_id = message.from_user.id
    raw = message.text.split(None, 1)[1].strip() if len(message.command) > 1 else ""
    if not raw:
        return await message.reply_text(
            "<b>🎧 Playlist Manager</b>\n\n"
            "<code>/playlist create name</code>\n"
            "<code>/playlist list</code>\n"
            "<code>/playlist add name | song or URL</code>\n"
            "<code>/playlist show name</code>\n"
            "<code>/playlist remove name | number</code>\n"
            "<code>/playlist delete name</code>"
        )
    action, _, tail = raw.partition(" ")
    action = action.lower()
    tail = tail.strip()

    if action == "list":
        cursor = playlists_db.find({"user_id": user_id}, {"name": 1, "_id": 0}).sort("name", 1)
        docs = await cursor.to_list(length=MAX_PLAYLISTS)
        names = [d.get("name", "") for d in docs]
        return await message.reply_text("<b>🎧 Your Playlists</b>\n\n" + ("\n".join(f"• {n}" for n in names) if names else "<i>No playlists yet.</i>"))

    if action == "create":
        name = _clean_name(tail)
        if not name:
            return await message.reply_text("Usage: <code>/playlist create name</code>")
        count = await playlists_db.count_documents({"user_id": user_id})
        if count >= MAX_PLAYLISTS:
            return await message.reply_text(f"Playlist limit reached ({MAX_PLAYLISTS}).")
        await playlists_db.update_one(
            {"user_id": user_id, "name_key": name.casefold()},
            {"$setOnInsert": {"user_id": user_id, "name": name, "name_key": name.casefold(), "items": []}},
            upsert=True,
        )
        return await message.reply_text(f"✅ Playlist <b>{name}</b> is ready.")

    if action in {"add", "remove"}:
        if "|" not in tail:
            return await message.reply_text("Use <code>name | song</code> for add or <code>name | number</code> for remove.")
        name, value = [part.strip() for part in tail.split("|", 1)]
        name = _clean_name(name)
        doc = await playlists_db.find_one({"user_id": user_id, "name_key": name.casefold()})
        if not doc:
            return await message.reply_text("Playlist not found. Create it first with /playlist create.")
        if action == "add":
            if not value:
                return await message.reply_text("Please provide a song title or URL.")
            if len(doc.get("items", [])) >= MAX_TRACKS_PER_PLAYLIST:
                return await message.reply_text(f"This playlist is full ({MAX_TRACKS_PER_PLAYLIST} tracks).")
            await playlists_db.update_one({"_id": doc["_id"]}, {"$addToSet": {"items": value[:500]}})
            return await message.reply_text(f"➕ Added to <b>{doc['name']}</b>.")
        if not value.isdigit():
            return await message.reply_text("Provide the track number shown by /playlist show.")
        items = doc.get("items", [])
        index = int(value) - 1
        if index < 0 or index >= len(items):
            return await message.reply_text("That track number does not exist.")
        removed = items.pop(index)
        await playlists_db.update_one({"_id": doc["_id"]}, {"$set": {"items": items}})
        return await message.reply_text(f"Removed <code>{removed[:160]}</code> from <b>{doc['name']}</b>.")

    if action == "show":
        name = _clean_name(tail)
        doc = await playlists_db.find_one({"user_id": user_id, "name_key": name.casefold()})
        if not doc:
            return await message.reply_text("Playlist not found.")
        return await message.reply_text(f"<b>🎧 {doc['name']}</b>\n\n" + _format_items(doc.get("items", []), 50) + "\n\n<i>Use /play with a saved title or URL to start playback.</i>")

    if action == "delete":
        name = _clean_name(tail)
        if not name:
            return await message.reply_text("Usage: <code>/playlist delete name</code>")
        result = await playlists_db.delete_one({"user_id": user_id, "name_key": name.casefold()})
        return await message.reply_text("🗑 Playlist deleted." if result.deleted_count else "Playlist not found.")

    await message.reply_text("Unknown action. Send /playlist to see available commands.")
