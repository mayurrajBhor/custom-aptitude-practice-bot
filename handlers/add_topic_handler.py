from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from database.db_manager import db
from llm.generator import generator
import html

# States
SELECT_CATEGORY, SELECT_TOPIC, INPUT_PATTERN, CONFIRM_RESTRUCTURING = range(4)

async def start_add_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = db.get_categories()
    keyboard = [[InlineKeyboardButton(cat['name'], callback_data=f"addcat_{cat['id']}")] for cat in categories]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Let's add a new practice pattern! 🎓\nStep 1: Select a GMAT Category:",
        reply_markup=reply_markup
    )
    return SELECT_CATEGORY

async def category_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    cat_id = int(query.data.split('_')[1])
    context.user_data['add_topic_cat_id'] = cat_id
    
    topics = db.get_topics(cat_id)
    keyboard = [[InlineKeyboardButton(t['name'], callback_data=f"addtopic_{t['id']}")] for t in topics]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "Step 2: Select a Topic:",
        reply_markup=reply_markup
    )
    return SELECT_TOPIC

async def topic_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    topic_id = int(query.data.split('_')[1])
    context.user_data['add_topic_id'] = topic_id
    
    await query.message.edit_text(
        "Step 3: Describe the new pattern in your own words.\n"
        "Tell me what specific GMAT concept or problem type you want to practice.\n"
        "(e.g., 'Work rate problems with three people and one of them leaves halfway')"
    )
    return INPUT_PATTERN

async def pattern_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text
    await update.message.reply_text("Restructuring your input... ⏳")
    
    restructured, error = generator.restructure_pattern(raw_text)
    
    if error:
        await update.message.reply_text(f"❌ Error during restructuring: {error}\n\nPlease try describing it again.")
        return INPUT_PATTERN
    
    context.user_data['temp_pattern'] = restructured
    
    msg = (
        f"🎯 <b>I've restructured your pattern:</b>\n\n"
        f"<b>Name:</b> {html.escape(restructured['name'])}\n"
        f"<b>Description:</b> {html.escape(restructured['description'])}\n"
        f"<b>Difficulty:</b> {restructured['difficulty']}/5\n\n"
        "Does this look correct?"
    )
    
    keyboard = [
        [InlineKeyboardButton("Confirm ✅", callback_data="confirm_pattern")],
        [InlineKeyboardButton("Try Again 🔄", callback_data="retry_pattern")],
        [InlineKeyboardButton("Cancel ❌", callback_data="cancel_add")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode='HTML')
    return CONFIRM_RESTRUCTURING

async def confirm_restructuring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "confirm_pattern":
        p = context.user_data['temp_pattern']
        pattern_id = db.add_pattern(
            context.user_data['add_topic_id'],
            p['name'],
            p['description'],
            p['difficulty'],
            user_id=update.effective_user.id
        )
        
        if pattern_id:
            await query.message.edit_text(
                f"✅ <b>Successfully added!</b>\n"
                f"'{html.escape(p['name'])}' is now available in your practice list.",
                parse_mode='HTML'
            )
        else:
            await query.message.edit_text(
                "❌ <b>Database Error</b>\n"
                "I couldn't save this pattern to the database. Please try again later.",
                parse_mode='HTML'
            )
        
        # Reset context
        del context.user_data['temp_pattern']
        return ConversationHandler.END
        
    elif query.data == "retry_pattern":
        await query.message.edit_text("Please describe the pattern again with more detail.")
        return INPUT_PATTERN
        
    else:
        await query.message.edit_text("Action canceled.")
        return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Process canceled.")
    return ConversationHandler.END

add_topic_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Add a topic ➕$"), start_add_topic)],
    states={
        SELECT_CATEGORY: [CallbackQueryHandler(category_choice, pattern="^addcat_")],
        SELECT_TOPIC: [CallbackQueryHandler(topic_choice, pattern="^addtopic_")],
        INPUT_PATTERN: [MessageHandler(filters.TEXT & (~filters.COMMAND), pattern_input)],
        CONFIRM_RESTRUCTURING: [CallbackQueryHandler(confirm_restructuring, pattern="^(confirm_pattern|retry_pattern|cancel_add)$")]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
