noimport asyncio
import os
import logging
import threading
import http.server
import socketserver
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

# --- RENDER PORT BINDING FIX ---
def run_dummy_server():
    """Satisfies Render's requirement for a web service to listen on a port."""
    PORT = int(os.environ.get("PORT", 10000))
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            print(f"✅ Health check server serving at port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Dummy server failed: {e}")

# Start dummy server in background
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION ---
BOT_TOKEN = '8466225003:AAFQJVaMwSX9kzYUOc0gZxMtUDdW3Ifnf8E'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 *Downloader Active*\nSend a link to start.", parse_mode='Markdown')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"): return
    
    status_msg = await update.message.reply_text("🔎 *Analyzing link...*", parse_mode='Markdown')

    # UPDATED YDL_OPTS
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'quiet': True
    }

    try:
        loop = asyncio.get_event_loop()
        def run_ydl():
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

if __name__ == "__main__":
    application = ApplicationBuilder().token("YOUR_TOKEN").build()
    # Add your handlers here...
    # This automatically handles clearing old connections
    application.run_polling(drop_pending_updates=True)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("🤖 Bot is starting...")
    app.run_polling()
application = (
    ApplicationBuilder()
    .token("8466225003:AAFQJVaMwSX9kzYUOc0gZxMtUDdW3Ifnf8E")
    .post_init(my_setup) # Add the hook here
    .build()
)

application.run_polling()

async def my_setup(application: Application):
    # This runs after the bot is initialized but before polling starts
    await application.bot.delete_webhook()
    print("✅ Webhook deleted and bot initialized")
