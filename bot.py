import os
import logging
import html
import threading
import http.server
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
from database.db_manager import db
from utils.keyboards import main_menu_keyboard

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# Silence frequent httpx logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# Heartbeat Server to keep Render awake
def run_heartbeat():
    class HeartbeatHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is alive!")

        def log_message(self, format, *args):
            return # Silence server logs

    port = int(os.environ.get("PORT", 10000))
    server = http.server.HTTPServer(("0.0.0.0", port), HeartbeatHandler)
    print(f"Heartbeat server started on port {port}")
    server.serve_forever()

# Start heartbeat in a separate thread
threading.Thread(target=run_heartbeat, daemon=True).start()


def get_bot_token():
    env = os.getenv("ENV", "production").lower()
    if env in ("development", "test", "testing"):
        token = os.getenv("TELEGRAM_BOT_TOKEN_TEST")
        if token:
            logging.info("Using TELEGRAM_BOT_TOKEN_TEST because ENV=%s", env)
            return token

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        logging.info("Using TELEGRAM_BOT_TOKEN")
        return token

    raise RuntimeError("Telegram bot token is missing. Set TELEGRAM_BOT_TOKEN_TEST for development or TELEGRAM_BOT_TOKEN for production.")

from handlers.menu_handler import show_categories, handle_callback
from handlers.daily_v2_handler import start_daily_practice
print(">>> v1.2.0 CURRICULUM ACTIVE <<<")
print("DEBUG HANDLERS:", os.listdir('handlers'))
from handlers.profile_handler import show_profile
from handlers.practice_handler import handle_answer
from handlers.add_topic_handler import add_topic_conv
from telegram.ext import CallbackQueryHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        db.register_user(user.id, user.username, user.first_name, user.last_name)
    except Exception:
        logging.exception("Failed to register user during /start")
        await update.message.reply_text(
            "Database is currently unavailable. Please check Supabase and try again.",
            parse_mode='HTML'
        )
        return
    
    first_name = html.escape(user.first_name or "there")
    
    # Inform user about database mode
    db_mode = f" (Mode: {db.driver.upper() if db.driver else 'NONE'})"
    
    welcome_msg = (
        f"Welcome 🎓 <b>GMAT Mastery Bot</b> (v1.2.0-CURRICULUM){db_mode}!\n\n"
        f"Hello {first_name}, I'll help you master GMAT Quant, Verbal, and Data Insights.\n\n"
        "Choose a mode to start:"
    )
    
    await update.message.reply_text(welcome_msg, reply_markup=main_menu_keyboard(), parse_mode='HTML')

    web_app_url = os.getenv("WEB_APP_URL")
    if web_app_url:
        await update.message.reply_text(
            "Mini App is available here:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open Practice App", web_app=WebAppInfo(web_app_url))]]
            )
        )
    elif os.getenv("ENV", "production").lower() in ("development", "test", "testing"):
        await update.message.reply_text(
            "Mini App is not linked yet. Set WEB_APP_URL in .env, restart the bot, then send /app."
        )


async def open_practice_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app_url = os.getenv("WEB_APP_URL")
    if web_app_url:
        await update.message.reply_text(
            "Open the practice app:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open Practice App", web_app=WebAppInfo(web_app_url))]]
            )
        )
        return

    await update.message.reply_text(
        "WEB_APP_URL is not configured yet.\n\n"
        "Run the UI server, expose it with an HTTPS tunnel, put that HTTPS URL in .env as WEB_APP_URL, then restart this test bot."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "Daily Practice 🕒":
        await start_daily_practice(update, context)
    elif text == "Custom Practice 🛠️":
        await show_categories(update, context)
    elif text == "My Profile 👤":
        await show_profile(update, context)
    elif text == "Open Practice App":
        await open_practice_app(update, context)

async def db_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        conn = db.get_connection()
        status = "Connected ✅" if conn else "Disconnected ❌"
        categories = db.get_categories()
        cat_count = len(categories) if isinstance(categories, list) else "Error"
        error_text = ""
    except Exception as exc:
        logging.exception("Database status check failed")
        status = "Disconnected ❌"
        cat_count = "Error"
        error_text = f"\nError: <code>{html.escape(str(exc)[:500])}</code>"
    
    msg = (
        f"🖥️ <b>Database Status:</b>\n"
        f"Connectivity: {status}\n"
        f"Driver: {db.driver.upper() if db.driver else 'None'}\n"
        f"Category Count: {cat_count}\n"
        f"Search Path: aptitude_practice / public"
        f"{error_text}"
    )
    await update.message.reply_text(msg, parse_mode='HTML')


async def send_smart_reminders(context: ContextTypes.DEFAULT_TYPE):
    try:
        db.ensure_engagement_schema()
        settings = db.get_enabled_reminder_settings()
    except Exception:
        logging.exception("Failed to load reminder settings")
        return

    for row in settings:
        try:
            timezone = ZoneInfo(row.get("timezone") or "Asia/Kolkata")
            now = datetime.now(timezone)
            reminder_time = row.get("reminder_time") or "20:00"
            hours, minutes = [int(part) for part in reminder_time.split(":")]
            target_minutes = hours * 60 + minutes
            current_minutes = now.hour * 60 + now.minute
            if current_minutes < target_minutes or current_minutes - target_minutes > 10:
                continue

            last_reminded_at = row.get("last_reminded_at")
            if last_reminded_at and last_reminded_at.astimezone(timezone).date() == now.date():
                continue

            user_id = row["user_id"]
            if db.get_today_solved_count(user_id):
                continue

            first_name = row.get("first_name") or "there"
            await context.bot.send_message(
                user_id,
                f"Hi {html.escape(first_name)}, your practice is still pending today. Open the app and solve a quick 5-question set.",
            )
            db.mark_reminder_sent(user_id)
        except Exception:
            logging.exception("Failed to send reminder for row: %s", row)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    import traceback
    import html
    
    # Log the error
    logging.error("Exception while handling an update:", exc_info=context.error)
    
    # Collect traceback
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    
    # Keep full tracebacks out of production chats.
    if os.getenv("ENV", "production").lower() == "development":
        message = (
            f"🚨 <b>An error occurred:</b>\n\n"
            f"<code>{html.escape(tb_string[-4000:])}</code>" # Truncate if too long
        )
    else:
        message = "🚨 <b>An error occurred.</b>\n\nPlease try again in a moment."
    
    if not update:
        return

    # Try to send to the user
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
    try:
        db.ensure_engagement_schema()
    except Exception:
        logging.exception("Could not initialize engagement schema on bot startup")

    application = ApplicationBuilder().token(get_bot_token()).connect_timeout(30).read_timeout(30).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('app', open_practice_app))
    application.add_handler(CommandHandler('db_status', db_status))
    application.add_handler(add_topic_conv)
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    application.add_error_handler(error_handler)

    if application.job_queue:
        application.job_queue.run_repeating(send_smart_reminders, interval=300, first=30)
    else:
        logging.warning("Smart reminders are disabled because python-telegram-bot job-queue extra is not installed.")
    
    print("Bot is starting...")
    application.run_polling()
