import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

ASK_QUANTITY, ASK_USERNAME = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [["✅ شراء", "📋 معاملاتي"], ["🛒 شحن auto", "🔧 شحن يدوي"],
                ["🎉 عروضنا", "📞 الدعم الفني"], ["💰 محفظتي", "⚙️ أنظمة البوت"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("مرحباً بك! الرجاء اختيار أحد الأزرار أدناه:", reply_markup=reply_markup)
    return ConversationHandler.END

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("📦 أدخل الكمية المطلوبة:")
    return ASK_QUANTITY

async def quantity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["quantity"] = update.message.text
    await update.message.reply_text("📲 أدخل رابط أو معرف الحساب:")
    return ASK_USERNAME

async def username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    quantity = int(context.user_data.get("quantity", 1))
    price_per_unit = 20020
    total_price = quantity * price_per_unit
    await update.message.reply_text(
        f"💰 السعر الأساسي: {price_per_unit:,} ل.س\\n✨ السعر النهائي: {total_price:,} ل.س"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ تم إلغاء العملية.")
    return ConversationHandler.END

if __name__ == '__main__':
    import os
    TOKEN = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^(✅ شراء)$"), buy)],
        states={
            ASK_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, quantity)],
            ASK_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, username)],
        },
        fallbacks=[MessageHandler(filters.Regex("^(❌ إلغاء)$"), cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex("^(❌ إلغاء)$"), cancel))
    application.run_polling()
