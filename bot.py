import asyncio
import os
import logging
import threading
import http.server
import socketserver
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

# --- LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION ---
# Use an Environment Variable on Render for security! 
# If not set, it defaults to the string provided below.
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8466225003:AAFQJVaMwSX9kzYUOc0gZxMtUDdW3Ifnf8E")

# --- RENDER PORT BINDING FIX ---
def run_dummy_server():
    """Satisfies Render's requirement for a web service to listen on a port."""
    PORT = int(os.environ.get("PORT", 10000))
    Handler = http.server.SimpleHTTPRequestHandler
    # Use allow_reuse_address to prevent port errors on restarts
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            logging.info(f"✅ Health check server serving at port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        logging.error(f"❌ Dummy server failed: {e}")

# Start dummy server in background immediately
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- BOT FUNCTIONS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 *Downloader Active*\nSend a link to start.", parse_mode='Markdown')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        return
    
    status_msg = await update.message.reply_text("🔎 *Analyzing link...*", parse_mode='Markdown')

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'quiet': True,
        # 'cookiefile': 'cookies.txt', # Uncomment if you upload a cookies.txt file
    }

    try:
        loop = asyncio.get_event_loop()
        def run_ydl():
            if not os.path.exists('downloads'):
                os.makedirs('downloads')
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        file_path = await loop.run_in_executor(None, run_ydl)
        await status_msg.edit_text("📤 *Uploading...*")
        
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ *Done!*")
        
        os.remove(file_path)
        await status_msg.delete()
    except Exception as e:
        logging.error(f"Download Error: {e}")
        await status_msg.edit_text(f"❌ *Error:* {str(e)}")

# --- MAIN BLOCK ---
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ Error: No BOT_TOKEN found!")
    else:
        # Build the application once
        application = ApplicationBuilder().token(BOT_TOKEN).build()

        # Add Handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

        print("🤖 Bot is starting...")
        
        # This will automatically clear webhooks and start polling
        application.run_polling(drop_pending_updates=True)
        
