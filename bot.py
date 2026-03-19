from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8431502772

PHOTO_URL = "raj.jpg"
CHANNEL_LINK = "https://t.me/+p2oG2g4fNxAwYjc9"
ADMIN_USERNAME = "ADS_EXPERT_RAJ"  # without @

# MENU
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📢 Meta Ads", callback_data="meta")],
        [InlineKeyboardButton("🌐 Landing Page", callback_data="landing")],
        [InlineKeyboardButton("🤖 Bots", callback_data="bots")],
        [InlineKeyboardButton("✍️ Other", callback_data="other")],
        [
            InlineKeyboardButton("📩 Message Admin", url=f"https://t.me/{ADMIN_USERNAME}"),
            InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=(
            "🔥 *Welcome to Raj Digital Services* 🚀\n\n"
            "💼 We provide premium services:\n\n"
            "📢 Meta Ads\n"
            "🌐 Landing Pages\n"
            "🤖 Automation Bots\n\n"
            "👇 *Choose a service below*"
        ),
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# BUTTON HANDLER
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "meta":
        await query.message.reply_text(
            "📢 *META ADS SERVICE* 🚀\n\n"
            "💰 Weekly: ₹2,500\n"
            "💰 Monthly: ₹10,000\n\n"
            "✅ High converting ads\n"
            "✅ Targeted audience\n"
            "✅ Full setup",
            parse_mode="Markdown"
        )

    elif query.data == "landing":
        await query.message.reply_text(
            "🌐 *LANDING PAGE SERVICE* 🎨\n\n"
            "💰 Basic: ₹1,000\n"
            "💰 Premium: ₹1,500\n\n"
            "✅ Modern design\n"
            "✅ Mobile responsive\n"
            "✅ High conversion",
            parse_mode="Markdown"
        )

    elif query.data == "bots":
        await query.message.reply_text(
            "🤖 *BOT SERVICE* ⚡\n\n"
            "💰 Basic: ₹500/month\n"
            "💰 Advanced: Discuss price\n\n"
            "✅ Automation\n"
            "✅ Custom features",
            parse_mode="Markdown"
        )

    elif query.data == "other":
        await query.message.reply_text(
            "✍️ *Custom Requirement*\n\nSend your message 👇",
            parse_mode="Markdown"
        )
        context.user_data["waiting"] = True
        return

    # BACK MENU
    await query.message.reply_text(
        "👇 *Choose Service*",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

# HANDLE MESSAGE
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if context.user_data.get("waiting"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 *New Inquiry*\n\n👤 @{user.username}\n🆔 {user.id}\n💬 {text}",
            parse_mode="Markdown"
        )

        await update.message.reply_text(
            "✅ Message sent! We’ll contact you soon 🚀",
            reply_markup=main_menu()
        )

        context.user_data["waiting"] = False

# ADMIN REPLY
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = context.args[0]
        msg = " ".join(context.args[1:])

        await context.bot.send_message(chat_id=user_id, text=f"💬 {msg}")
        await update.message.reply_text("✅ Sent!")

    except:
        await update.message.reply_text("❌ Use:\n/reply USER_ID message")

# MAIN
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
