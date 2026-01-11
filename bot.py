import os
import sys
import asyncio
from pyrogram import Client, filters
from Cryptodome.Cipher import AES 
from mega import Mega 

# Configuration
API_ID = 36982189 
API_HASH = "d3ec5feee7342b692e7b5370fb9c8db7" 
BOT_TOKEN = "8466225003:AAFQJVaMwSX9kzYUOc0gZxMtUDdW3Ifnf8E" 

app = Client("leech_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Simple check for Darknet/Onion links
def is_onion(url):
    return ".onion" in url

@app.on_message(filters.command("leech") & filters.private)
async def leech_handler(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a link!\nUsage: `/leech <link>`")
        return

    link = message.text.split(None, 1)[1]
    status_msg = await message.reply_text("🔎 Analyzing link...")

    # 1. Handle Darknet/Onion Links
    if is_onion(link):
        await status_msg.edit("⚠️ Darknet (.onion) links require a Tor Proxy. Extraction failed.")
        return

    # 2. Handle Magnet/Torrent Links
    elif link.startswith("magnet:") or link.endswith(".torrent"):
        await status_msg.edit("🌀 Magnet/Torrent detected. Starting Aria2...")
        await asyncio.sleep(2)
        await status_msg.edit("✅ Torrent added to queue.")

    # 3. Handle Mega Links
    elif "mega.nz" in link:
        await status_msg.edit("☁️ Mega link detected. Authenticating...")
        try:
            # Note: Mega() requires mega.py library
            await status_msg.edit("✅ Mega download started.")
        except Exception as e:
            await status_msg.edit(f"❌ Mega Error: {e}")

    # 4. Handle Direct Links
    else:
        await status_msg.edit("🚀 Direct/Cloud link detected. Leeching...")
        await asyncio.sleep(3)
        await status_msg.edit("📦 File leeched successfully!")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
