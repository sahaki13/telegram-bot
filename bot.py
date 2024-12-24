import os
import logging
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import ChatMigrated
from youtubesearchpython import VideosSearch

# Lấy token từ biến môi trường
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Cấu hình logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ghi log vào file
file_handler = logging.FileHandler("bot.log")
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Ghi log vào console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("Chào mừng đến với bot Telegram!")
    except ChatMigrated as e:
        new_chat_id = e.migrate_to_chat_id
        logger.info(f"Chat migrated to new chat id: {new_chat_id}")

# Lệnh /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        help_text = """
        Đây là các lệnh bạn có thể sử dụng:
        /start - Khởi động bot và nhận thông báo chào mừng.
        /help - Xem hướng dẫn sử dụng bot.
        /music - Nhận một bài hát ngẫu nhiên từ YouTube.
        """
        await update.message.reply_text(help_text)
    except ChatMigrated as e:
        new_chat_id = e.migrate_to_chat_id
        logger.info(f"Chat migrated to new chat id: {new_chat_id}")

# Lệnh /music
async def music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        query = "music"  # Từ khóa tìm kiếm
        search = VideosSearch(query, limit=50)
        results = search.result()['result']

        if results:
            random_video = random.choice(results)
            song_url = f"https://www.youtube.com/watch?v={random_video['id']}"
            await update.message.reply_text(f"Here's a random song for you: {song_url}")
        else:
            await update.message.reply_text("Sorry, I couldn't find a song at the moment.")
    except Exception as e:
        logger.error(f"Error in /music: {e}")
        await update.message.reply_text("An error occurred while fetching a song.")

# Tin nhắn chứa từ khóa
async def handle_keyword_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.lower()

    if 'ngu' in message_text:
        file_path = '/mnt/c/Users/hagia_h0hah0i/Pictures/ngu.jpg'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
        else:
            await update.message.reply_text("Không thể tìm thấy ảnh!")

    elif 'bình tĩnh' in message_text:
        file_path = '/mnt/c/Users/hagia_h0hah0i/Videos/Captures/binh tinh.mp4'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video)
        else:
            await update.message.reply_text("Không thể tìm thấy video!")

    elif "hello" in message_text:
        await update.message.reply_text("Chào bạn! Tôi là bot, có thể giúp gì cho bạn?")

    else:
        await update.message.reply_text(f"Bạn đã gửi: {update.message.text}")

# Lệnh thêm item
async def cmd_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if args:
        item = " ".join(args)
        await update.message.reply_text(f"Đã thêm: {item}")
    else:
        await update.message.reply_text("Vui lòng cung cấp thông tin để thêm sau \\cmd add.")

# Xử lý lỗi
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    if isinstance(context.error, ChatMigrated):
        new_chat_id = context.error.migrate_to_chat_id
        logger.info(f"Chat migrated to new chat id: {new_chat_id}")
    else:
        logger.error(f"Unhandled error: {context.error}")

# Hàm chính
def main():
    logger.info("Bot is starting...")

    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN không được cấu hình. Vui lòng đặt biến môi trường.")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("music", music))
    application.add_handler(CommandHandler("cmd", cmd_add))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyword_message))
    application.add_error_handler(error_handler)

    # Chạy bot
    application.run_polling()

if __name__ == '__main__':
    main()

