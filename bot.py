import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Lấy token Telegram bot từ biến môi trường
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Lấy cookie từ biến môi trường
XB_USER_ID = os.getenv("XB_USER_ID")
XB_USER_LOGIN = os.getenv("XB_USER_LOGIN")
XB_USER_TOKEN = os.getenv("XB_USER_TOKEN")

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot đã sẵn sàng. Gửi mã giftcode để nhập.")

# Hàm xử lý mã giftcode gửi vào
async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    
    headers = {
        "cookie": f"xb_user_id={XB_USER_ID}; xb_user_login={XB_USER_LOGIN}; xb_user_token={XB_USER_TOKEN}"
    }
    url = f"https://xworld.info/vi-VN/giftcode/check/{code}"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        message = data.get("message", "Không có phản hồi từ server.")
    except Exception as e:
        message = f"Lỗi khi gửi yêu cầu: {e}"

    await update.message.reply_text(message)

# Khởi tạo bot và chạy
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("giftcode", handle_code))  # Có thể xài /giftcode CODE
    app.add_handler(CommandHandler("code", handle_code))       # Hoặc /code CODE
    app.add_handler(CommandHandler("", handle_code))           # Hoặc gửi mã trống
    app.add_handler(CommandHandler(None, handle_code))         # fallback

    app.run_polling()

if __name__ == "__main__":
    main()
