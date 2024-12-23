from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Chào mừng đến với bot Telegram!')

# Hàm xử lý lệnh /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
    Đây là các lệnh bạn có thể sử dụng:
    /start - Khởi động bot và nhận thông báo chào mừng.
    /help - Xem hướng dẫn sử dụng bot.
    """
    await update.message.reply_text(help_text)

# Hàm xử lý tin nhắn chứa từ khóa
async def handle_keyword_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.lower()

    # Kiểm tra từ khóa trong tin nhắn
    if 'ngu' in message_text:
        # Gửi ảnh từ file
        file_path = '/mnt/c/Users/hagia_h0hah0i/Pictures/ngu.jpg'  # Thay đổi đường dẫn khi triển khai
        try:
            with open(file_path, 'rb') as photo:
                await update.message.reply_photo(photo=photo)
        except FileNotFoundError:
            await update.message.reply_text("Không thể tìm thấy ảnh!")

    elif 'bình tĩnh' in message_text:
        file_path = '/mnt/c/Users/hagia_h0hah0i/Videos/Captures/binh tinh.mp4'  # Thay đổi đường dẫn khi triển khai
        try:
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video)
        except FileNotFoundError:
            await update.message.reply_text("Không thể tìm thấy video!")

    elif "hello" in message_text:
        await update.message.reply_text("Chào bạn! Tôi là bot, có thể giúp gì cho bạn?")
    elif "help" in message_text:
        await update.message.reply_text("Để sử dụng bot, bạn có thể dùng các lệnh: /start, /help...")
    else:
        await update.message.reply_text(f"Bạn đã gửi: {update.message.text}")

# Hàm xử lý lệnh \cmd add
async def cmd_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args  # `args` chứa các tham số sau lệnh \cmd add
    if args:
        item = " ".join(args)  # Ghép tất cả các từ lại thành một chuỗi
        await update.message.reply_text(f"Đã thêm: {item}")
    else:
        await update.message.reply_text("Vui lòng cung cấp thông tin để thêm sau \\cmd add.")

def main():
    print("Bot is starting...")

    # Thay "YOUR_TOKEN" bằng token bạn nhận từ BotFather
    application = Application.builder().token("7592678969:AAGyWclB-oOK5gYfWwFIZMLtpnhbKsgkv0E").build()

    # Thêm CommandHandler cho lệnh /start
    application.add_handler(CommandHandler("start", start))

    # Thêm CommandHandler cho lệnh /help
    application.add_handler(CommandHandler("help", help_command))

    # Thêm CommandHandler cho lệnh \cmd add
    application.add_handler(CommandHandler("cmd", cmd_add))

    # Thêm MessageHandler cho các tin nhắn
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_keyword_message))

    # Bắt đầu bot
    application.run_polling()
    application.idle()

if __name__ == '__main__':
    main()

