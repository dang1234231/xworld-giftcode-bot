import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Thông tin xác thực cookie người dùng (cần thay thế bằng giá trị thật)
COOKIES = {
    "xb_user_id": "YOUR_USER_ID",
    "xb_user_login": "YOUR_USER_LOGIN",
    "xb_user_token": "YOUR_USER_TOKEN"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gửi /giftcode CODE để nhập giftcode vào XWorld.")

async def giftcode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Sai cú pháp. Dùng: /giftcode CODE")
        return

    code = context.args[0]
    url = "https://xworld.info/vi-VN/giftcode"
    response = requests.post(url, data={"giftcode": code}, cookies=COOKIES)

    if "thành công" in response.text.lower():
        await update.message.reply_text(f"✅ Đã nhập giftcode: {code}")
    elif "đã sử dụng" in response.text.lower():
        await update.message.reply_text(f"⚠️ Giftcode đã sử dụng hoặc không hợp lệ: {code}")
    else:
        await update.message.reply_text(f"❌ Không thể nhập giftcode.")

def main():
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("giftcode", giftcode))
    app.run_polling()

if __name__ == "__main__":
    main()