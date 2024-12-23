from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os


# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Chào mừng đến với bot Telegram!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
    Đây là các lệnh bạn có thể sử dụng:
    /start - Khởi động bot và nhận thông báo chào mừng.
    /help - Xem hướng dẫn sử dụng bot.
    """
    await update.message.reply_text(help_text)

async def handle_keyword_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    message_text = update.message.text.lower()

    # Kiểm tra nếu tin nhắn chứa từ khóa 'abc'
    if 'ngu' in message_text:
        # Gửi hình ảnh hoặc GIF nếu tìm thấy từ khóa
        # Cách gửi ảnh từ file
        file_path = '/mnt/c/Users/hagia_h0hah0i/Pictures/ngu.jpg'  # Đường dẫn đến ảnh của bạn
        await update.message.reply_photo(photo=open(file_path, 'rb'))  # Gửi ảnh

        # Nếu bạn muốn gửi GIF, thay thế bằng:
        # await update.message.reply_animation(animation=open('path_to_gif/abc_animation.gif', 'rb'))
    elif 'bình tĩnh' in message_text:
        file_path = '/mnt/c/Users/hagia_h0hah0i/Videos/Captures/binh tinh.mp4'
        await update.message.reply_video(video=open(file_path, 'rb'))

    if "hello" in message:
        update.message.reply_text("Chào bạn! Tôi là bot, có thể giúp gì cho bạn?")
    elif "help" in message:
        update.message.reply_text("Để sử dụng bot, bạn có thể dùng các lệnh: /start, /help...")    
    else:
        # Nếu không có từ khóa 'abc', bạn có thể phản hồi mặc định
        await update.message.reply_text(f"Bạn đã gửi: {update.message.text}")

# Hàm xử lý lệnh \cmd add
async def cmd_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Lấy thông tin sau lệnh \cmd add
    args = context.args  # `args` chứa các tham số sau lệnh \cmd add
    if args:
        # Ví dụ: xử lý lệnh \cmd add với một tham số
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

