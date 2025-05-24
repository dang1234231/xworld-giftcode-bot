import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

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

        if data.get("status") == True:
            await update.message.reply_text(f"✅ Thành công: {data.get('msg')}")
        else:
            await update.message.reply_text(f"❌ Thất bại: {data.get('msg')}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Lỗi khi xử lý: {e}")

# Hàm chính khởi động bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))  # Xử lý lệnh /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))  # Xử lý giftcode

    app.run_polling()

if __name__ == "__main__":
    main()
