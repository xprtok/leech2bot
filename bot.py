import asyncio
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
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
    status_msg = await update.message.reply_text("🔎 *Analyzing link...*", parse_mode='Markdown')

    # yt-dlp options for high speed and best quality
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # Run yt-dlp in a separate thread to keep the bot async
        loop = asyncio.get_event_loop()
        
        def run_ydl():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)

        file_path = await loop.run_in_executor(None, run_ydl)

        await status_msg.edit_text("📤 *Uploading video to Telegram...*", parse_mode='Markdown')
        
        # Send the downloaded video file
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ *Download Complete!*")
        
        # Clean up: Delete the file after sending to save server space
        os.remove(file_path)
        await status_msg.delete()

    except Exception as e:
        logging.error(f"Download Error: {e}")
        await status_msg.edit_text(f"❌ *Error:* Failed to process link. Ensure the site is supported.")

if __name__ == '__main__':
    # Ensure a download directory exists
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # Build the application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot is running...")
    app.run_polling()
