import os
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token (get it from @BotFather)
TELEGRAM_BOT_TOKEN = '7641758752:AAE_DzNEUf8lZWxgEgJ3omvH45G7ARDQs5Q'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a download link to upload the video to Telegram.")

def download_video(url: str, filename: str) -> bool:
    """Downloads video from URL to a local file."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise error if request failed
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    except Exception as e:
        print("Failed to download video:", e)
        return False

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handles messages containing video download links."""
    url = update.message.text
    filename = 'downloaded_video.mp4'
    
    # Attempt to download the video
    if download_video(url, filename):
        # Send video to the chat where the link was received
        with open(filename, 'rb') as video_file:
            update.message.reply_video(video=video_file)
        update.message.reply_text("Video uploaded successfully!")
        # Clean up by removing the downloaded file
        os.remove(filename)
    else:
        update.message.reply_text("Failed to download video. Please check the link.")

def main() -> None:
    """Starts the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)
    
    # Command handler for /start
    updater.dispatcher.add_handler(CommandHandler("start", start))
    # Message handler for receiving download links
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
