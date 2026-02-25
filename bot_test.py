import os
import logging
import html
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from database.db_manager import db
from utils.keyboards import main_menu_keyboard

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# Silence frequent httpx logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# No Heartbeat Server needed for local testing

from handlers.menu_handler import show_categories, handle_callback
from handlers.daily_practice_handler import start_daily_practice
from handlers.profile_handler import show_profile
from handlers.practice_handler import handle_answer
from handlers.add_topic_handler import add_topic_conv
from telegram.ext import CallbackQueryHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.register_user(user.id, user.username, user.first_name, user.last_name)
    
    first_name = html.escape(user.first_name)
    welcome_msg = (
        f"TEST BOT 🧪\n\n"
        f"Hello {first_name}, this is the local testing environment.\n\n"
        "Choose a mode to start:"
    )
    
    await update.message.reply_text(welcome_msg, reply_markup=main_menu_keyboard(), parse_mode='HTML')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "Daily Practice 🕒":
        await start_daily_practice(update, context)
    elif text == "Custom Practice 🛠️":
        await show_categories(update, context)
    elif text == "My Profile 👤":
        await show_profile(update, context)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    import traceback
    import html
    
    logging.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    
    message = (
        f"🚨 <b>Test Bot Error:</b>\n\n"
        f"<code>{html.escape(tb_string[-4000:])}</code>"
    )
    
    if not update:
        return

    chat_id = None
    if hasattr(update, 'effective_chat') and update.effective_chat:
        chat_id = update.effective_chat.id
    elif hasattr(update, 'callback_query') and update.callback_query.message:
        chat_id = update.callback_query.message.chat_id
    
    if chat_id:
        try:
            await context.bot.send_message(chat_id, message, parse_mode='HTML')
        except Exception as e:
            logging.error(f"Failed to send error message to Telegram: {e}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN_TEST")
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN_TEST is missing from environment variables.")
        exit(1)
        
    print("Starting TEST BOT (Local Environment)...")
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(add_topic_conv)
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    application.add_error_handler(error_handler)
    
    print("Test Bot is starting...")
    application.run_polling()
