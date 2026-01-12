import asyncio
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
    """Run a simple web server to satisfy Render's port check."""
    PORT = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            print(f"✅ Health check server serving at port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Dummy server failed: {e}")

threading.Thread(target=run_dummy_server, daemon=True).start()
# -------------------------------

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Replace with your NEW token from BotFather
BOT_TOKEN = '8466225003:AAFQJVaMwSX9kzYUOc0gZxMtUDdW3Ifnf8E'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message."""
    await update.message.reply_text(
        "🚀 *High-Speed Video Downloader Bot Active*\n\n"
        "Send me a link from any supported website to start the download.",
        parse_mode='Markdown'
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the link, downloads, and sends the video."""
    url = update.message.text
    if not url.startswith("http"):
        return

    status_msg = await update.message.reply_text("🔎 *Analyzing link...*", parse_mode='Markdown')

    # Updated yt-dlp options with headers to bypass detection
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
        },
    }

    try:
        loop = asyncio.get_event_loop()
        
        def run_ydl():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        file_path = await loop.run_in_executor(None, run_ydl)

        await status_msg.edit_text("📤 *Uploading video to Telegram...*", parse_mode='Markdown')
        
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ *Download Complete!*")
        
        if os.path.exists(file_path):
            os.remove(file_path)
        await status_msg.delete()

    except Exception as e:
        logging.error(f"Download Error: {e}")
        await status_msg.edit_text(f"❌ *Error:* Failed to process link. The site might be blocking the request or is unsupported.")

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("🤖 Bot is starting...")
    app.run_polling()
