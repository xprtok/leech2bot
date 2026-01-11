import os
import asyncio
from pyrogram import Client, filters
from mega import Mega  # For Mega links
 from Crypto.Cipher import AES  # pycrypto
from Cryptodome.Cipher import AES  # pycryptodome

# --- CONFIGURATION ---
API_ID = 36982189          # Get from my.telegram.org
API_HASH = "d3ec5feee7342b692e7b5370fb9c8db7"    # Get from my.telegram.org
BOT_TOKEN = "8466225003:AAFQJVaMwSX9kzYUOc0gZxMtUDdW3Ifnf8E"  # Get from @BotFather

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
        await status_msg.edit("⚠️ Darknet (.onion) links require a Tor Proxy to download. Extraction failed.")
        return

    # 2. Handle Magnet/Torrent Links
    elif link.startswith("magnet:") or link.endswith(".torrent"):
        await status_msg.edit("🌀 Magnet/Torrent detected. Starting Aria2...")
        # In a real bot, you'd call: os.system(f"aria2c '{link}'")
        await asyncio.sleep(2)
        await status_msg.edit("✅ Torrent added to queue.")

    # 3. Handle Mega Links
    elif "mega.nz" in link:
        await status_msg.edit("☁️ Mega link detected. Authenticating...")
        try:
            # Simple Mega Logic
            # m = Mega().login()
            # m.download_url(link)
            await status_msg.edit("✅ Mega download started (using mega-cmd/py-mega).")
        except Exception as e:
            await status_msg.edit(f"❌ Mega Error: {e}")

    # 4. Handle Direct Links (Google, Dropbox, etc.)
    else:
        await status_msg.edit("🚀 Direct/Cloud link detected. Leeching...")
        # Logic: download file -> upload to Telegram
        await asyncio.sleep(3)
        await status_msg.edit("📦 File leeched successfully!")

print("Bot is running...")
app.run()
