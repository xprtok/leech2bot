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
    # Render provides a port via the PORT environment variable; default to 8080
    PORT = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    
    # TCPServer allows Render's health check to find an open port
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            print(f"✅ Health check server serving at port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Dummy server failed: {e}")

# Start the dummy server in a separate background thread
# This happens BEFORE the bot starts polling to ensure the port is open fast
threading.Thread(target=run_dummy_server, daemon=True).start()
# -------------------------------

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# Insert your Bot Token from BotFather here
BOT_TOKEN = '8466225003:AAFQJVaMwSX9kzYUOc0gZxMtUDdW3Ifnf8E'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the command /start is issued."""
    await update.message.reply_text(
        "🚀 *High-Speed Video Downloader Bot Active*\n\n"
        "Send me a link from any supported website to start the download.",
        parse_mode='Markdown'
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes the link, downloads the video, and sends it to the user."""
    url = update.message.text
    
    # Check if the text looks like a link
    if not url.startswith("http"):
        return

    status_msg = await update.message.reply_text("🔎 *Analyzing link...*", parse_mode='Markdown')

    # yt-dlp options for high speed and compatible format for Telegram
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # Use run_in_executor to prevent blocking the main event loop during download
        loop = asyncio.get_event_loop()
        
        def run_ydl():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        file_path = await loop.run_in_executor(None, run_ydl)

        await status_msg.edit_text("📤 *Uploading video to Telegram...*", parse_mode='Markdown')
        
        # Send the downloaded video file back to the user
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ *Download Complete!*")
        
        # Clean up: Delete the local file to save server space
        if os.path.exists(file_path):
            os.remove(file_path)
        await status_msg.delete()

    except Exception as e:
        logging.error(f"Download Error: {e}")
        await status_msg.edit_text(f"❌ *Error:* Failed to process link. Ensure the site is supported.")

if __name__ == '__main__':
    # Ensure a local download directory exists for temporary storage
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # Build the Application using the v20+ async style
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add Command and Message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("🤖 Bot is starting...")
    
    # Run the bot using polling method
    app.run_polling()
