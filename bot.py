from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 8431502772 # 👈 put your telegram user id here

# Menu keyboard
menu = ReplyKeyboardMarkup(
    [["1", "2"], ["3", "4"]],
    resize_keyboard=True
)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hlo 👋 What are you looking for?\n\n"
        "1️⃣ Meta Ads\n"
        "2️⃣ Landing Page\n"
        "3️⃣ Bots\n"
        "4️⃣ Other",
        reply_markup=menu
    )

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user

    # OPTION 1 - META ADS
    if text == "1":
        await update.message.reply_text(
            "📢 Meta Ads Pricing:\n\n"
            "💰 Weekly: ₹2,500\n"
            "💰 Monthly: ₹10,000\n\n"
            "Message me to start 🚀"
        )

    # OPTION 2 - LANDING PAGE
    elif text == "2":
        await update.message.reply_text(
            "🌐 Landing Page Pricing:\n\n"
            "💰 Basic: ₹1,000\n"
            "💰 Premium: ₹1,500\n\n"
            "Price depends on design & features ✨"
        )

    # OPTION 3 - BOTS
    elif text == "3":
        await update.message.reply_text(
            "🤖 Bot Pricing:\n\n"
            "💰 Simple Bot: ₹500/month\n"
            "💰 Advanced Bots: Price will be discussed\n\n"
            "Tell me your requirement 👍"
        )

    # OPTION 4 - OTHER (SAVE MESSAGE)
    elif text == "4":
        await update.message.reply_text(
            "✍️ Please write your message:"
        )
        context.user_data["waiting_for_msg"] = True
        return

    # SAVE USER MESSAGE
    elif context.user_data.get("waiting_for_msg"):
        msg = text

        # send to admin
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 New Message:\n\n👤 @{user.username}\n🆔 {user.id}\n💬 {msg}"
        )

        await update.message.reply_text(
            "✅ Your message has been saved. I will contact you soon."
        )

        context.user_data["waiting_for_msg"] = False

    # ADMIN COMMAND TO VIEW MESSAGES (optional manual trigger)
    elif text.lower() == "/saved" and user.id == ADMIN_ID:
        await update.message.reply_text("📩 Messages are sent directly to you already.")

    # INVALID INPUT
    else:
        await update.message.reply_text(
            "❌ Please select a valid option (1, 2, 3, 4)",
            reply_markup=menu
        )
        return

    # RETURN TO MENU AFTER EVERY TASK
    await update.message.reply_text(
        "\n🔁 What do you need next?\n\n"
        "1️⃣ Meta Ads\n"
        "2️⃣ Landing Page\n"
        "3️⃣ Bots\n"
        "4️⃣ Other",
        reply_markup=menu
    )

# MAIN
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
